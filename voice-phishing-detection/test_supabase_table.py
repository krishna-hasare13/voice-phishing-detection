
from supabase import create_client, Client
import os

SUPABASE_URL = "https://gjwcexivvjhunbdnhepx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdqd2NleGl2dmpodW5iZG5oZXB4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1OTUwMTQ0OSwiZXhwIjoyMDc1MDc3NDQ5fQ.P4nz5LMH1V3qunT-_lnF_65BvqQJsZ0xiBgVGj_tMXQ"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    # Check if 'chunks' table exists by trying a select
    try:
        res = supabase.table("chunks").select("*").limit(1).execute()
        print(f"✅ 'chunks' table exists and is accessible. Rows found: {len(res.data)}")
    except Exception as table_err:
        print(f"❌ 'chunks' table check failed: {table_err}")
except Exception as e:
    print(f"❌ Supabase connection failed: {e}")
