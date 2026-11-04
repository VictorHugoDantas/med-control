#!/usr/bin/env bash
# Sobe o container, escolhe a opção "5. Sair" do menu e confere se o app respondeu.
set -euo pipefail

IMAGE="$1"

if [ "${SIMULAR_FALHA:-false}" = "true" ]; then
  echo "SIMULAR_FALHA=true -> forçando falha do smoke test"
  exit 1
fi

SAIDA=$(printf '5\n' | docker run -i --rm \
  -e SUPABASE_URL \
  -e SUPABASE_ANON_KEY \
  "$IMAGE")

echo "$SAIDA"

if echo "$SAIDA" | grep -q "Saindo do MedControl"; then
  echo "Smoke test OK"
else
  echo "Smoke test falhou"
  exit 1
fi
