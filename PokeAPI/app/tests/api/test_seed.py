from sqlmodel import select

from app.models import Species
from app.scripts.seed import seed_species


def test_seed_insere_todas_as_especies(session):
    species = {1: 'bulbasaur', 2: 'ivysaur'}

    inserted, updated = seed_species(session, species)

    assert (inserted, updated) == (len(species), 0)
    assert len(session.exec(select(Species)).all()) == len(species)


def test_seed_so_insere_especies_novas(session):
    seed_species(session, {1: 'bulbasaur'})

    # Simula uma geração nova saindo na PokéAPI
    inserted, updated = seed_species(session, {1: 'bulbasaur', 2: 'ivysaur'})

    assert (inserted, updated) == (1, 0)


def test_seed_atualiza_nome_alterado(session):
    seed_species(session, {1: 'bulbasaur'})

    inserted, updated = seed_species(session, {1: 'bulbasaur-novo'})

    assert (inserted, updated) == (0, 1)
    assert session.get(Species, 1).name == 'bulbasaur-novo'
