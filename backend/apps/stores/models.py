from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Store(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="stores")
    name = models.CharField(max_length=120)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=2)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} - {self.city}/{self.state}"
