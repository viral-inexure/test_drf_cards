from random import randrange
from django.contrib.auth.models import User
from django.db import models


def generate_unique_code():
    code = randrange(0, 1000000, 6)
    game_code_check = Game.objects.filter(game_token=code).first()
    if not game_code_check:
        return code
    return generate_unique_code()


class Game(models.Model):
    game_token = models.IntegerField(default=generate_unique_code)

    def __str__(self):
        return str(self.game_token)


class Cards(models.Model):
    card_type = models.CharField(max_length=50)
    card_number = models.CharField(max_length=5)

    def __str__(self):
        return f'{self.card_type} of {self.card_number}'


class UserGameMapping(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class UserGameCardStatus(models.Model):
    user_game_id = models.ForeignKey(UserGameMapping, on_delete=models.CASCADE)
    card_id = models.ForeignKey(Cards, on_delete=models.CASCADE)
    number_of_click = models.IntegerField()

    def __str__(self):
        return str(self.id)


class Scoreboard(models.Model):
    user_game_id = models.ForeignKey(UserGameMapping, on_delete=models.CASCADE)
    game_status = models.BooleanField()

    def __str__(self):
        return str(self.id)
