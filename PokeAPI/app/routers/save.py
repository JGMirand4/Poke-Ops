from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Query,
    UploadFile,
)
from sqlmodel import Session, select

from ..dependencies import get_session
from ..models import Location, Pokemon, Save, Species
from ..schemas.pokemon import PokemonJson
from ..schemas.save import SavePublic, SaveUpdate
from ..service.save import get_save_info

router = APIRouter(
    prefix='/save',
    tags=['Save'],
    responses={404: {'description': 'Not found'}},
)

SessionDep = Annotated[Session, Depends(get_session)]


@router.get('/')
def read_saves(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=10)] = 5,
) -> list[SavePublic]:
    saves = session.exec(select(Save).offset(offset).limit(limit)).all()
    return saves


@router.get('/{save_id}')
def read_save(save_id: int, session: SessionDep) -> SavePublic:
    save = session.get(Save, save_id)
    if not save:
        raise HTTPException(status_code=404, detail='Save not found')
    return save


@router.post('/', response_model=SavePublic)
async def create_save(
    file: UploadFile, session: SessionDep, save_name: str = Form(...)
):
    dados_parser = await get_save_info(file)
    # Extrai as informações do JSON retornado pelo parser
    trainer = dados_parser.get('trainer', {})
    party = dados_parser.get('party', [])
    boxes = dados_parser.get('boxes', [])
    save_db = Save(
        save_name=save_name,
        file_name=file.filename,
        trainer_name=trainer.get('otName'),
        game_name=trainer.get('gameVersion'),
    )
    session.add(save_db)
    session.flush()  # gera save_db.id sem fechar a transação

    # Party e boxes viram uma lista única de (pokémon, localização)
    entries = [
        (poke, Location(party=True, slot_number=poke.get('slotNumber')))
        for poke in party
    ]
    for box in boxes:
        for poke in box.get('pokemon', []):
            location = Location(
                party=False,
                nr_box=box.get('boxNumber'),
                slot_number=poke.get('slotNumber'),
            )
            entries.append((poke, location))

    for poke, location_db in entries:
        session.add(location_db)
        session.flush()  # gera location_db.id
        poke_data = PokemonJson.model_validate(poke)
        species = session.get(Species, poke_data.species_id)
        session.add(
            Pokemon(
                **poke_data.model_dump(),
                save_id=save_db.id,
                location_id=location_db.id,
                species_name=species.name if species else None,
            )
        )

    save_db.nr_pokemons = len(entries)
    session.commit()
    session.refresh(save_db)
    return save_db


@router.delete('/')
def delete_save(save_id: int, session: SessionDep):
    save = session.get(Save, save_id)
    if not save:
        raise HTTPException(status_code=404, detail='Save not found')
    session.delete(save)
    session.commit()
    return {'ok': True}


@router.patch('/')
def update_save(
    save_id: int, save: SaveUpdate, session: SessionDep
) -> SavePublic:
    save_db = session.get(Save, save_id)
    if not save_db:
        raise HTTPException(status_code=404, detail='Save not found')
    save_data = save.model_dump(exclude_unset=True)
    for key, value in save_data.items():
        setattr(save_db, key, value)
    # Salva no banco corretamente
    session.add(save_db)
    session.commit()
    session.refresh(save_db)
    return save_db
