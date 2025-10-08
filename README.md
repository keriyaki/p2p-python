# P2P Python + MySQL (MVC)

Este projeto implementa um esqueleto de um sistema P2P estilo torrent com:
- Autenticação via JWT
- Níveis de acesso (SuperAdmin, Admin, Gerente, Supervisor, etc.) com capacidade de adicionar novos
- Catálogo de arquivos com palavras‑chave (FULLTEXT) e respeito ao nível de acesso
- Cliente P2P que faz seed/download via libtorrent e reporta estatísticas (downloads, uploads e ratio por usuário)
- Visualização básica de imagens/PDF/Vídeos (abrindo localmente após download)

> **Stack**: Python 3.11+, FastAPI, SQLAlchemy, MySQL 8, libtorrent (python-libtorrent), Uvicorn

## Subir MySQL

```bash
docker compose up -d mysql
```

Crie um arquivo `.env` a partir de `.env.example` e ajuste as variáveis.

## Instalar dependências

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Rodar o servidor API (MVC = Models + Controllers + Views-API)

```bash
uvicorn server.app:app --reload --host 0.0.0.0 --port 8000
```

Acesse docs: http://localhost:8000/docs

## Rodar o cliente CLI (View-CLI)

```bash
python client/cli.py login --username admin --password admin123
python client/cli.py list
python client/cli.py search --q "relatorio segurança"
python client/cli.py download --file-id 1 --dest ./downloads
python client/cli.py seed --path ./downloads/minha_coisa.mp4
```

> **Nota sobre libtorrent**: Em algumas plataformas o pacote é `python-libtorrent` ou `libtorrent`. No Windows, procure wheel compatível. No Linux, instale dependências do sistema (libboost, etc.).

## Fluxo de papéis e permissões

- **SuperAdmin**: gerencia níveis de acesso, configurações, banimentos, ratio default; pode excluir do catálogo.
- **Admin**: gerencia usuários, aprova uploads, ajusta ratio de usuários.
- **Gerente/Supervisor/…**: níveis customizáveis; permissões herdáveis.

## Índice e busca

- FULLTEXT (MySQL) em: título, descrição, tags
- Filtro por `min_role_weight` do arquivo vs. `role_weight` do usuário

## Estatísticas e Ratio

- Tabela `user_stats`: bytes_up, bytes_down, ratio calculado server‑side
- Cliente reporta eventos (piece finished, torrent finished, upload tick) ao servidor

---
```