// PokeOps.Parser — Microserviço de parsing de saves Pokémon
//
// Como rodar:
//   dotnet run --project PokeOps.Parser
//
// Endpoints:
//   POST http://localhost:5000/parse  (multipart/form-data, campo "file")
//   GET  http://localhost:5000/health
//
// Nota: SaveUtil.GetVariantSAV(byte[]) foi removido no PKHeX.Core 26.x.
// TryGetSaveFile oferece a mesma detecção automática de geração (GBA, DS, 3DS, Switch).

using Microsoft.AspNetCore.Http.Features;
using PKHeX.Core;
using PokeOps.Parser;
using Scalar.AspNetCore;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddCors(options =>
    options.AddDefaultPolicy(p => p.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader()));

builder.Services.AddOpenApi();

// Saves de Pokémon chegam a no máximo poucos MB; 16 MB é margem segura
builder.WebHost.ConfigureKestrel(k => k.Limits.MaxRequestBodySize = 16 * 1024 * 1024);
builder.Services.Configure<FormOptions>(f =>
{
    f.MultipartBodyLengthLimit = 16 * 1024 * 1024;
    f.ValueLengthLimit = int.MaxValue;
});

var app = builder.Build();

app.UseCors();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
    app.MapScalarApiReference();
}

app.MapGet("/health", () => Results.Ok(new { status = "ok" }))
    .WithSummary("Liveness check");

app.MapPost("/parse", async (HttpRequest request) =>
{
    if (!request.HasFormContentType)
        return Results.UnprocessableEntity(new { error = "Esperado multipart/form-data" });

    var form = await request.ReadFormAsync();
    var file = form.Files["file"];

    if (file is null || file.Length == 0)
        return Results.UnprocessableEntity(new { error = "Campo 'file' ausente ou vazio" });

    using var ms = new MemoryStream((int)file.Length);
    await file.CopyToAsync(ms);
    var saveBytes = ms.ToArray();

    try
    {
        if (!SaveUtil.TryGetSaveFile(saveBytes.AsMemory(), out var sav, string.Empty))
            return Results.UnprocessableEntity(new { error = "save inválido ou não suportado" });

        return Results.Ok(ParseSave(sav));
    }
    catch (Exception ex)
    {
        return Results.UnprocessableEntity(new { error = ex.Message });
    }
})
.WithSummary("Parseia um arquivo de save Pokémon")
.WithDescription("Recebe um .sav via multipart/form-data (campo 'file') e retorna os dados do treinador, time, boxes e pokédex.")
.Accepts<IFormFile>("multipart/form-data")
.Produces<ParseResponse>(StatusCodes.Status200OK)
.Produces(StatusCodes.Status422UnprocessableEntity)
.DisableAntiforgery();

app.Run();

// ── Parsing ───────────────────────────────────────────────────────────────────

static ParseResponse ParseSave(SaveFile sav)
{
    var trainer = new TrainerDto(sav.OT, sav.Version.ToString());

    var party = sav.PartyData
        .Where(p => p.Species != 0)
        .Select((p, i) => PokemonMapper.Map(p, i))
        .ToList();

    var boxes = new List<BoxDto>();
    int slotsPerBox = sav.BoxSlotCount;
    for (int box = 0; box < sav.BoxCount; box++)
    {
        var pokemon = new List<PokemonDto>();
        for (int slot = 0; slot < slotsPerBox; slot++)
        {
            var pkm = sav.GetBoxSlotAtIndex(box, slot);
            if (pkm.Species != 0)
                pokemon.Add(PokemonMapper.Map(pkm, slot));
        }
        string boxName = sav is IBoxDetailNameRead namedBoxes
            ? namedBoxes.GetBoxName(box)
            : $"Box {box + 1}";
        boxes.Add(new BoxDto(box + 1, boxName, pokemon));
    }

    var pokedex = new List<PokedexEntryDto>();
    for (ushort species = 1; species <= sav.MaxSpeciesID; species++)
    {
        bool seen = sav.GetSeen(species);
        bool caught = sav.GetCaught(species);
        if (seen || caught)
            pokedex.Add(new PokedexEntryDto(species, seen, caught));
    }

    return new ParseResponse(trainer, party, boxes, pokedex);
}

// DTOs definidos em Models.cs
