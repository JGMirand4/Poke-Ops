from fastapi import FastAPI, Depends
from typing import Annotated
from sqlmodel import Session

from .dependencies import create_db_and_tables
from .routers import pokemon, save
from .service.save import seed_all_species
from .dependencies import get_session, engine

app = FastAPI()
app.include_router(pokemon.router)
app.include_router(save.router)

SessionDep = Annotated[Session, Depends(get_session)]

@app.on_event("startup")
async def on_startup():
    create_db_and_tables() 
    with Session(engine) as session:
        await seed_all_species(session)


    
    
    