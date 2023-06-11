from django.contrib import admin
from .models import Hexagram, Coin, CoinTossCombination, CastedResult, Line, UserProfile, HexagramInstance

class CoinAdmin(admin.ModelAdmin):
    list_display = ["side"]

class CoinTossCombinationAdmin(admin.ModelAdmin):
    list_display = ["name", "casted_result"]

class CastedResultAdmin(admin.ModelAdmin):
    list_display = ["name", "line"]

class LineAdmin(admin.ModelAdmin):
    list_display = ["line"]

class HexagramAdmin(admin.ModelAdmin):
    list_display = ["number", "line1", "line2", "line3", "line4", "line5", "line6"]

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user"]

class HexagramIntanceAdmin(admin.ModelAdmin):
    list_display = ["user_profile", "hexagram_number", "modified_hexagram_number", "date_saved", "note"]

# Register your models here.
admin.site.register(Coin, CoinAdmin)
admin.site.register(CoinTossCombination, CoinTossCombinationAdmin)
admin.site.register(CastedResult, CastedResultAdmin)
admin.site.register(Line, LineAdmin)
admin.site.register(Hexagram, HexagramAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(HexagramInstance, HexagramIntanceAdmin)
