import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega as chaves do arquivo .env (localmente) ou das variaveis de ambiente (container/CI)
load_dotenv()

_client: Client | None = None


def get_supabase() -> Client:
    global _client
    if _client is None:
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_ANON_KEY")
        if not url or not key:
            raise RuntimeError("SUPABASE_URL e SUPABASE_ANON_KEY precisam estar definidas.")
        _client = create_client(url, key)
    return _client
