from django.contrib import admin

# Register your models here.
from .models import Game, Cards, UserGameMapping, UserGameCardStatus, Scoreboard


class Game_admin(admin.ModelAdmin):
    list_display = ('game_token',)


class UserGameCardStatus_admin(admin.ModelAdmin):
    list_display = ('user_game_id', 'card_id', 'number_of_click')


class Scoreboard_admin(admin.ModelAdmin):
    list_display = ('user_game_id', 'game_status')


admin.site.register(Game, Game_admin)
admin.site.register(Cards)
admin.site.register(UserGameMapping)
admin.site.register(UserGameCardStatus, UserGameCardStatus_admin)
admin.site.register(Scoreboard, Scoreboard_admin)
