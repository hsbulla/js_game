from django.contrib import admin
from login_score.models import custom_game
from login_score.models import player_info
from login_score.models import player_shop

# Register your models here.

@admin.register(custom_game , player_info, player_shop)

class custom_gameAdmin(admin.ModelAdmin):
    pass

class player_infoAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'coin', 'best_score']

class player_shopAdmin(admin.ModelAdmin):
    list_display = ('id','nickname', 'item1', 'item2', 'item3', 'item4', 'item5')

