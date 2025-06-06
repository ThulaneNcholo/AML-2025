from django.db import models

# Create your models here.


class RegistrationsModel(models.Model):
    reference = models.CharField(max_length=50, null=True, blank=True)
    plans = models.CharField(max_length=200, null=True, blank=True)
    FullName = models.CharField(max_length=200, null=True, blank=True)
    contact = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    company = models.CharField(max_length=200, null=True, blank=True)
    position = models.CharField(max_length=200, null=True, blank=True)
    dietary = models.CharField(max_length=200, null=True, blank=True)
    other_diet = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.reference


class Proposal(models.Model):
    title = models.CharField(max_length=255)
    # Saves to MEDIA_ROOT/proposals/
    brochure = models.FileField(upload_to='static/brochure')

    def __str__(self):
        return self.title
