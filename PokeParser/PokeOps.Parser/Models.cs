namespace PokeOps.Parser;

public record TrainerDto(string OtName, string GameVersion);

public record PokemonDto(
    int SpeciesId,
    string Nickname,
    int Level,
    bool IsShiny,
    string Nature,
    string Ability,
    int IvHp,
    int IvAtk,
    int IvDef,
    int IvSpa,
    int IvSpd,
    int IvSpe,
    int? HeldItemId,
    int SlotNumber);

public record BoxDto(int BoxNumber, string BoxName, List<PokemonDto> Pokemon);

public record PokedexEntryDto(int SpeciesId, bool Seen, bool Caught);

public record ParseResponse(
    TrainerDto Trainer,
    List<PokemonDto> Party,
    List<BoxDto> Boxes,
    List<PokedexEntryDto> Pokedex);
