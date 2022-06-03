from django.db import models


class Domain(models.Model):
    domain = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def url_check_count(self):
        return len(self.urls.all())

    @property
    def has_active_url(self):
        return any([url.status_code for url in self.urls.all()])

    def __str__(self):
        return self.domain


class Url(models.Model):
    url = models.CharField(max_length=255)
    status_code = models.IntegerField()
    title = models.CharField(max_length=255)
    dt = models.DateTimeField(auto_now_add=True)
    error = models.CharField(max_length=255)
    domain = models.ForeignKey(to=Domain, on_delete=models.CASCADE, related_name="urls")

    def __str__(self):
        return f"domain: {self.domain}, url: {self.url}"
