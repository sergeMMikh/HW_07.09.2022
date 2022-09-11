import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


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
    response = client.get('/courses/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_course(client, courses_factory):
    """
    Проверка получения 1го курса (retrieve-логика)
    """
    message = courses_factory(_quantity=1)
    response = client.get('/courses/')
    data = response.json()

    assert response.status_code == 200
    assert data[0]['name'] == message[0].name


@pytest.mark.django_db
def test_get_courses(client, courses_factory):
    """
    Проверка получения списка курсов
    """
    message = courses_factory(_quantity=10)

    response = client.get('/courses/')
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


@pytest.mark.django_db
def test_course_creation(client):
    Student.objects.create(
        id=1,
        name='Yorik',
        birth_date='2000-01-01'
    )
    count = Course.objects.count()
    response = client.post('/courses/',
                           data={
                               "name": "Latin",
                               "students": [1]
                           })

    assert response.status_code == 201
    assert Course.objects.count() == count + 1
