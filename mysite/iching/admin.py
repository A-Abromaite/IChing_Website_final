from django.contrib import admin
from .models import Hexagram, Coin, CoinTossCombination, CastedResult, Line

class CoinAdmin(admin.ModelAdmin):
    list_display = ["side"]

class CoinTossCombinationAdmin(admin.ModelAdmin):
    list_display = ["name", "casted_result"]

class CastedResultAdmin(admin.ModelAdmin):
    list_display = ["name"]

class LineAdmin(admin.ModelAdmin):
    list_display = ["line"]

class HexagramAdmin(admin.ModelAdmin):
    list_display = ["number"]

# Register your models here.
admin.site.register(Coin, CoinAdmin)
admin.site.register(CoinTossCombination, CoinTossCombinationAdmin)
admin.site.register(CastedResult, CastedResultAdmin)
admin.site.register(Line, LineAdmin)
admin.site.register(Hexagram)
