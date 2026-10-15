from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class PokemonJson(BaseModel):
    # Traduz tudo de/para camelCase automaticamente (JSON do PokeParser)
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    species_id: int | None = None
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


class LocationPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    party: bool
    nr_box: int | None
    slot_number: int | None


class SpeciesPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    species_id: int
    name: str | None


class PokemonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    species_name: str | None = None
    nickname: str | None = None
    location: LocationPublic | None = None
