from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session

from .dependencies import create_db_and_tables, engine, get_session
from .routers import pokemon, save
from .service.save import seed_all_species

app = FastAPI()
app.include_router(pokemon.router)
app.include_router(save.router)

SessionDep = Annotated[Session, Depends(get_session)]


@app.on_event('startup')
async def on_startup():
    create_db_and_tables()
    with Session(engine) as session:
        await seed_all_species(session)
