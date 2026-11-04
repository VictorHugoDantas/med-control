# Deploy, versionamento e rollback

## Fluxo do pipeline

O arquivo `.github/workflows/ci.yml` roda em toda push na `main`, em PRs e em tags `vX.Y.Z`.

| Job | Quando roda | O que faz |
|-----|-------------|-----------|
| `build-and-test` | sempre | ruff + pytest. Em tag, confere se a tag bate com o arquivo `VERSION` |
| `publish-image` | push na main ou tag | build da imagem e push para o GHCR |
| `deploy-homologacao` | push na main ou tag | sobe o container, roda o smoke test e marca a imagem como `homologacao` |
| `deploy-producao` | só em tag | promove a versão para `producao`, roda o smoke test e faz rollback automático se falhar |
| `release` | só em tag | cria a release no GitHub com as notas geradas |

O ambiente de homologação/produção é simulado: o "servidor" é o próprio runner do GitHub Actions, e a versão em produção é a que está com a tag `producao` no registry. O smoke test (`scripts/smoke_test.sh`) sobe o container, manda a opção `5` (Sair) para o menu e verifica se o app respondeu.

## Segredos

Nada de senha ou chave fica no código. O `.env` está no `.gitignore` e o repositório só tem o `.env.example`.

No GitHub, em **Settings > Environments**, criar os ambientes `homologacao` e `producao` e cadastrar em cada um:

| Secret | Uso |
|--------|-----|
| `SUPABASE_URL` | URL do projeto no Supabase |
| `SUPABASE_ANON_KEY` | chave do Supabase |

O login no GHCR usa o `GITHUB_TOKEN` que o Actions já fornece, então não precisa cadastrar nada para o registry. No ambiente `producao` dá para ativar "Required reviewers" para exigir aprovação antes do deploy.

Variável opcional (Settings > Environments > producao > Variables):

| Variable | Uso |
|----------|-----|
| `SIMULAR_FALHA` | se `true`, o smoke test de produção falha de propósito (usado para testar o rollback) |

## Versionamento semântico

A versão fica no arquivo `VERSION` e segue `MAJOR.MINOR.PATCH`:

- **PATCH** (1.0.0 -> 1.0.1): correção de bug
- **MINOR** (1.0.1 -> 1.1.0): funcionalidade nova sem quebrar nada
- **MAJOR** (1.1.0 -> 2.0.0): mudança incompatível

Para lançar uma versão:

```bash
echo 1.1.0 > VERSION
git commit -am "release 1.1.0"
git tag v1.1.0
git push origin main --tags
```

Cada tag gera estas tags de imagem no GHCR (`ghcr.io/victorhugodantas/med-control`):

| Tag | Exemplo | Muda? |
|-----|---------|-------|
| `X.Y.Z` | `1.1.0` | nunca, é fixa |
| `X.Y` | `1.1` | aponta para o último patch |
| `X` | `1` | aponta para o último minor |
| `sha-xxxxxxx` | `sha-3f2a1bc` | fixa, uma por commit |
| `homologacao` | | última versão que passou em homologação |
| `producao` | | versão que está "rodando" em produção |
| `producao-anterior` | | versão de antes do último deploy |

Se a tag do git não bater com o `VERSION`, o pipeline para no primeiro job.

## Rollback

Existem dois jeitos.

### 1. Automático

No `deploy-producao`, antes de promover a nova versão, o pipeline copia a tag `producao` atual para `producao-anterior`. Se o smoke test falhar, o passo "Rollback automático" aponta `producao` de volta para `producao-anterior`. O job fica vermelho (a versão nova não entrou) e o resumo da execução mostra para qual versão voltou.

### 2. Manual

Em **Actions > Rollback Manual > Run workflow**, informar a versão (ex: `1.0.0`). O workflow confere se a imagem existe no registry, aponta `producao` para ela e roda o smoke test.

Também dá para fazer na mão, de qualquer máquina com acesso ao registry:

```bash
docker buildx imagetools create -t ghcr.io/victorhugodantas/med-control:producao ghcr.io/victorhugodantas/med-control:1.0.0
```

## Simulação do rollback

Passo a passo do teste feito para validar o fluxo:

1. **Versão estável.** Com `VERSION` em `1.0.0`, criar e enviar a tag `v1.0.0`. O pipeline passa por todos os jobs e `producao` passa a apontar para `1.0.0`.
2. **Forçar a falha.** Em Settings > Environments > producao, criar a variável `SIMULAR_FALHA=true`.
3. **Versão com problema.** Mudar `VERSION` para `1.1.0`, commitar, criar e enviar a tag `v1.1.0`.
4. **Resultado.** Homologação passa (a variável só existe em produção). Em `deploy-producao` o smoke test falha, o passo "Rollback automático" roda e o resumo mostra:
   ```
   Rollback executado
   Versão v1.1.0 falhou. Produção voltou para 1.0.0.
   ```
   Para conferir:
   ```bash
   docker pull ghcr.io/victorhugodantas/med-control:producao
   docker inspect --format '{{ index .Config.Labels "org.opencontainers.image.version" }}' ghcr.io/victorhugodantas/med-control:producao
   ```
   Saída esperada: `1.0.0`.
5. **Corrigir.** Apagar a variável `SIMULAR_FALHA`, lançar `v1.1.1` e o deploy segue normal.
6. **Rollback manual.** Rodar o workflow "Rollback Manual" com `versao = 1.0.0` e conferir de novo com o comando do passo 4.

Os prints de cada execução ficam na aba Actions do repositório.
