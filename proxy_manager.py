import os
import random
import logging
import threading
import concurrent.futures
from typing import Dict, List, Optional
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger("proxy_manager")

FREE_PROXIES_SEED = [
    "http://176.111.37.216:39811",
    "http://176.111.37.5:39811",
    "http://5.42.97.67:8080"
]


class ProxyPool:
    """
    ProxyPool handles zero-proxy direct mode by default.
    When running in cloud datacenters (like Render) that encounter IP challenges (analyze_risk/Cloudflare),
    it provides 100% free auto-scraped public fallback proxies at zero cost.
    """
    def __init__(self):
        self.proxies: List[str] = []
        self.free_proxies: List[str] = list(FREE_PROXIES_SEED)
        self._index = 0
        self._free_index = 0
        self.reload()
        # Fetch fresh free public proxies in background thread for cloud fallback
        threading.Thread(target=self._background_refresh_free_proxies, daemon=True).start()

    def reload(self):
        # 1. Custom env proxies if supplied
        env_proxies = os.environ.get("PROXY_LIST") or os.environ.get("PROXY_URL")
        if env_proxies:
            lines = [p.strip() for p in env_proxies.replace(";", "\n").replace(",", "\n").splitlines() if p.strip()]
            parsed = []
            for item in lines:
                if item.startswith("http://") or item.startswith("https://") or item.startswith("socks5://"):
                    parsed.append(item)
                else:
                    parts = item.split(":")
                    if len(parts) == 4:
                        parsed.append(f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}")
                    elif len(parts) == 2:
                        parsed.append(f"http://{parts[0]}:{parts[1]}")
            if parsed:
                self.proxies = parsed
                logger.info(f"Loaded {len(self.proxies)} custom proxies from environment")
                return

        # 2. Pure Zero-Proxy (Direct) Mode by default
        self.proxies = []
        logger.info("Running in ZERO-PROXY Direct Mode (0 cost, ultra-fast native direct connections)")

    def _background_refresh_free_proxies(self):
        """Fetches and validates free public proxies in parallel for emergency cloud fallback."""
        try:
            r = requests.get("https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt", timeout=6, verify=False)
            candidates = [f"http://{p.strip()}" for p in r.text.splitlines() if p.strip()][:35]

            def check_p(p):
                try:
                    res = requests.get("https://httpbin.org/ip", proxies={"http": p, "https": p}, timeout=2.5, verify=False)
                    if res.status_code == 200:
                        return p
                except Exception:
                    pass
                return None

            working = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
                futures = [executor.submit(check_p, p) for p in candidates]
                for fut in concurrent.futures.as_completed(futures):
                    res = fut.result()
                    if res:
                        working.append(res)
                        if len(working) >= 6:
                            break

            if working:
                self.free_proxies = working
                logger.info(f"Refreshed {len(working)} verified free fallback proxies: {working[:2]}")
        except Exception as e:
            logger.debug(f"Free proxy background refresh error: {e}")

    def get_proxy(self) -> Optional[str]:
        if not self.proxies:
            return None
        proxy = self.proxies[self._index % len(self.proxies)]
        self._index = (self._index + 1) % len(self.proxies)
        return proxy

    def get_fallback_proxy(self) -> Optional[str]:
        """Returns a verified free public proxy when direct request gets Cloudflare/datacenter blocked."""
        if self.proxies:
            return self.get_proxy()
        if not self.free_proxies:
            return None
        proxy = self.free_proxies[self._free_index % len(self.free_proxies)]
        self._free_index = (self._free_index + 1) % len(self.free_proxies)
        return proxy

    def get_dict(self) -> Optional[Dict[str, str]]:
        p = self.get_proxy()
        return {"http": p, "https": p} if p else None

    def get_fallback_dict(self) -> Optional[Dict[str, str]]:
        p = self.get_fallback_proxy()
        return {"http": p, "https": p} if p else None

    def get_all(self) -> List[str]:
        return list(self.proxies)

    @property
    def is_direct(self) -> bool:
        return len(self.proxies) == 0

    @property
    def status_summary(self) -> str:
        if self.is_direct:
            return f"Zero-Proxy Direct (with {len(self.free_proxies)} free cloud fallbacks)"
        return f"{len(self.proxies)} active custom proxies"


proxy_pool = ProxyPool()
