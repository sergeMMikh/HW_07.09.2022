import pytest
from rest_framework.test import APIClient
# from model_bakery import baker
import baker

from students.models import Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def courses_factory():
    # создаем курс через фабрик
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory()



@pytest.mark.django_db
def test_api(client):
    # Arrange

    # Act
    response = client.get('/courses/')

    # Assert
    assert response.status_code == 200

# @pytest.mark.django_db
# def test_get_courses(client, courses_factory):
#     """
#     проверка получения 1го курса (retrieve-логика)
#     """
#
#     # создаем курс через фабрику
#     message = courses_factory(_qantity=10)
#     # строим урл и делаем запрос через тестовый клиент
#     response = client.get('/courses/')
#     # проверяем, что вернулся именно тот курс, который запрашивали
#
#
#     assert response.status_code == 200


