# ETL Moedas Brasil

Pipeline ETL em Python que coleta cotações de moedas estrangeiras em relação ao Real Brasileiro via API pública, transforma os dados e carrega no PostgreSQL.

## Moedas coletadas

- USD — Dólar Americano
- EUR — Euro
- GBP — Libra Esterlina
- ARS — Peso Argentino
- BTC — Bitcoin

## Tecnologias

- Python 3.14
- pandas
- requests
- SQLAlchemy
- psycopg2
- PostgreSQL
- python-dotenv

## Estrutura do projeto

etl-moedas-brasil/
├── src/
│   ├── extract.py      # Coleta cotações da AwesomeAPI
│   ├── transform.py    # Limpeza e transformação dos dados
│   └── load.py         # Carregamento no PostgreSQL
├── data/
│   ├── raw/            # CSV bruto da API
│   └── processed/      # CSV transformado
├── .env.example        # Modelo de variáveis de ambiente
└── requirements.txt

## Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/gilbertosilvabertoni/etl-moedas-brasil.git
cd etl-moedas-brasil
```

### 2. Crie o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o `.env` com suas credenciais do PostgreSQL.

### 4. Crie o banco de dados

```bash
sudo -u postgres psql -c "CREATE USER etl_user WITH PASSWORD 'sua_senha';"
sudo -u postgres psql -c "CREATE DATABASE etl_moedas OWNER etl_user;"
sudo -u postgres psql -d etl_moedas -U postgres -c "
CREATE TABLE cotacoes (
    id          SERIAL PRIMARY KEY,
    code        VARCHAR(10)    NOT NULL,
    name        VARCHAR(100)   NOT NULL,
    high        NUMERIC(18,6)  NOT NULL,
    low         NUMERIC(18,6)  NOT NULL,
    bid         NUMERIC(18,6)  NOT NULL,
    ask         NUMERIC(18,6)  NOT NULL,
    pct_change  NUMERIC(10,6)  NOT NULL,
    spread      NUMERIC(18,6)  NOT NULL,
    coletado_em TIMESTAMP      NOT NULL,
    inserido_em TIMESTAMP      DEFAULT NOW()
);"
sudo -u postgres psql -d etl_moedas -U postgres -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO etl_user;"
sudo -u postgres psql -d etl_moedas -U postgres -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO etl_user;"
```

### 5. Execute o pipeline

```bash
python src/extract.py
python src/transform.py
python src/load.py
```

## Fonte dos dados

[AwesomeAPI](https://docs.awesomeapi.com.br) — API brasileira gratuita de cotações.