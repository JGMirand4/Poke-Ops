using PKHeX.Core;

namespace PokeOps.Parser;

public static class PokemonMapper
{
    private static readonly string[] AbilityList = GameInfo.GetStrings("en").abilitylist;

    public static PokemonDto Map(PKM pkm, int slotNumber) => new(
        SpeciesId:  pkm.Species,
        Nickname:   pkm.Nickname,
        Level:      pkm.CurrentLevel,
        IsShiny:    pkm.IsShiny,
        Nature:     pkm.Nature.ToString(),
        Ability:    GetAbilityName(pkm.Ability),
        IvHp:       pkm.IV_HP,
        IvAtk:      pkm.IV_ATK,
        IvDef:      pkm.IV_DEF,
        IvSpa:      pkm.IV_SPA,
        IvSpd:      pkm.IV_SPD,
        IvSpe:      pkm.IV_SPE,
        HeldItemId: pkm.HeldItem == 0 ? null : pkm.HeldItem,
        SlotNumber: slotNumber
    );

    private static string GetAbilityName(int id) =>
        id > 0 && id < AbilityList.Length ? AbilityList[id] : string.Empty;
}
