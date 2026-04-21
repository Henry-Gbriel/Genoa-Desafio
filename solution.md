# Solution - Pipeline de Coleta de Preços

## Objetivo

Desenvolver um pipeline de coleta de dados de um site de varejo nacional, com execução automatizada, reprocessável e independente de ambiente.

---

## Escolha do site

Foi escolhido o site da Hering por apresentar uma estrutura acessível via requisições HTTP, permitindo uma abordagem inicial mais leve sem necessidade de automação de navegador.

---

## Arquitetura da solução

A solução foi estruturada em três camadas principais:

1. Orquestração (Airflow)
2. Coleta (Python + HTTP)
3. Persistência (PostgreSQL)

O fluxo funciona da seguinte forma:

- O Airflow executa uma DAG
- A task realiza a coleta via HTTP
- Os dados são processados
- O resultado é armazenado no banco

---

## Orquestração com Airflow

Foi utilizado Apache Airflow com LocalExecutor para simplificar a execução local.

Motivos da escolha:

- Permite agendamento flexível
- Facilita reprocessamento
- Mantém histórico de execuções
- Estrutura escalável para futuras DAGs

---

## Containerização com Docker

Toda a solução foi executada em containers Docker, garantindo:

- Ambiente reprodutível
- Isolamento de dependências
- Facilidade de execução em diferentes máquinas
- Padronização do ambiente de desenvolvimento

O Docker Compose foi utilizado para orquestrar os serviços:

- Airflow (webserver e scheduler)
- PostgreSQL

---

## Gerenciamento de dependências com Poetry

Foi utilizado Poetry no desenvolvimento local para:

- Controle de dependências
- Versionamento consistente
- Organização do projeto

Para execução no Docker, as dependências foram exportadas para `requirements.txt`, garantindo builds mais simples e rápidos.

---

## Estratégia de coleta

A coleta foi feita utilizando a biblioteca `httpx`.

Motivos:

- Leve e performática
- Não depende da renderização do front-end
- Mais resiliente a mudanças de layout do que ferramentas baseadas em browser

Nesta etapa, foram coletadas métricas básicas:

- Status da requisição
- Tamanho do HTML

A estrutura permite evolução para parsing completo de produtos e preços.

---

## Persistência

Os dados são armazenados em PostgreSQL.

Características da implementação:

- Criação de tabela idempotente
- Inserção de dados a cada execução
- Registro de timestamp para auditoria

---

## Reprocessamento

O pipeline é reprocessável pois:

- Não depende de estado anterior
- Cada execução gera um novo registro
- Permite análise histórica

---

## Configuração

As configurações foram desacopladas do código via variáveis de ambiente:

- URL do site
- Credenciais do banco
- Configurações de conexão

Essas variáveis são injetadas via Docker Compose.

---

## Robustez

Mesmo sendo uma implementação inicial, foram considerados pontos de robustez:

- Timeout na requisição HTTP
- Separação entre código e configuração
- Estrutura pronta para retries
- Persistência transacional

---

## Limitações

- Coleta ainda não extrai produtos detalhados
- Não há tratamento de erros avançado
- Não há camada de dados (raw/trusted)

---

## Melhorias futuras

- Parsing estruturado de produtos e preços
- Implementação de retries com tenacity
- Logs estruturados com loguru
- Armazenamento em Parquet
- Criação de camadas de dados (raw → curated)
- Monitoramento e alertas
- Uso de filas (SQS/Kafka) para escalabilidade
- Deploy em ambiente cloud 

---

## Conclusão

A solução entrega um pipeline funcional e escalável, com orquestração, coleta e persistência integradas, além de uma base sólida para evolução futura.

Mesmo simples, a arquitetura foi pensada para crescer sem necessidade de grandes refatorações.
