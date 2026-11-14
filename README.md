# ip-info

Show your public IP address, location and ISP — a zero-dependency Python CLI.

## Requirements

- Python 3.8+
- No third-party packages, no API key. Uses [ip-api.com](http://ip-api.com) (free tier) and [ipify](https://www.ipify.org) for IPv6 detection.

## Usage

```bash
python3 ip_info.py                 # your own public IPv4 address
python3 ip_info.py --ipv6          # your own public IPv6 address
python3 ip_info.py 8.8.8.8         # look up a specific IP
python3 ip_info.py --json          # machine-readable JSON output
```

## Example output

```
IP       8.8.8.8
Location Ashburn, Virginia, United States (US) 20149
Coords   39.03, -77.5
Timezone America/New_York
ISP      Google LLC
Org      Google Public DNS
ASN      AS15169 Google LLC
```

## Notes

- ip-api.com's free tier allows 45 requests per minute from one IP.
- The `--ipv6` lookup first fetches your IPv6 address from api64.ipify.org, then looks it up — useful on IPv6-only VPS nodes.
