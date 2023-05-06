import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from shortener.models import URL


@pytest.fixture
def api_client() -> APIClient:
    """Return an authorized APIClient object."""
    test_user = get_user_model().objects.create_user(
        username="foo", password="bar"
    )
    token = Token.objects.create(user=test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client


@pytest.mark.parametrize("short_url_exists", [True, False])
@pytest.mark.django_db()
def test_get_short_url_endpoint_returns_http_201_with_correct_data(
    api_client: APIClient, short_url_exists: bool
) -> None:
    """Test that the get-short url endpoint returns http 201 status and
    correct data when authentication is successfull and short URL already
    exists or does not exist in DB.
    """
    url = reverse("get-short")
    full_url = "https://www.google.com"
    short_url = "https://foobar.com/8ffdefbdec956b595d257f0aaeefd623"

    if not short_url_exists:
        response = api_client.post(url, {"url": full_url})
        url_obj = URL.objects.first()
        assert response.json() == {
            "full_url": url_obj.full_url,
            "short_url": url_obj.short_url,
            "hits": url_obj.hits,
        }
    else:
        url_obj = URL.objects.create(full_url=full_url, short_url=short_url)
        response = api_client.post(url, {"url": full_url})
        assert response.json() == {
            "full_url": url_obj.full_url,
            "short_url": url_obj.short_url,
            "hits": url_obj.hits + 1,
        }
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db()
def test_get_full_url_endpoint_returns_http_200_with_correct_data(
    api_client: APIClient,
) -> None:
    """Test that the get-full url endpoint returns http 200 status and
    correct data when authentication is successfull and short URL already
    exists in DB.
    """
    full_url = "https://www.google.com"
    short_url = "https://foobar.com/8ffdefbdec956b595d257f0aaeefd623"

    URL.objects.create(full_url=full_url, short_url=short_url)

    url = reverse("get-full")
    response = api_client.post(url, {"url": short_url})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "full_url": full_url,
        "short_url": short_url,
        "hits": 1,
    }


@pytest.mark.django_db()
def test_list_urls_endpoint_returns_http_200_with_correct_data(
    api_client: APIClient,
) -> None:
    """Test that the get-full url endpoint returns http 200 status and
    correct data when authentication is successfull and URLs exist in DB.
    """
    full_urls = [
        "https://www.google.com",
        "https://www.foobar.xyz",
    ]
    short_urls = [
        "https://foobar.com/8ffdefbdec956b595d257f0aaeefd623",
        "http://foobar.com/6a84e8bef3917f8b400604ed8c983ade",
    ]

    for full, short in zip(full_urls, short_urls):
        URL.objects.create(full_url=full, short_url=short)

    url = reverse("get-urls")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "full_url": full_urls[0],
            "short_url": short_urls[0],
            "hits": 1,
        },
        {
            "full_url": full_urls[1],
            "short_url": short_urls[1],
            "hits": 1,
        },
    ]
