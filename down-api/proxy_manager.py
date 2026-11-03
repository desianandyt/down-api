import os
import random
import logging
from typing import Dict, List, Optional

logger = logging.getLogger("proxy_manager")


class ProxyPool:
    """
    ProxyPool handles proxy rotation.
    By default, it operates in pure ZERO-PROXY (DIRECT) mode for maximum speed and 100% free usage.
    If the user supplies custom proxies via PROXY_LIST or PROXY_URL, it rotates them.
    """
    def __init__(self):
        self.proxies: List[str] = []
        self._index = 0
        self.reload()

    def reload(self):
        # 1. Check PROXY_URL / PROXY_LIST env var
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

    def get_proxy(self) -> Optional[str]:
        if not self.proxies:
            return None
        proxy = self.proxies[self._index % len(self.proxies)]
        self._index = (self._index + 1) % len(self.proxies)
        return proxy

    def get_random_proxy(self) -> Optional[str]:
        if not self.proxies:
            return None
        return random.choice(self.proxies)

    def get_dict(self) -> Optional[Dict[str, str]]:
        p = self.get_proxy()
        return {"http": p, "https": p} if p else None

    def get_all(self) -> List[str]:
        return list(self.proxies)

    @property
    def is_direct(self) -> bool:
        return len(self.proxies) == 0

    @property
    def status_summary(self) -> str:
        if self.is_direct:
            return "Zero-Proxy (Direct High-Speed)"
        return f"{len(self.proxies)} active custom proxies"


proxy_pool = ProxyPool()
