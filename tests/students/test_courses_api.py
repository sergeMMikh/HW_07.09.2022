import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def courses_factory():
    # создаем курс через фабрику
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory



@pytest.mark.django_db
def test_api(client):
    # Arrange

    # Act
    response = client.get('/courses/')

    # Assert
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_course(client, courses_factory):
    """
    Проверка получения 1го курса (retrieve-логика)
    """
    # создаем курс через фабрику
    message = courses_factory(_quantity=1)
    # строим урл и делаем запрос через тестовый клиент

    response = client.get('/courses/')
    # проверяем, что вернулся именно тот курс, который запрашивали
    data = response.json()

    assert response.status_code == 200
    assert data[0]['name'] == message[0].name

@pytest.mark.django_db
def test_get_courses(client, courses_factory):
    """
    Проверка получения списка курсов
    """
    # создаем курс через фабрику
    message = courses_factory(_quantity=10)
    # строим урл и делаем запрос через тестовый клиент

    response = client.get('/courses/')
    # проверяем, что вернулся именно тот курс, который запрашивали
    data = response.json()

    assert response.status_code == 200
    assert len(data) == len(message)
    for i, m in enumerate(data):
        assert m['name'] == message[i].name

@pytest.mark.django_db
def test_filter_by_id_4_courses(client, courses_factory):
    """
    Проверка фильтрации списка курсов по id
    """
    message = courses_factory(_quantity=10)

    url = '/courses/?id=' + str(message[5].id)

    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data[0]['id'] == message[5].id

@pytest.mark.django_db
def test_filter_by_name_4_courses(client, courses_factory):
    """
    Проверка фильтрации списка курсов по id
    """
    message = courses_factory(_quantity=10)

    url = '/courses/?name=' + str(message[5].name)

    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data[0]['name'] == message[5].name
