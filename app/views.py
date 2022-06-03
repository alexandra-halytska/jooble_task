import requests
import tldextract
from bs4 import BeautifulSoup

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Url, Domain
from app.serializers import DomainSerializer


class FirstTask(APIView):

    def post(self, request):
        url = request.data["url"]
        title, error = "", ""
        try:
            response = requests.get(url).text
            status_code = requests.get(url).status_code
            error = requests.get(url).reason
            title = BeautifulSoup(response, "lxml").find("title").text if status_code == 200 else ""
        except requests.exceptions.ConnectionError:
            error = "Connection Error"
            status_code = 0

        domain = '.'.join(tldextract.extract(url)[:3]).strip(".")
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


class SecondTask(APIView):

    def get(self, request):
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
