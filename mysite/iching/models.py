from django.db import models

# Create your models here.
class Hexagram(models.Model):
    number = models.CharField(verbose_name="Number", max_length=80, help_text="Enter the number of the hexagram, eg. Hexagram 3")
    description = models.CharField(verbose_name="Description", max_length=100, help_text="Enter description of the hexagram")
    meaning = models.CharField(verbose_name="meaning", max_length=200)

class CoinTossResult(models.Model):
    COIN_SIDES = (
        ('Heads', 'Heads'),
        ('Tails', 'Tails'),
    )
    toss = models.CharField(verbose_name="toss", max_length=5, choices=COIN_SIDES)
    timestamp = models.DateTimeField(auto_now_add=True)
