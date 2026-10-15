from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from .base import table_registry


@table_registry.mapped_as_dataclass
class Save:
    __tablename__ = 'saves'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    save_name: Mapped[str] = mapped_column(unique=True)
    trainer_name: Mapped[str]
    game_name: Mapped[str]
    file_name: Mapped[str | None] = mapped_column(default=None)
    nr_pokemons: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
