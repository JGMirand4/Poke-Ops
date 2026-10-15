"""Popula/atualiza a tabela species com os dados da PokéAPI oficial.

Uso:
    uv run python -m app.scripts.seed

Idempotente: pode rodar de novo quando sair uma geração nova. Só insere as
espécies que faltam e corrige nomes que mudaram; o resto fica intacto.
"""

import httpx
from sqlmodel import Session, select

from app.config import settings
from app.dependencies import engine
from app.models import Species


def fetch_species() -> dict[int, str]:
    """Busca todas as espécies numa única requisição: {species_id: nome}."""
    url = settings.poke_api_ofc_url
    if not url:
        raise RuntimeError('POKE_API_OFC_URL não definida')

    # limit alto o bastante para trazer tudo, inclusive gerações futuras
    response = httpx.get(url, params={'limit': 100_000}, timeout=30)
    response.raise_for_status()

    # O id vem no fim da url: .../pokemon-species/25/ -> 25
    return {
        int(item['url'].rstrip('/').split('/')[-1]): item['name']
        for item in response.json()['results']
    }


def seed_species(session: Session, species: dict[int, str]) -> tuple[int, int]:
    """Sincroniza a tabela com `species`. Retorna (inseridas, atualizadas)."""
    existing = {s.species_id: s for s in session.exec(select(Species)).all()}
    inserted = updated = 0

    for species_id, name in species.items():
        current = existing.get(species_id)
        if current is None:
            session.add(Species(species_id=species_id, name=name))
            inserted += 1
        elif current.name != name:
            current.name = name
            updated += 1

    session.commit()
    return inserted, updated


def main():
    species = fetch_species()
    with Session(engine) as session:
        inserted, updated = seed_species(session, species)
    print(
        f'{len(species)} espécies na PokéAPI: '
        f'{inserted} inseridas, {updated} atualizadas.'
    )


if __name__ == '__main__':
    main()
