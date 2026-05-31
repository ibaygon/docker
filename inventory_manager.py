import pandas as pd
from datetime import datetime

def load_inventory(path: str = "data/inventory.csv") -> pd.DataFrame:
    return pd.read_csv(path)

def filter_vulnerable(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra servidores Windows o con menos de 4GB de RAM."""
    windows = df["os"].str.contains("Windows Server")
    low_ram = df["ram_gb"] < 4
    return df[windows | low_ram].copy()

def group_by_department(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("department").size().reset_index(name="total_servers")

def generate_excel_report(df_vulnerable: pd.DataFrame, output_path: str | None = None) -> None:
    if output_path is None:
        today = datetime.today().strftime("%Y-%m")
        output_path = f"data/report_{today}.xlsx"

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df_vulnerable.to_excel(writer, sheet_name="Vulnerables", index=False)
        group_by_department(df_vulnerable).to_excel(writer, sheet_name="Por Departamento", index=False)

    print(f"✅ Reporte generado: {output_path}")

if __name__ == "__main__":
    df = load_inventory()
    vulnerable = filter_vulnerable(df)
    print(f"\nServidores vulnerables: {len(vulnerable)} de {len(df)}")
    print(group_by_department(vulnerable).to_string(index=False))
    generate_excel_report(vulnerable)