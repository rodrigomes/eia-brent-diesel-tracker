# EIA Petroleum Tracker (Brent & US Diesel)

Este repositório fornece uma biblioteca e script em Python para consultar automaticamente as cotações do **Petróleo Brent** e do **Diesel nos Estados Unidos** (Ultra-Low Sulfur Diesel / Heating Oil) utilizando a API v2 oficial da **U.S. Energy Information Administration (EIA)**.

---

## 🚀 Como Configurar

### 1. Obter a Chave de API da EIA
Se ainda não possui, cadastre-se gratuitamente no site oficial:
👉 [https://www.eia.gov/opendata/register.php](https://www.eia.gov/opendata/register.php)

### 2. Configurar a Chave de API
Copie o arquivo `.env.example` para `.env` e insira sua chave:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:
```env
EIA_API_KEY=sua_chave_recebida_por_email
```

> **Nota de Segurança**: O arquivo `.env` está incluído no `.gitignore` para garantir que sua chave privada nunca seja enviada publicamente para o GitHub.

---

## 📦 Instalação das Dependências

Instale as dependências executando:

```bash
pip install -r requirements.txt
```

---

## 💻 Como Executar

Execute o script principal para visualizar as cotações mais recentes:

```bash
python main.py
```

### Exemplo de Código em Python

```python
from eia_client import EIAClient

# Inicializa o cliente (lê a chave do arquivo .env)
client = EIAClient()

# Buscar cotações do Brent
df_brent = client.get_brent_prices(length=10)
print(df_brent[['period', 'value', 'product_name']])

# Buscar cotações do Diesel nos EUA
df_diesel = client.get_us_diesel_prices(region="gulf_coast", length=10)
print(df_diesel[['period', 'value', 'product_name']])
```

---

## 📊 Séries Utilizadas da EIA (v2 API)

* **Petróleo Brent**: `RBRTE` (*Europe Brent Spot Price FOB*, em USD por barril)
* **Diesel EUA (Gulf Coast)**: `EER_EPD2D_PF4_RGC_DPG` (*U.S. Gulf Coast Ultra-Low Sulfur No 2 Diesel Spot Price*, em USD por galão)
* **Diesel EUA (NY Harbor)**: `EER_EPD2F_PF4_Y35NY_DPG` (*New York Harbor Ultra-Low Sulfur No 2 Diesel Spot Price*, em USD por galão)

---

## 🔒 Boas Práticas de Segurança
* **Nunca comite a sua `EIA_API_KEY` diretamente nos arquivos `.py` ou no Git.**
* Utilize sempre o arquivo `.env` ou variáveis de ambiente de sistema.
