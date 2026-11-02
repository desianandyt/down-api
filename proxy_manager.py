import os
import random
import logging
from typing import Dict, List, Optional

logger = logging.getLogger("proxy_manager")

BUILTIN_PROXIES = [
    "http://qlezdepm:sennijjqf08p@45.38.107.97:6014",
    "http://qlezdepm:sennijjqf08p@64.137.96.74:6641",
    "http://qlezdepm:sennijjqf08p@198.23.243.226:6361",
    "http://qlezdepm:sennijjqf08p@38.154.185.97:6370",
    "http://qlezdepm:sennijjqf08p@84.247.60.125:6095",
    "http://qlezdepm:sennijjqf08p@191.96.254.138:6185",
    "http://qlezdepm:sennijjqf08p@198.46.161.42:5092",
    "http://qlezdepm:sennijjqf08p@64.137.10.153:5803",
    "http://qlezdepm:sennijjqf08p@104.164.49.38:7693",
    "http://qlezdepm:sennijjqf08p@23.26.71.145:5628"
]


class ProxyPool:
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
                logger.info(f"Loaded {len(self.proxies)} proxies from environment")
                return

        # 2. Use built-in proxies
        self.proxies = list(BUILTIN_PROXIES)
        logger.info(f"Loaded {len(self.proxies)} built-in rotation proxies")

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


proxy_pool = ProxyPool()
