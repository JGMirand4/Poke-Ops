from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import table_registry


@table_registry.mapped_as_dataclass
class Location:
    __tablename__ = 'locations'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    party: Mapped[bool]
    slot_number: Mapped[int | None] = mapped_column(default=None)
    nr_box: Mapped[int | None] = mapped_column(default=None)


@table_registry.mapped_as_dataclass
class Species:
    __tablename__ = 'species'

    species_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=False
    )
    name: Mapped[str | None] = mapped_column(default=None)


@table_registry.mapped_as_dataclass
class Pokemon:
    __tablename__ = 'pokemons'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    save_id: Mapped[int] = mapped_column(ForeignKey('saves.id'))
    location_id: Mapped[int | None] = mapped_column(
        ForeignKey('locations.id'), default=None
    )
    species_id: Mapped[int | None] = mapped_column(index=True, default=None)
    species_name: Mapped[str | None] = mapped_column(index=True, default=None)
    nickname: Mapped[str | None] = mapped_column(default=None)
    level: Mapped[int | None] = mapped_column(default=None)
    is_shiny: Mapped[bool | None] = mapped_column(default=None)
    nature: Mapped[str | None] = mapped_column(default=None)
    ability: Mapped[str | None] = mapped_column(default=None)
    iv_hp: Mapped[int | None] = mapped_column(default=None)
    iv_atk: Mapped[int | None] = mapped_column(default=None)
    iv_def: Mapped[int | None] = mapped_column(default=None)
    iv_spa: Mapped[int | None] = mapped_column(default=None)
    iv_spd: Mapped[int | None] = mapped_column(default=None)
    iv_spe: Mapped[int | None] = mapped_column(default=None)
    held_item_id: Mapped[int | None] = mapped_column(default=None)
    slot_number: Mapped[int | None] = mapped_column(default=None)

    location: Mapped[Location | None] = relationship(init=False)
