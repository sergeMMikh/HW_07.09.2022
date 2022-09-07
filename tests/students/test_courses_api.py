import pytest
from rest_framework.test import APIClient


def test_example():
    assert 2 == 2


@pytest.mark.django_db
def test_api():
    # Arrange
    client = APIClient()

    # Act
    response = client.get('/courses/')

    # Assert
    assert response.status_code == 200
