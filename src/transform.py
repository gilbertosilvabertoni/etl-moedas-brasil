import pandas as pd
from datetime import datetime
import os

def transformar(caminho_raw: str) -> pd.DataFrame:
    """
    Lê o CSV bruto e aplica limpeza e transformações.
    Retorna um DataFrame tratado.
    """
    df = pd.read_csv(caminho_raw)

    # Remove linhas com qualquer valor ausente
    df = df.dropna()
   
    # Garante tipos numéricos corretos
    colunas_numericas = ["high", "low", "bid", "ask", "pct_change"]
    df[colunas_numericas] = df[colunas_numericas].apply(pd.to_numeric,errors="coerce")
   
    # Remove linhas que viraram NaN após a conversão
    df = df.dropna(subset=colunas_numericas)

    # Coluna calculada — spread entre compra e venda
    df["spread"] = (df["ask"] - df["bid"]).round(6)

    # Padroniza o nome da data e converte para datetime
    df["coletado_em"] = pd.to_datetime(df["coletado_em"])

    # Ordena por código da moeda
    df = df.sort_values("code").reset_index(drop=True)

    return df

def transformar_pipeline() ->None:
    """
    Orquestra a transformação: lê o bruto de hoje e salva o processado.
    """
    hoje = datetime.today().strftime("%Y-%m-%d")
    caminho_raw = f"data/raw/cotacoes_raw_{hoje}.csv"

    if not os.path.exists(caminho_raw):
        raise FileNotFoundError(f"Arquivo bruto não encontrado: {caminho_raw}")
    
    print(f"Transformando: {caminho_raw}")
    df = transformar(caminho_raw)

    os.makedirs("data/processed", exist_ok=True)
    caminho_out = f"data/processed/cotacoes_{hoje}.csv"

    df.to_csv(caminho_out, index=False, encoding="utf-8")

    print(f"Arquivo salvo em: {caminho_out}")
    print(f"Total de registros: {len(df)}")
    print(df.to_string(index=False))
    
    
if __name__ == "__main__":
    transformar_pipeline()

  
