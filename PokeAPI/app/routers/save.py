from typing import Annotated
from sqlmodel import select, Session
from ..models.save import Save, SaveUpdate
from ..models.pokemon import Pokemon, Location, Species
from ..service.save import get_save_info
from fastapi import UploadFile, Query, HTTPException, Form, APIRouter, UploadFile, Depends
from typing import Annotated
from ..dependencies import get_session

router = APIRouter(
    prefix="/save",
    tags=["Save"],
    responses={404: {"description": "Not found"}},
)

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/")
def read_saves(session: SessionDep,
               offset: int = 0,
               limit: Annotated[int, Query(le=10)] = 5) -> list[Save]:
    saves = session.exec(select(Save).offset(offset).limit(limit)).all()
    return saves

@router.get("/{save_id}")
def read_save(save_id: int, session: SessionDep) -> Save:
    save = session.get(Save, save_id)
    if not save:
        raise HTTPException(status_code=404, detail="Save not found")
    return save

@router.post("/", response_model=Save)
async def create_save(file: UploadFile, session: SessionDep, save_name: str = Form(...)):
    dados_parser = await get_save_info(file)
    
    # Extrai as informações do JSON retornado pelo parser
    trainer = dados_parser.get("trainer", {})
    party = dados_parser.get("party", [])
    boxes = dados_parser.get("boxes", [])
    
    save_db = Save(
        save_name=save_name,
        file_name=file.filename,
        trainer_name=trainer.get("otName"), 
        game_name=trainer.get("gameVersion")
    )
    # Salva no banco corretamente
    session.add(save_db)
    session.commit()
    session.refresh(save_db)
        
    ################
    # 2º PASSO: Salva os Pokémons usando o ID do Save
    if party:
        for poke in party:
            # Usa a classe Pokemon, passando o save_id gerado acima
            poke_db = Pokemon(**poke, save_id=save_db.id)
            session.add(poke_db)
            location_db = Location(
                            party=True,
                            slot_number=poke.get("slotNumber")
                        )
            
        # Faz o commit de TODOS os pokémons de uma vez (mais rápido)
        session.commit()
        nr_pokemon = len(party)
    else:
        print("Party vazia")
    
    for box in boxes:
        nr_box = box.get("boxNumber")
        pokemons_box = box.get("pokemon", [])
        nr_pokemon += len(pokemons_box)
        for poke in pokemons_box:
            location_db = Location(
                party=False,
                nr_box=nr_box,
                slot_number=poke.get("slotNumber")
            )
            session.add(location_db)
            session.flush()  # gera location_db.id sem fechar a transação
            
            name =  session.exec(select(Species).where(Species.species_id==poke.get("speciesId"))).first()
            
            print(name)
            poke_db = Pokemon(
                **poke,
                save_id=save_db.id,
                location_id=location_db.id
            )
            session.add(poke_db)
    
    session.commit()
    save_db.nr_pokemons = nr_pokemon
    return Save.model_validate(save_db)

@router.delete("/")
def delete_save(save_id: int, session: SessionDep):
    save = session.get(Save, save_id)
    if not save:
        raise HTTPException(status_code=404, detail="Save not found")
    session.delete(save)
    session.commit()
    return {"ok": True}

@router.patch("/")
def update_save(save_id: int, save: SaveUpdate, session: SessionDep):
    save_db = session.get(Save, save_id)
    if not save_db:
            raise HTTPException(status_code=404, detail="Save not found")
    save_data = save.model_dump(exclude_unset=True)
    save_db.sqlmodel_update(save_data)
    
    # Salva no banco corretamente
    session.add(save_db)
    session.commit()
    session.refresh(save_db)
    return save_db