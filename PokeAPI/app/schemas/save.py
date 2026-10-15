from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SavePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    save_name: str
    file_name: str | None
    trainer_name: str
    game_name: str
    nr_pokemons: int
    created_at: datetime
    updated_at: datetime


class SaveUpdate(BaseModel):
    save_name: str
