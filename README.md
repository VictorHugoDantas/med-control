# MedControl CLI

[![CI/CD Pipeline](https://github.com/VictorHugoDantas/med-control/actions/workflows/ci.yml/badge.svg)](https://github.com/VictorHugoDantas/med-control/actions)

## Por que o MedControl existe?

Cuidar da própria saúde ou de quem a gente ama já exige muita energia. O controle de horários e dosagens de medicamentos não deveria ser mais um motivo de estresse. 

O esquecimento ou a confusão com remédios é um problema real que afeta a independência de idosos e sobrecarrega a rotina de cuidadores e familiares. O **MedControl** nasceu para ser uma ferramenta de alívio: um lugar simples, rápido e seguro para registrar o que precisa ser tomado e a que horas. Sem telas complexas, direto ao ponto.

## Objetivo

Através de um menu interativo no seu terminal, você pode:
- **Cadastrar:** Adicionar o nome do remédio, a dose e o horário.
- **Consultar:** Ver a lista completa de tudo que está ativo no tratamento.
- **Remover:** Apagar um remédio quando o tratamento acabar.

*(Tudo fica salvo automaticamente no seu computador, você não perde nada ao fechar o programa).*

---

## Instalação

Você só precisa ter o Python instalado. Siga estes passos simples:

**1. Baixe o projeto:**
```bash
git clone https://github.com/VictorHugoDantas/med-control.git
cd med-control
```

**2. Configure as variáveis:**
```bash
cp .env.example .env
```
Preencha o `.env` com as chaves do Supabase e uma senha para o Postgres.

**3. Rode sem Docker:**
```bash
pip install -r requirements.txt
python src/main.py
```

## Docker

Build da imagem:
```bash
docker build --build-arg VERSION=$(cat VERSION) -t med-control:$(cat VERSION) .
```

Subir a aplicação com Postgres e Redis:
```bash
docker compose up -d db cache
docker compose run --rm app
```

Os medicamentos ficam salvos no volume `app_data`, então não se perdem ao recriar o container.

Usar a imagem publicada no GHCR:
```bash
docker run -it --rm --env-file .env ghcr.io/victorhugodantas/med-control:producao
```

## CI/CD

Pipeline com testes, publicação da imagem no GHCR, deploy em homologação e produção (simulados) e rollback. Detalhes de secrets, versionamento e da simulação de rollback em [docs/DEPLOY.md](docs/DEPLOY.md).

## 👥 Integrantes do Projeto
* Victor Hugo Dantas
* Pedro da Silva Andrade
* Mateus Volkmer Amaral