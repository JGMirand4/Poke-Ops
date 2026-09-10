using PKHeX.Core;

byte[] data = File.ReadAllBytes("/Users/joaogui/Library/Application Support/Astris/bis/user/save/0000000000000001/0/savedata.bin");

// byte[] data = File.ReadAllBytes("/Users/joaogui/Library/Application Support/Azahar/sdmc/Nintendo 3DS/00000000000000000000000000000000/00000000000000000000000000000000/title/00040000/00055d00/data/00000001/main");

if (!SaveUtil.TryGetSaveFile(data.AsMemory(), out var sav, string.Empty))
{
    Console.WriteLine("Save inválido ou não suportado.");
    return;
}

Console.WriteLine($"Jogo: {sav.Version}");
Console.WriteLine($"Treinador: {sav.OT}");
Console.WriteLine($"Tempo de jogo: {sav.PlayTimeString}");

// Time atual
foreach (PKM pkm in sav.PartyData)
{
    if (pkm.Species == 0) continue; // slot vazio
    Console.WriteLine($"{pkm.Nickname} (espécie #{pkm.Species}) - Nv.{pkm.CurrentLevel} - Shiny: {pkm.IsShiny}");
}

// Todas as boxes
foreach (PKM pkm in sav.BoxData)
{
    if (pkm.Species == 0) continue;
    Console.WriteLine($"Box: {pkm.Nickname} - espécie #{pkm.Species}");
}