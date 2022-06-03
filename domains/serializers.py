from rest_framework import serializers

from domains.models import Url, Domain


class UrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Url
        exclude = ("id", "domain")
        read_only_fields = ("status_code", "title", "dt", "error")


class DomainSerializer(serializers.ModelSerializer):

    class Meta:
        model = Domain
        fields = ("domain", "url_check_count", "has_active_url", "created", "urls")
        read_only_fields = ("__all__", )

    urls = UrlSerializer(many=True, read_only=True)
