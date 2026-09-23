from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry
from sqlmodel import SQLModel

table_registry = registry()


class SaveBase:
    file_name: Mapped[str] | None = None


@table_registry.mapped_as_dataclass
class Save(SaveBase):
    __tablename__ = 'saves'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    save_name: Mapped[str] = mapped_column(unique=True)
    trainer_name: Mapped[str]
    game_name: Mapped[str]
    nr_pokemons: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
            init=False, server_default=func.now()
        )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now
    )


class SaveUpdate(SQLModel):
    save_name: str
