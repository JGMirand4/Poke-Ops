from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from app.dependencies import get_session
from app.models.pokemon import Pokemon, PokemonResponse, Species

router = APIRouter(
    prefix='/pokemon',
    tags=['Pokémons'],
    responses={404: {'description': 'Not found'}},
)

SessionDep = Annotated[Session, Depends(get_session)]


@router.get('/{save_id}', response_model=list[PokemonResponse])
def read_pokemon(
    save_id: int,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):

    pokemons = session.exec(
        select(Pokemon)
        .where(Pokemon.save_id == save_id)
        .offset(offset)
        .limit(limit)
    ).all()
    return pokemons


@router.get('/species', response_model=list[Species])
def list_species(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    species = session.exec(select(Species).offset(offset).limit(limit)).all()
    print(species)
    return species
