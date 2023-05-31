from django.db import models

# Create your models here.
class Coin(models.Model):
    COIN_SIDES = [
        ("Heads", "Heads"),
        ("Tails", "Tails"),
    ]
    side = models.CharField(max_length=5, choices=COIN_SIDES, default="Heads")

    def __str__(self):
        return f"{self.side}"
class CoinTossCombination(models.Model):
    coin1 = models.ForeignKey(to="Coin", verbose_name="Coin1", related_name="combination_coin1", on_delete=models.SET_NULL, null=True)
    coin2 = models.ForeignKey(to="Coin", verbose_name="Coin2", related_name="combination_coin2", on_delete=models.SET_NULL, null=True)
    coin3 = models.ForeignKey(to="Coin", verbose_name="Coin3", related_name="combination_coin3",on_delete=models.SET_NULL, null=True)
    name = models.CharField(verbose_name="combination", max_length=3, default="")
    casted_result = models.ForeignKey(to="CastedResult", verbose_name="Casted result", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}"

class CastedResult(models.Model):
    CASTED_RESULT = [
        ("HHT", "HHT"),
        ("TTH", "TTH"),
        ("HHH", "HHH"),
        ("TTT", "TTT"),
    ]

    name = models.CharField(verbose_name="Casted Result", max_length=3, choices=CASTED_RESULT, null=True)
    line = models.ForeignKey(to="Line", verbose_name="Line", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}"

class Line(models.Model):
    LINE_CHOICE = [
        ("Solid", "Solid"),
        ("Broken", "Broken"),
    ]

    line = models.CharField(max_length=6, choices=LINE_CHOICE, default="Solid")

    def __str__(self):
        return f"{self.line}"

class Hexagram(models.Model):
    number = models.CharField(verbose_name="Number", max_length=80, help_text="Enter the number of the hexagram, eg. Hexagram 3")
    description = models.CharField(verbose_name="Description", max_length=200, help_text="Enter description of the hexagram")
    meaning = models.CharField(verbose_name="meaning", max_length=300)
    line1 = models.ForeignKey(to="Line", verbose_name="Line1", on_delete=models.SET_NULL, null=True, related_name="line1")
    line2 = models.ForeignKey(to="Line", verbose_name="Line2", on_delete=models.SET_NULL, null=True, related_name="line2")
    line3 = models.ForeignKey(to="Line", verbose_name="Line3", on_delete=models.SET_NULL, null=True, related_name="line3")
    line4 = models.ForeignKey(to="Line", verbose_name="Line4", on_delete=models.SET_NULL, null=True, related_name="line4")
    line5 = models.ForeignKey(to="Line", verbose_name="Line5", on_delete=models.SET_NULL, null=True, related_name="line5")
    line6 = models.ForeignKey(to="Line", verbose_name="Line6", on_delete=models.SET_NULL, null=True, related_name="line6")

    def __str__(self):
        return f"{self.number}"

