import csv
import random
from faker import Faker

fake = Faker()

OS_OPTIONS   = ["Windows Server 2019", "Windows Server 2022", "Ubuntu 22.04", "CentOS 7", "Debian 11"]
DEPARTMENTS  = ["IT", "RRHH", "Finanzas", "Operaciones", "Marketing", "Seguridad"]
RAM_OPTIONS  = [2, 4, 8, 16, 32, 64]

def generate_inventory(output_path: str = "data/inventory.csv", rows: int = 1000) -> None:
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["hostname", "ip", "os", "ram_gb", "department", "last_update"])

        for _ in range(rows):
            writer.writerow([
                fake.hostname(),
                fake.ipv4_private(),
                random.choice(OS_OPTIONS),
                random.choice(RAM_OPTIONS),
                random.choice(DEPARTMENTS),
                fake.date_between(start_date="-3y", end_date="today"),
            ])

    print(f"✅ Inventario generado: {output_path} ({rows} filas)")

if __name__ == "__main__":
    generate_inventory()