from django.contrib import admin
from login_score.models import custom_game
from login_score.models import player_info
from login_score.models import player_shop

# Register your models here.

class CustomGameAdmin(admin.ModelAdmin):
    pass
    list_display = ('platforms', 'backgrounds', 'obstacle')

class PlayerInfoAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'coin', 'best_score')
    list_editable = ('coin', 'best_score')
    list_filter = ('coin', 'best_score')
    
class PlayerShopAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'item1', 'item2', 'item3', 'item4', 'item_active')
    list_editable = ('item1', 'item2', 'item3', 'item4')
    list_filter = ('item1', 'item2', 'item3', 'item4')
    def item_active(self, obj):
        return obj.item5
    item_active.short_description = 'item_active'

admin.site.register(player_info, PlayerInfoAdmin)
admin.site.register(player_shop, PlayerShopAdmin)
admin.site.register(custom_game, CustomGameAdmin)
