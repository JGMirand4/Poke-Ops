from fastapi import APIRouter, Depends, Query
from sqlmodel import select, Session
from app.models.pokemon import Pokemon, PokemonList, Species
from typing import Annotated
from app.dependencies import get_session

router = APIRouter(
    prefix="/pokemon",
    tags=["Pokémons"],
    responses={404: {"description": "Not found"}},
)

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/{save_id}", response_model=list[PokemonList])
def read_pokemon(save_id: int, 
                 session: SessionDep,
                 offset: int = 0, 
                 limit: Annotated[int, Query(le=100)] = 100):
    
    pokemons = session.exec(
        select(Pokemon)
        .where(Pokemon.save_id == save_id)
        .offset(offset)
        .limit(limit)
    ).all()
    
    return pokemons

@router.get("/species", response_model=list[Species])
def read_pokemon(session: SessionDep,
                 offset: int = 0, 
                 limit: Annotated[int, Query(le=100)] = 100):
    
    species = session.exec(
        select(Species)
        .offset(offset)
        .limit(limit)
    ).all()
    print(species)
    
    return species