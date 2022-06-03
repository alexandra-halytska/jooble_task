import requests
from bs4 import BeautifulSoup

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from requests.exceptions import ConnectionError

from domains.models import Url, Domain
from domains.serializers import DomainSerializer


class DomainApi(APIView):

    @staticmethod
    def post(request):
        url = request.data["url"]
        title, error = "", ""
        try:
            response = requests.get(url)
            status_code = response.status_code
            error = response.reason
            title = BeautifulSoup(response.text, "lxml").find("title").text if status_code == 200 else ""
        except ConnectionError:
            error = "Connection Error"
            status_code = 0

        start = url.index("/") + 2
        domain = url[start:url[start:].index("/") + start]
        new_domain = Domain.objects.get_or_create(
            domain=domain
        )
        new_url = Url.objects.get_or_create(
            url=url,
            status_code=status_code,
            error=error,
            title=title,
            domain=new_domain[0]
        )
        new_domain[0].save()
        new_url[0].save()
        domain = Domain.objects.get(domain=domain)
        serializer = DomainSerializer(domain)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Statistics(APIView):

    @staticmethod
    def get(request):
        result = dict()
        result["url_count"] = len(Url.objects.all())
        result["active_url_count"] = len(Url.objects.filter(status_code=200))
        result["exceptions"] = len(Url.objects.filter(status_code=0))
        result["domain_count"] = len(Domain.objects.all())
        result["active_domain_count"] = len(
            [
                domain for domain in Domain.objects.all() if domain.has_active_url
            ]
        )
        return Response(result)
