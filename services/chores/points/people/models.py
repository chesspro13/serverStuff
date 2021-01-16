from django.db import models

# Create your models here.
class Brandon(models.Model):
	date = models.CharField(max_length=8)
	task = models.CharField(max_length=256)
	remarks = models.CharField(max_length=1024)
	points = models.DecimalField(decimal_places=0, max_digits=3)

class Jennifer(models.Model):
	date = models.CharField(max_length=8)
	task = models.CharField(max_length=256)
	remarks = models.CharField(max_length=1024)
	points = models.DecimalField(decimal_places=0, max_digits=3)

class Pandora(models.Model):
	date = models.CharField(max_length=8)
	task = models.CharField(max_length=256)
	remarks = models.CharField(max_length=1024)
	points = models.DecimalField(decimal_places=0, max_digits=3)

class Violet(models.Model):
	date = models.CharField(max_length=8)
	task = models.CharField(max_length=256)
	remarks = models.CharField(max_length=1024)
	points = models.DecimalField(decimal_places=0, max_digits=3)

class invalid_passwords(models.Model):
	date = models.CharField(max_length=8)
	name = models.CharField(max_length=256)
	task = models.CharField(max_length=1024)