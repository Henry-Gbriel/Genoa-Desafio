# Genoa Desafio - Pipeline de Coleta de Dados de Varejo

Este projeto implementa um pipeline end-to-end para coleta de dados de um site de varejo nacional (Hering), com orquestração via Apache Airflow, persistência em PostgreSQL e execução containerizada com Docker.

## Tecnologias utilizadas

- Python
- Apache Airflow
- PostgreSQL
- Docker / Docker Compose
- httpx (requisições HTTP)
- psycopg2 (conexão com banco)

## Arquitetura

O pipeline segue um fluxo simples e reprocessável:

1. O Airflow orquestra a execução via DAG
2. Uma task executa uma requisição HTTP no site da Hering
3. São coletadas métricas da resposta (status e tamanho do HTML)
4. Os dados são persistidos no PostgreSQL

## Estrutura do projeto

```
.
├── dags/
│   └── final_pipeline.py
├── app/
├── data/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── pyproject.toml
├── poetry.lock
├── .env
├── README.md
├── solution.md
```

## Como executar

1. Subir os containers:

```bash
docker-compose up --build
```

2. Inicializar o banco do Airflow (primeira execução):

```bash
docker-compose run airflow-webserver airflow db migrate
```

3. Criar usuário do Airflow:

```bash
docker-compose run airflow-webserver airflow users create \
  --username airflow \
  --password airflow \
  --firstname admin \
  --lastname user \
  --role Admin \
  --email admin@email.com
```

4. Acessar o Airflow:

http://localhost:8080

Login:
- user: airflow
- password: airflow

5. Executar o pipeline:

- Ativar o DAG `final_retail_pipeline`
- Clicar em **Trigger DAG**

## Banco de dados

Tabela criada automaticamente:

```sql
CREATE TABLE hering_metrics (
    id SERIAL PRIMARY KEY,
    status_code INT,
    html_size INT,
    collected_at TIMESTAMP DEFAULT NOW()
);
```

Consulta:

```sql
SELECT * FROM hering_metrics;
```

## Configuração

As variáveis de ambiente são definidas no arquivo `.env`:

```env
URL_HERING=https://www.hering.com.br
HOST=postgres
DATABASE=airflow
USER=airflow
PASSWORD=airflow
PORT=5432
```

## Reprocessamento

O pipeline é reprocessável:

- Cada execução gera um novo registro
- Não depende de estado anterior
- Permite análise histórica

## Possíveis melhorias

- Extração de produtos e preços (parsing HTML)
- Implementação de retries (tenacity)
- Logs estruturados (loguru)
- Armazenamento em parquet
- Camadas de dados (raw → curated)
- Monitoramento e alertas
- Deploy em ambiente cloud

## Observações

A solução foi construída com foco em simplicidade, robustez e facilidade de evolução, mantendo uma base sólida para expansão futura.
