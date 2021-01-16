from django.db import models

# Create your models here.
class basic_chore(models.Model):
	name=models.CharField(max_length=128)
	description=models.CharField(max_length=1024)
	requirements=models.CharField(max_length=256)
	limitations=models.CharField(max_length=256)
	pointValue=models.DecimalField(decimal_places=0, max_digits=5)

class rewards(models.Model):
	name=models.CharField(max_length=128)
	description=models.CharField(max_length=1024)
	limitations=models.CharField(max_length=256)
	pointValue=models.DecimalField(decimal_places=0, max_digits=5)