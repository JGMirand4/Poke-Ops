using PKHeX.Core;

var builder = WebApplication.CreateBuilder(args);

var app = builder.Build();

app.MapPost("/parse", (byte[] saveBytes) =>
{
    if (!SaveUtil.TryGetSaveFile(saveBytes.AsMemory(), out var sav, string.Empty))
        return Results.BadRequest("Save inválido");

    var party = sav.PartyData.Where(p => p.Species != 0)
        .Select(p => new { p.Nickname, p.Species, p.CurrentLevel, p.IsShiny });

    return Results.Ok(new { trainer = sav.OT, game = sav.Version.ToString(), party });
});

app.Run();