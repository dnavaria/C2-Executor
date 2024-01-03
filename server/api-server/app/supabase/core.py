from config import Settings
from supabase import create_client, Client

supabase: Client = create_client(Settings.SUPABASE_URL, Settings.SUPABASE_KEY)
