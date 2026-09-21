# IT Support Health Checker

A small Python diagnostic tool built for IT support and cloud support scenarios.

## What it does

- Collects basic system information
- Checks local disk usage
- Resolves DNS for configured targets
- Tests TCP connectivity to common services
- Exports results to a JSON report
- Supports custom targets through a JSON config file

## Why I built it

I wanted a small project that connects my professional IT support background with my current Python and cloud learning.

The goal was to automate a few checks that are useful during basic troubleshooting instead of checking every item manually.

## Skills demonstrated

- Python
- Troubleshooting
- Networking fundamentals
- DNS
- TCP connectivity
- JSON
- File handling
- Error handling
- Command-line arguments
- Automation

## Requirements

Python 3.10+.

No external Python packages are required.

## Run

```bash
python health_checker.py
```

The script creates:

```text
health_report.json
```

## Use a custom target list

Create a JSON file like this:

```json
[
  {
    "name": "Microsoft Login",
    "host": "login.microsoftonline.com",
    "port": 443
  },
  {
    "name": "GitHub",
    "host": "github.com",
    "port": 443
  }
]
```

Then run:

```bash
python health_checker.py --config targets.json
```

You can also choose a different output file:

```bash
python health_checker.py --config targets.json --output report.json
```

## Example output

```text
=== IT SUPPORT HEALTH CHECK ===
Host: DESKTOP-EXAMPLE
OS: Windows 11
Disk: 59.2% used (OK)

Connectivity:
- Cloudflare DNS: DNS=ok, TCP=reachable
- GitHub HTTPS: DNS=ok, TCP=reachable
- Microsoft Login: DNS=ok, TCP=reachable

Report saved to: health_report.json
```

## Future improvements

- Add CPU and memory checks
- Add Windows service status checks
- Add Microsoft Graph API checks
- Add CSV export
- Add logging
- Add automated tests
- Add a PowerShell version for comparison

## Portfolio context

This project is part of my continued development toward cloud support, automation, and security-focused IT roles.

