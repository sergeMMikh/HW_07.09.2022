import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def courses_factory():
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
    Проверка получения одного курса (retrieve-логика)
    """
    message = courses_factory(_quantity=1)
    response = client.get(f'/courses/{str(message[0].id)}/')
    data = response.json()

    assert response.status_code == 200
    assert data.get('name') == message[0].name


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
    response = client.get('/courses/?',
                          {'id': message[5].id})

    data = response.json()

    assert response.status_code == 200
    assert data[0]['id'] == message[5].id


@pytest.mark.django_db
def test_filter_by_name_4_courses(client, courses_factory):
    """
    Проверка фильтрации списка курсов по name
    """
    message = courses_factory(_quantity=10)

    response = client.get(f'/courses/?name={message[5].name}')
    data = response.json()

    assert response.status_code == 200
    assert data[0]['name'] == message[5].name


@pytest.mark.django_db
def test_course_creation(client):
    """
    Проверка успешного создания курса
    """

    count = Course.objects.count()

    Student.objects.create(
        id=1,
        name='Yorik',
        birth_date='2000-01-01'
    )

    response = client.post('/courses/',
                           data={
                               "name": "Latin",
                               "students": [1]
                           })

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_course_update(client, courses_factory):
    """
    Проверка успешного обновления курса
    """

    message = courses_factory(_quantity=10)
    Student.objects.create(
        id=1,
        name='Yorik',
        birth_date='2000-01-01'
    )

    count = Course.objects.count()

    response = client.patch(f'/courses/{message[5].id}/',
                            data={
                                "name": "Latin",
                                "students": [1]
                            })
    data = response.json()

    assert response.status_code == 200
    assert Course.objects.count() == count
    assert data['name'] == "Latin"


@pytest.mark.django_db
def test_course_delete(client, courses_factory):
    """
    Проверка успешного удаления курса
    """
    count = Course.objects.count()
    message = courses_factory(_quantity=10)

    response = client.delete(f'/courses/{message[5].id}/')

    assert response.status_code == 204
    assert Course.objects.count() == count + 9
