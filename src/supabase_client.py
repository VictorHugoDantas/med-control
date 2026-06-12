import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega as chaves do arquivo .env
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_KEY")

# Cria a conexão oficial
supabase: Client = create_client(url, key)