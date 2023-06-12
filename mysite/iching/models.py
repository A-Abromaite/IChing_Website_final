from django.db import models
from django.contrib.auth.models import User
from PIL import Image


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
    coin1 = models.ForeignKey(to="Coin", verbose_name="Coin1", related_name="combination_coin1",
                              on_delete=models.SET_NULL, null=True)
    coin2 = models.ForeignKey(to="Coin", verbose_name="Coin2", related_name="combination_coin2",
                              on_delete=models.SET_NULL, null=True)
    coin3 = models.ForeignKey(to="Coin", verbose_name="Coin3", related_name="combination_coin3",
                              on_delete=models.SET_NULL, null=True)
    name = models.CharField(verbose_name="combination", max_length=3, default="")
    casted_result = models.ForeignKey(to="CastedResult", verbose_name="Casted Result", on_delete=models.SET_NULL,
                                      null=True)

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
    number = models.CharField(verbose_name="Number", max_length=80,
                              help_text="Enter the number of the hexagram, eg. Hexagram 3")
    description = models.CharField(verbose_name="Description", max_length=200,
                                   help_text="Enter description of the hexagram")
    meaning = models.CharField(verbose_name="meaning", max_length=300)
    line1 = models.ForeignKey(to="Line", verbose_name="Line1", on_delete=models.SET_NULL, null=True,
                              related_name="line1")
    line2 = models.ForeignKey(to="Line", verbose_name="Line2", on_delete=models.SET_NULL, null=True,
                              related_name="line2")
    line3 = models.ForeignKey(to="Line", verbose_name="Line3", on_delete=models.SET_NULL, null=True,
                              related_name="line3")
    line4 = models.ForeignKey(to="Line", verbose_name="Line4", on_delete=models.SET_NULL, null=True,
                              related_name="line4")
    line5 = models.ForeignKey(to="Line", verbose_name="Line5", on_delete=models.SET_NULL, null=True,
                              related_name="line5")
    line6 = models.ForeignKey(to="Line", verbose_name="Line6", on_delete=models.SET_NULL, null=True,
                              related_name="line6")
    picture = models.ImageField(default="hexagrams/default.png", upload_to="hexagrams")

    def __str__(self):
        return f"{self.number}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"


class HexagramInstance(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hexagram_number = models.ForeignKey(Hexagram, on_delete=models.CASCADE, related_name='hexagram_instances')
    modified_hexagram_number = models.ForeignKey(Hexagram, on_delete=models.CASCADE, null=True, blank=True,
                                                 related_name='modified_hexagram_instances')
    date_saved = models.DateTimeField(auto_now_add=True)
    note = models.TextField(verbose_name='Note', max_length=2000)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.hexagram_number.number}"
