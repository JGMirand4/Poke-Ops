from pydantic import ConfigDict
from pydantic.alias_generators import to_camel
from sqlmodel import Field, Relationship, SQLModel


class Location(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    party: bool
    nr_box: int
    slot_number: int


class Species(SQLModel, table=True):
    species_id: int | None = Field(default=None, primary_key=True)
    name: str | None = None


class PokemonJson(SQLModel):
    # Essa linha faz a mágica: traduz tudo de/para camelCase automaticamente
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    species_id: int | None = Field(index=True)
    nickname: str | None = None
    level: int | None = None
    is_shiny: bool | None = None
    nature: str | None = None
    ability: str | None = None
    iv_hp: int | None = None
    iv_atk: int | None = None
    iv_def: int | None = None
    iv_spa: int | None = None
    iv_spd: int | None = None
    iv_spe: int | None = None
    held_item_id: int | None = None
    slot_number: int | None = None


class Pokemon(PokemonJson, table=True):
    id: int | None = Field(default=None, primary_key=True)
    species_name: str | None = Field(index=True)

    save_id: int = Field(default=None, foreign_key='save.id')
    location_id: int | None = Field(default=None, foreign_key='location.id')

    location: 'Location' = Relationship()


class PokemonList(SQLModel):
    id: int
    species_id: int
    species_name: str | None = None
    nickname: str | None = None
    location: Location | None = None
