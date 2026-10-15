from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session

from .dependencies import get_session
from .routers import pokemon, save

app = FastAPI()

app.include_router(pokemon.router)
app.include_router(save.router)

SessionDep = Annotated[Session, Depends(get_session)]
