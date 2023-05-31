from django.db import models

# Create your models here.
class Coin(models.Model):
    COIN_SIDES = [
        ("Heads", "Heads"),
        ("Tails", "Tails"),
    ]
    side = models.CharField(max_length=5, choices=COIN_SIDES, default="Heads")

class CoinTossCombination(models.Model):
    coin1 = models.ForeignKey(to="Coin", verbose_name="coin1", related_name="combination_coin1", on_delete=models.SET_NULL, null=True)
    coin2 = models.ForeignKey(to="Coin", verbose_name="coin2", related_name="combination_coin2", on_delete=models.SET_NULL, null=True)
    coin3 = models.ForeignKey(to="Coin", verbose_name="coin3", related_name="combination_coin3",on_delete=models.SET_NULL, null=True)
    name = models.CharField(verbose_name="combination", max_length=3, default="")
    casted_result = models.ForeignKey(to="CastedResult", verbose_name="casted_result", on_delete=models.SET_NULL, null=True)

class CastedResult(models.Model):
    CASTED_RESULT = [
        ("HHT", "HHT"),
        ("TTH", "TTH"),
        ("HHH", "HHH"),
        ("TTT", "TTT"),
    ]

    name = models.CharField(verbose_name="casted_result", max_length=3, choices=CASTED_RESULT, null=True)

class Hexagram(models.Model):
    number = models.CharField(verbose_name="Number", max_length=80, help_text="Enter the number of the hexagram, eg. Hexagram 3")
    description = models.CharField(verbose_name="Description", max_length=100, help_text="Enter description of the hexagram")
    meaning = models.CharField(verbose_name="meaning", max_length=200)


