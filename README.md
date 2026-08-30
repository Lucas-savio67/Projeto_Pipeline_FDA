# FDA Drug Pipeline

Pipeline em Python para extração, transformação e carga (ETL) de dados públicos da API [openFDA](https://open.fda.gov/) (endpoint `drug/event`), com armazenamento intermediário no Amazon S3 e carga final em MySQL.

## Visão geral

O pipeline é organizado seguindo conceitos de **Clean Architecture**, separando claramente as etapas de extração, transformação e análise exploratória (EDA). A configuração de cada fonte de dados é centralizada em um dicionário, permitindo adicionar novas fontes sem alterar a lógica principal.

Fluxo geral:

```
openFDA API → S3 (JSON) → Extração → Transformação → Tabelas limpas → EDA → MySQL
```

## Funcionalidades

- **Ingestão de dados** a partir da API openFDA, com autenticação via `api_key` (variável de ambiente carregada com `dotenv`)
- **Paginação via cursor**, seguindo o header `Link` retornado pela API (`search_after`)
- **Limite configurável de páginas** (`max_paginas`) por fonte de dados
- **Armazenamento em S3**, com extração via `boto3` (`get_object` + paginação com `list_objects_v2`)
- **Tratamento de erros na extração** com uma classe própria (`ExtractionErrors`), capturada no orquestrador: em caso de falha, o erro é logado e o pipeline segue para a próxima chave
- **Transformação orientada a metadados**: cada API tem, no dicionário `regras_limpeza`, informações como tipo (`lista`, etc.), a parte essencial do JSON (`results`) e as subtabelas a serem extraídas (via `record_path`/`meta`, ex.: `reaction`, `drug`)
- **Resiliência na criação de tabelas**: se uma subtabela falhar ao estruturar, o erro é logado e o pipeline continua estruturando as demais, retornando as que tiveram sucesso
- **Análise exploratória (EDA)** automática das tabelas geradas com `pandas`, com o resultado salvo em JSON
- **Dockerizado**: imagem baseada em `python:3.12-slim`, com `.dockerignore`; a imagem do MySQL fica a cargo do `docker-compose`

## Arquitetura

O pipeline conta com dois níveis de orquestração:

- **Orquestrador geral**: coordena as macro-etapas (extração → transformação → EDA → carga)
- **Orquestrador de transformação**: chama os métodos menores responsáveis por transformar cada API

## Configuração

1. Copie o arquivo de variáveis de ambiente de exemplo (se houver) e preencha:
   ```
   FDA_API_KEY=sua_chave_aqui
   AWS_ACCESS_KEY_ID=...
   AWS_SECRET_ACCESS_KEY=...
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure as fontes de dados no dicionário de configuração (endpoint, `max_paginas`, regras de limpeza).

## Executando com Docker

```bash
docker build -t fda-pipeline .
docker-compose up
```

## Roadmap / Próximos passos

- [ ] Migrar carga final para MySQL via SQLAlchemy
- [ ] Estudar e implementar testes de integração
- [ ] Avaliar versionamento dos JSONs de EDA a cada execução
- [ ] Revisitar tratamento de atomicidade entre subtabelas quando o pipeline passar a rodar de forma automatizada
- [ ] Detectar dinamicamente outros formatos de conteúdo além de lista (envelope, registro único, mapa, aninhado)
- [ ] Avaliar uso de Spark para resolver gargalo de performance no `json.dumps` durante a ingestão

## Status

Projeto em desenvolvimento ativo.