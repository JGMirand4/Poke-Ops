from sqlmodel import Field, SQLModel


class SaveBase(SQLModel):
    file_name: str | None = None


class Save(SaveBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    save_name: str
    trainer_name: str | None
    game_name: str | None = Field(index=True)
    nr_pokemons: int | None


class SaveUpdate(SQLModel):
    save_name: str
