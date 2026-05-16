import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

# Moedas configuradas no .env - padrão se não encontrar
MOEDAS_RAW =  os.getenv("MOEDAS", "USD, EUR, GBP, ARS, BTC")
MOEDAS = [m.strip() for m in MOEDAS_RAW.split(",")]

# Monta os pares moeda-BRL para a API
# Exemplo: ["USD", "EUR"] → "USD-BRL,EUR-BRL"
PARES = ",".join([f"{m}-BRL"for m in MOEDAS])

URL_BASE = "https://economia.awesomeapi.com.br/json/last"

def buscar_cotacoes() -> pd.DataFrame:
    """
    Busca cotações das moedas configuradas na API AwesomeAPI.
    Retorna um DataFrame com os dados brutos.
    """
    url = f"{URL_BASE}/{PARES}"

    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Erro ao buscar cotações: {exc}") from exc
    
    dados = resposta.json()

    if not dados:
        raise RuntimeError("A API retornou resposta vazia.")

    registros = []
    for chave, valores in dados.items():
        registros.append({
            "code":        valores["code"],
            "name":        valores["name"],
            "high":        float(valores["high"]),
            "low":         float(valores["low"]),
            "bid":         float(valores["bid"]),
            "ask":         float(valores["ask"]),
            "pct_change":  float(valores["pctChange"]),
            "coletado_em": valores["create_date"],

        })

    return pd.DataFrame(registros)

def extrair() -> None:
    """
    Orquestra a extração e salva o CSV bruto.
    """
    print("Buscando cotações na API...")
    df = buscar_cotacoes()
        

    os.makedirs("data/raw", exist_ok=True)

    hoje = datetime.today().strftime("%Y-%m-%d")
    caminho = f"data/raw/cotacoes_raw_{hoje}.csv"

    df.to_csv(caminho, index=False, encoding="utf-8")
    print(f"Arquivo salvo em: {caminho}")
    print(f"Total de registros: {len(df)}")
    print(df.to_string(index=False))


if __name__ == "__main__":
    extrair()