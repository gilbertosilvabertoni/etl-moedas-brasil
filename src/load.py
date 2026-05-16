import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

def criar_engine():
    """
    Cria a conexão com o PostgreSQL via SQLAlchemy.
    """
    url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    return create_engine(url)


def carregar(df: pd.DataFrame) -> None:
    """
    Insere o DataFrame na tabela cotacoes do PostgreSQL.
    """
    engine = criar_engine()

    df.to_sql(name="cotacoes", con=engine, if_exists="append", index=False)

    print(f"Registros inseridos: {len(df)}")


def carregar_pipeline() -> None:
    """
    Orquestra o carregamento: lê o CSV processado e insere no banco.
    """
    hoje = datetime.today().strftime("%Y-%m-%d")
    caminho = f"data/processed/cotacoes_{hoje}.csv"


    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
    
    print(f"Carregando: {caminho}")
    df = pd.read_csv(caminho)

    carregar(df)
    print("Carregamento concluído.")

if __name__ == "__main__":
    carregar_pipeline()


