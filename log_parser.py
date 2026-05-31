from typing import Set

def parse_failed_ips(log_path: str) -> dict[str, int]:
    """
    Lee un archivo auth.log línea a línea.
    Devuelve un diccionario {ip: número_de_fallos}.
    """
    failed_ips: dict[str, int] = {}

    with open(log_path, "r") as f:
        for line in f:
            if "Failed password" in line:
                parts: list[str] = line.strip().split()
                # La IP está después de "from"
                if "from" in parts:
                    ip_index: int = parts.index("from") + 1
                    ip: str = parts[ip_index]

                    failed_ips[ip] = failed_ips.get(ip, 0) + 1

    return failed_ips

def get_unique_attackers(failed_ips: dict[str, int]) -> Set[str]:
    """Devuelve un Set con las IPs únicas que han fallado."""
    return set(failed_ips.keys())

def print_failed_summary(failed_ips: dict[str, int]) -> None:
    unique: Set[str] = get_unique_attackers(failed_ips)
    print(f"\n{'─'*40}")
    print(f"IPs únicas atacantes: {len(unique)}")
    print(f"{'─'*40}")
    for ip, count in sorted(failed_ips.items(), key=lambda x: x[1], reverse=True):
        print(f"  {ip:<20} {count} intentos fallidos")