from __future__ import annotations

import argparse
import json
import platform
import shutil
import socket
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_TARGETS = [
    {"host": "1.1.1.1", "port": 53, "name": "Cloudflare DNS"},
    {"host": "github.com", "port": 443, "name": "GitHub HTTPS"},
    {"host": "login.microsoftonline.com", "port": 443, "name": "Microsoft Login"},
]


def get_system_info() -> dict:
    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
    }


def get_disk_info(path: str = ".") -> dict:
    usage = shutil.disk_usage(path)
    percent_used = round((usage.used / usage.total) * 100, 2)

    return {
        "path": str(Path(path).resolve()),
        "total_gb": round(usage.total / (1024**3), 2),
        "used_gb": round(usage.used / (1024**3), 2),
        "free_gb": round(usage.free / (1024**3), 2),
        "percent_used": percent_used,
        "status": "warning" if percent_used >= 90 else "ok",
    }


def resolve_dns(host: str) -> dict:
    try:
        ip = socket.gethostbyname(host)
        return {"host": host, "resolved_ip": ip, "status": "ok"}
    except socket.gaierror as exc:
        return {"host": host, "resolved_ip": None, "status": "failed", "error": str(exc)}


def check_tcp(host: str, port: int, timeout: float = 3.0) -> dict:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return {"host": host, "port": port, "status": "reachable"}
    except OSError as exc:
        return {
            "host": host,
            "port": port,
            "status": "unreachable",
            "error": str(exc),
        }


def load_targets(config_path: str | None) -> list[dict]:
    if not config_path:
        return DEFAULT_TARGETS

    path = Path(config_path)
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("Config must contain a JSON list of target objects.")

    return data


def run_checks(targets: list[dict]) -> dict:
    connectivity = []

    for target in targets:
        host = target["host"]
        port = int(target["port"])
        name = target.get("name", f"{host}:{port}")

        dns_result = resolve_dns(host)
        tcp_result = check_tcp(host, port)

        connectivity.append(
            {
                "name": name,
                "dns": dns_result,
                "tcp": tcp_result,
            }
        )

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "system": get_system_info(),
        "disk": get_disk_info(),
        "connectivity": connectivity,
    }


def print_summary(report: dict) -> None:
    print("\n=== IT SUPPORT HEALTH CHECK ===")
    print(f"Host: {report['system']['hostname']}")
    print(f"OS: {report['system']['os']} {report['system']['os_release']}")
    print(
        f"Disk: {report['disk']['percent_used']}% used "
        f"({report['disk']['status'].upper()})"
    )

    print("\nConnectivity:")
    for item in report["connectivity"]:
        dns_status = item["dns"]["status"]
        tcp_status = item["tcp"]["status"]
        print(f"- {item['name']}: DNS={dns_status}, TCP={tcp_status}")


def save_report(report: dict, output_path: str) -> None:
    path = Path(output_path)
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run basic IT support health checks.")
    parser.add_argument(
        "--config",
        help="Optional JSON file with custom host/port targets.",
    )
    parser.add_argument(
        "--output",
        default="health_report.json",
        help="Path for the generated JSON report.",
    )
    args = parser.parse_args()

    try:
        targets = load_targets(args.config)
        report = run_checks(targets)
        print_summary(report)
        save_report(report, args.output)
        print(f"\nReport saved to: {args.output}")
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
