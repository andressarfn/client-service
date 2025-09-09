# client-service
## Como executar

Este serviço roda em um container Docker. Para iniciar, utilize:

```bash

docker compose up --build

```

Ou, para facilitar o processo, utilize o comando abaixo se possuir o `Makefile` configurado:

```bash
make start-containers
```

## Variáveis de ambiente

As variáveis de ambiente necessárias para o funcionamento do serviço estão listadas no arquivo `env.example`.
Utilize esse arquivo como base para configurar o seu próprio `.env`. Utilize o  o `Makefile` configurado:


```bash
make create-env
```

Adapte conforme necessário para seu ambiente.

## Requisitos

- Docker instalado
- Python 3.12
- Make (opcional, para uso dos comandos automatizados)
