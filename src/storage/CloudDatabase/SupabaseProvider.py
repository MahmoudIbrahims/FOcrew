from supabase import create_client, Client
from typing import Optional



def get_supabase_client(
    url: str,
    key: str,
) -> Client:
    
    return create_client(url, key)


def get_file_record_from_supabase(
    supabase_client: Client,
    file_id: str
) -> Optional[dict]:
    
    response = supabase_client.table('files').select('*').eq('file_id', file_id).execute()

    if response.data:
        return response.data[0]
    else:
        return None