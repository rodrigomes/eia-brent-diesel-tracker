import sys
from eia_client import EIAClient

def main():
    print("==================================================")
    print("   EIA Petroleum Tracker (Brent & US Diesel)     ")
    print("==================================================\n")

    try:
        client = EIAClient()
    except ValueError as e:
        print(f"[ERRO] {e}")
        sys.exit(1)

    print("1. Buscando últimas 5 cotações do Petróleo Brent...")
    try:
        df_brent = client.get_brent_prices(length=5)
        if not df_brent.empty:
            print("\n--- Cotações Recentes: Petróleo Brent ---")
            for _, row in df_brent.iterrows():
                print(f"Data: {row.get('period')} | Preço: ${row.get('value')} USD/Barril | ({row.get('series-description', 'Europe Brent Spot Price FOB')})")
        else:
            print("Nenhum dado retornado para o Brent.")
    except Exception as err:
        print(f"Erro ao buscar Brent: {err}")

    print("\n2. Buscando últimas 5 cotações do Diesel nos EUA (US Gulf Coast)...")
    try:
        df_diesel = client.get_us_diesel_prices(region="gulf_coast", length=5)
        if not df_diesel.empty:
            print("\n--- Cotações Recentes: US Diesel (Gulf Coast) ---")
            for _, row in df_diesel.iterrows():
                print(f"Data: {row.get('period')} | Preço: ${row.get('value')} USD/Galão | ({row.get('series-description', 'ULSD Spot Price')})")
        else:
            print("Nenhum dado retornado para o Diesel.")
    except Exception as err:
        print(f"Erro ao buscar Diesel: {err}")

if __name__ == "__main__":
    main()
