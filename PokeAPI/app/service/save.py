import httpx
from fastapi import HTTPException, UploadFile

from ..config import settings


async def get_save_info(file: UploadFile):
    callback_url = settings.poke_parser_url
    if not callback_url:
        raise HTTPException(status_code=404, detail='callback_url not defined')
    file_content = await file.read()
    async with httpx.AsyncClient() as client:
        # Passa uma tupla com (nome_do_arquivo, bytes_do_arquivo)
        response = await client.post(
            callback_url, files={'file': (file.filename, file_content)}
        )
        response.raise_for_status()
    return response.json()
