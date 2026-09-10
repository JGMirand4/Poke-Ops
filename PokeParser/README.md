# PokeParser

Repositório do ecossistema de parsing de saves Pokémon do **PokeOps**. Contém dois projetos: um script de console para inspeção local e o microserviço HTTP principal.

## Projetos

| Projeto | Tipo | Descrição |
|---|---|---|
| `PokeParser` | Console | Lê um arquivo `.sav` local e imprime no terminal |
| `PokeOps.Parser` | ASP.NET Core (Minimal API) | Microserviço HTTP que recebe um save e devolve JSON |

## Pré-requisitos

- [.NET 10 SDK](https://dotnet.microsoft.com/download)

## Como rodar

### Console (inspeção local)

```bash
dotnet run --project PokeParser
```

Lê o save configurado diretamente em `Program.cs` e imprime treinador, time e boxes no terminal.

### Microserviço HTTP

```bash
dotnet run --project PokeOps.Parser
```

Sobe em `http://localhost:5000`.

## PokeOps.Parser — Endpoints

### `GET /health`

Liveness check. Retorna `200` se o serviço está no ar.

```json
{ "status": "ok" }
```

### `POST /parse`

Recebe um arquivo de save via `multipart/form-data` (campo `file`) e devolve os dados parseados.

**Gerações suportadas:** GBA (RS/E/FRLG), DS (DPPt/HGSS/BW/B2W2), 3DS (XY/ORAS/SM/USUM) e Switch (SwSh/PLA/SV/ZA).

**Exemplo com curl:**

```bash
curl -X POST http://localhost:5000/parse \
  -F "file=@/caminho/para/main.sav"
```

**Resposta `200`:**

```json
{
  "trainer": {
    "otName": "Ash",
    "gameVersion": "ScarletViolet"
  },
  "party": [
    {
      "speciesId": 6,
      "nickname": "Charizard",
      "level": 100,
      "isShiny": false,
      "nature": "Adamant",
      "ability": "Blaze",
      "ivHp": 31,
      "ivAtk": 31,
      "ivDef": 31,
      "ivSpa": 31,
      "ivSpd": 31,
      "ivSpe": 31,
      "heldItemId": 247,
      "slotNumber": 0
    }
  ],
  "boxes": [
    {
      "boxNumber": 1,
      "boxName": "Box 1",
      "pokemon": [ ]
    }
  ],
  "pokedex": [
    { "speciesId": 1, "seen": true, "caught": true }
  ]
}
```

**Resposta `422`** (save inválido ou erro de parsing):

```json
{ "error": "save inválido ou não suportado" }
```

### `GET /scalar`

Interface interativa (Scalar UI) disponível em ambiente de desenvolvimento.

## Estrutura

```
PokeParser/
├── PokeParser.slnx              # Solution
├── Program.cs                   # Console — lê save local
├── PokeParser.csproj
│
├── PokeOps.Parser/
│   ├── Program.cs               # Minimal API (endpoints + parsing)
│   ├── PokemonMapper.cs         # PKM → PokemonDto
│   ├── Models.cs                # DTOs de resposta
│   └── PokeOps.Parser.csproj
│
└── PokeParser.Api/              # Protótipo inicial (não usar em produção)
```

## Dependências principais

| Pacote | Uso |
|---|---|
| `PKHeX.Core` | Parsing de saves Pokémon |
| `Microsoft.AspNetCore.OpenApi` | Geração do spec OpenAPI |
| `Scalar.AspNetCore` | UI interativa da API |
