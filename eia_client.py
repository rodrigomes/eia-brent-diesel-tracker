import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class EIAClient:
    """
    Cliente Python para integração com a API v2 da U.S. Energy Information Administration (EIA).
    Documentação oficial: https://www.eia.gov/opendata/
    """
    BASE_URL = "https://api.eia.gov/v2"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("EIA_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Chave de API da EIA não encontrada!\n"
                "Por favor, crie um arquivo .env contendo 'EIA_API_KEY=sua_chave' "
                "ou defina a variável de ambiente 'EIA_API_KEY'."
            )

    def get_petroleum_spot_prices(self, series: str = None, frequency: str = "daily", length: int = 30) -> pd.DataFrame:
        """
        Busca os preços spot de petróleo e derivados na API v2 da EIA.

        Séries comuns:
        - RBRTE: Europe Brent Spot Price (USD/Barril)
        - EER_EPD2D_PF4_RGC_DPG: U.S. Gulf Coast Ultra-Low Sulfur No 2 Diesel Spot Price (USD/Galão)
        - EER_EPD2F_PF4_Y35NY_DPG: New York Harbor Ultra-Low Sulfur No 2 Diesel Spot Price (USD/Galão)
        """
        endpoint = f"{self.BASE_URL}/petroleum/pri/spt/data/"
        params = {
            "api_key": self.api_key,
            "frequency": frequency,
            "data[0]": "value",
            "sort[0][column]": "period",
            "sort[0][direction]": "desc",
            "offset": 0,
            "length": length
        }

        if series:
            params["facets[series][]"] = series

        response = requests.get(endpoint, params=params)
        response.raise_for_status()

        data = response.json()
        if "response" in data and "data" in data["response"]:
            df = pd.DataFrame(data["response"]["data"])
            return df
        return pd.DataFrame()

    def get_brent_prices(self, length: int = 30) -> pd.DataFrame:
        """Busca cotações recentes do Petróleo Brent (USD por barril)."""
        df = self.get_petroleum_spot_prices(series="RBRTE", length=length)
        if not df.empty:
            df["product_name"] = "Brent Crude Oil"
            df["unit"] = "USD/Barril"
        return df

    def get_us_diesel_prices(self, region: str = "gulf_coast", length: int = 30) -> pd.DataFrame:
        """
        Busca cotações recentes do Diesel (Ultra-Low Sulfur No 2 Diesel) nos EUA (USD por galão).
        Regiões disponíveis: 'gulf_coast', 'ny_harbor'.
        """
        series_map = {
            "gulf_coast": "EER_EPD2D_PF4_RGC_DPG",
            "ny_harbor": "EER_EPD2F_PF4_Y35NY_DPG"
        }
        series = series_map.get(region, "EER_EPD2D_PF4_RGC_DPG")
        df = self.get_petroleum_spot_prices(series=series, length=length)
        if not df.empty:
            df["product_name"] = f"US Diesel ({region.replace('_', ' ').title()})"
            df["unit"] = "USD/Galão"
        return df
