"""Strict validation and routing helpers for per-profile VLESS XHTTP CDN."""
import re

PROVIDERS = {"yandex", "vk", "custom"}
MODES = {"packet-up", "stream-up", "auto"}
UPLINK_METHODS = {"post", "get"}
FINGERPRINTS = {"chrome", "firefox", "safari", "edge", "random", "randomized"}
HOST_RE = re.compile(r"(?=.{1,253}\Z)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\Z")


class CDNError(ValueError):
    pass


def defaults():
    return {
        "enabled": False,
        "provider": "yandex",
        "public_host": "",
        "sni": "",
        "host_header": "",
        "mode": "packet-up",
        "uplink_method": "post",
        "fingerprint": "chrome",
    }


def _host(value, label, required=False):
    value = str(value or "").strip().lower().rstrip(".")
    if value.startswith("http://") or value.startswith("https://") or "/" in value or ":" in value:
        raise CDNError(f"{label}: укажите только домен без https://, пути и порта.")
    if value and not HOST_RE.fullmatch(value):
        raise CDNError(f"{label}: некорректное доменное имя.")
    if required and not value:
        raise CDNError(f"{label}: поле обязательно.")
    return value


def normalize(value):
    source = value if isinstance(value, dict) else {}
    result = defaults()
    result["enabled"] = bool(source.get("enabled", False))
    result["provider"] = str(source.get("provider", "yandex")).strip().lower()
    if result["provider"] not in PROVIDERS:
        raise CDNError("Неизвестный CDN-провайдер.")
    result["public_host"] = _host(source.get("public_host"), "Публичный домен CDN", result["enabled"])
    result["sni"] = _host(source.get("sni"), "TLS SNI") or result["public_host"]
    result["host_header"] = _host(source.get("host_header"), "HTTP Host") or result["public_host"]
    result["mode"] = str(source.get("mode", "packet-up")).strip().lower()
    if result["mode"] not in MODES:
        raise CDNError("Неизвестный режим XHTTP.")
    result["uplink_method"] = str(source.get("uplink_method", "post")).strip().lower()
    if result["uplink_method"] not in UPLINK_METHODS:
        raise CDNError("Неизвестный HTTP-метод XHTTP.")
    if result["uplink_method"] == "get":
        result["mode"] = "packet-up"
    result["fingerprint"] = str(source.get("fingerprint", "chrome")).strip().lower()
    if result["fingerprint"] not in FINGERPRINTS:
        raise CDNError("Неизвестный TLS fingerprint.")
    return result


def _get_only_extra():
    return {
        "mode": "packet-up",
        "uplinkHTTPMethod": "GET",
        "uplinkDataPlacement": "header",
        "uplinkDataKey": "X-Data",
        "uplinkChunkSize": 2048,
    }


def server_xhttp(path, get_only=False):
    result = {"path": path, "mode": "auto"}
    if get_only:
        result.update(_get_only_extra())
    return result


def profile_from_request(request):
    """Return a validated per-VLESS CDN profile or None for a direct route."""
    source = request if isinstance(request, dict) else {}
    route = str(source.get("vless_route", "direct")).strip().lower()
    if route == "direct":
        return None
    if route != "cdn":
        raise CDNError("Неизвестный маршрут VLESS.")
    return normalize({
        "enabled": True,
        "provider": source.get("vless_cdn_provider", "yandex"),
        "public_host": source.get("vless_cdn_public_host", ""),
        "sni": source.get("vless_cdn_sni", ""),
        "host_header": source.get("vless_cdn_host_header", ""),
        "mode": "packet-up",
        "uplink_method": "get",
        "fingerprint": source.get("vless_cdn_fingerprint", "chrome"),
    })


def vless_route(origin_domain, profile=None):
    try:
        value = normalize(profile) if isinstance(profile, dict) else defaults()
    except CDNError:
        value = defaults()
    if not value["enabled"]:
        return {
            "enabled": False,
            "address": origin_domain,
            "sni": origin_domain,
            "host": origin_domain,
            "mode": "auto",
            "extra": None,
            "fingerprint": value.get("fingerprint", "chrome"),
        }
    return {
        "enabled": True,
        "address": value["public_host"],
        "sni": value["sni"],
        "host": value["host_header"],
        "mode": value["mode"],
        "extra": _get_only_extra() if value["uplink_method"] == "get" else None,
        "fingerprint": value["fingerprint"],
    }
