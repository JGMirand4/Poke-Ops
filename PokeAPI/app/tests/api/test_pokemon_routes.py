from dataclasses import asdict
from http import HTTPStatus

from sqlalchemy import select

from app.models.save import Save


def test_get_pokemon(client):
    response = client.get('/pokemon/1')

    assert response.status_code == HTTPStatus.OK


def test_create_save(session, mock_db_time):
    with mock_db_time(model=Save) as time:
        new_save = Save(
            save_name='test',
            trainer_name='test trainer',
            game_name='X',
            nr_pokemons=10,
        )

        session.add(new_save)
        session.commit()

    save = session.scalar(select(Save).where(Save.save_name == 'test'))

    assert asdict(save) == {
        'id': 1,
        'save_name': 'test',
        'trainer_name': 'test trainer',
        'game_name': 'X',
        'nr_pokemons': 10,
        'created_at': time,
        'updated_at': time,
    }
