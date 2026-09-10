import httpx
from typing import Annotated
from fastapi import UploadFile, Depends
from sqlmodel import Session

from ..config import settings
from ..dependencies import get_session
from ..models.pokemon import Species

async def get_save_info(file: UploadFile):
    callback_url = settings.poke_parser_url
        
    file_content = await file.read()
    
    async with httpx.AsyncClient() as client: 
        # AQUI É A MUDANÇA: Passe uma tupla com (nome_do_arquivo, bytes_do_arquivo)
        response = await client.post(
            callback_url, 
            files={"file": (file.filename, file_content)}
        )
        response.raise_for_status()
    return response.json()

async def seed_all_species(session: Session):
    callback_url = settings.poke_api_ofc_url
    total_pokemons = await get_count_species()
    for species_id in range(1, total_pokemons + 1):
        async with httpx.AsyncClient() as client:
            response = await client.get(callback_url + f'{species_id}/')
            response.raise_for_status()
            if response.status_code == 200:
                name = response.json().get("name")
                print(name)
                session.add(Species(species_id=species_id, name=name))
            session.commit()
            
            
async def get_count_species() -> int:
    callback_url = settings.poke_api_ofc_url
    async with httpx.AsyncClient() as client:
        response = await client.get(callback_url + f'?offset=1&limit=1')
        response.raise_for_status()
        count = response.json().get("count")
    return count
    
    
    