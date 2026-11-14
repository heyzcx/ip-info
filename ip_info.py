#!/usr/bin/env python3
"""ip-info: show your public IP address, location and ISP.

Queries ip-api.com (no API key needed) and prints a short human-readable
summary, or machine-readable JSON with --json.

Usage:
    python3 ip_info.py            # IPv4 lookup (default)
    python3 ip_info.py --ipv6     # IPv6 lookup
    python3 ip_info.py --json     # JSON output
    python3 ip_info.py 8.8.8.8    # look up a specific IP
"""

import argparse
import json
import sys
import urllib.error
import urllib.request

API_URL = "http://ip-api.com/json/{ip}?fields=status,message,query,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as"
TIMEOUT = 10


def lookup(ip):
    """Return the ip-api.com record for *ip* (empty string = own IP)."""
    url = API_URL.format(ip=ip or "")
    req = urllib.request.Request(url, headers={"User-Agent": "ip-info/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.load(resp)
    except urllib.error.URLError as exc:
        raise SystemExit(f"error: cannot reach ip-api.com ({exc.reason})")
    if data.get("status") != "success":
        raise SystemExit(f"error: lookup failed: {data.get('message', 'unknown')}")
    return data


def render(data):
    lines = [
        f"IP       {data['query']}",
        f"Location {data['city']}, {data['regionName']}, "
        f"{data['country']} ({data['countryCode']}) {data.get('zip', '')}".rstrip(),
        f"Coords   {data['lat']}, {data['lon']}",
        f"Timezone {data['timezone']}",
        f"ISP      {data['isp']}",
        f"Org      {data['org']}",
        f"ASN      {data['as']}",
    ]
    return "\n".join(lines)


def own_ipv6():
    """Return this machine's public IPv6 address via api64.ipify.org."""
    req = urllib.request.Request("https://api64.ipify.org",
                                 headers={"User-Agent": "ip-info/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.read().decode().strip()
    except urllib.error.URLError as exc:
        raise SystemExit(f"error: cannot reach api64.ipify.org ({exc.reason})")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Show your public IP, location and ISP."
    )
    parser.add_argument("ip", nargs="?", default="",
                        help="IP address to look up (default: your own)")
    parser.add_argument("--ipv6", action="store_true",
                        help="look up your public IPv6 address")
    parser.add_argument("--json", action="store_true",
                        help="print the raw JSON record instead")
    args = parser.parse_args(argv)

    if args.ipv6 and args.ip:
        parser.error("--ipv6 cannot be combined with an explicit IP")
    ip = own_ipv6() if args.ipv6 else args.ip

    data = lookup(ip)
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(render(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
