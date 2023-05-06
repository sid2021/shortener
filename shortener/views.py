import hashlib

from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import URL
from .serializers import URLSerializer
from .utils import is_url_valid


class GetShortUrl(mixins.CreateModelMixin, generics.GenericAPIView):
    """View responsible for returning shortened URL."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = URLSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        """Return shortened URL. We guarantee that every unique valid URL will
        only have one shortened version by generating a hexadecimal equivalent
        encoded string and storing it in DB.

        Before returning shortened URL we check DB if the requested full URL
        already exists in DB. In such case we return the shortened URL based
        on object retrieved from DB. Othwerwise, we generate a shortened URL,
        save it in DB and return it within the Response object.
        """
        url = request.data.get("url")

        if not is_url_valid(url):
            return Response(
                {"msg": "Error parsing URL. Provide a valid URL (RFC 3986)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {
            "full_url": url,
            "short_url": f"https://foobar.com/{hashlib.md5(url.encode()).hexdigest()}",
        }
        url_obj = URL.objects.filter(full_url=url).first()

        if not url_obj:
            serializer = self.serializer_class(data=data)
        serializer = self.serializer_class(url_obj, data=data)

        serializer.is_valid()
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetFullUrl(mixins.CreateModelMixin, generics.GenericAPIView):
    """View responsible for returning full URL."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = URLSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        """Return full URL."""
        url = request.data.get("url")
        if not is_url_valid(url):
            return Response(
                {"msg": "Error parsing URL. Provide a valid URL (RFC 3986)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        url_obj = get_object_or_404(URL, short_url=url)
        serializer = self.serializer_class(url_obj)
        return Response(serializer.data)


class ListUrls(mixins.ListModelMixin, generics.GenericAPIView):
    """View responsible for returning list of all URLs."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = URL.objects.all()
    serializer_class = URLSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        """Get list of existing URLs."""
        return self.list(request, *args, **kwargs)
