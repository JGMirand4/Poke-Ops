from http import HTTPStatus


def test_get_pokemon(client):
    response = client.get('/pokemon/1')

    assert response.status_code == HTTPStatus.OK
