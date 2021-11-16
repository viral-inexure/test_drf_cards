import random
from sqlite3 import IntegrityError

from django.contrib.auth.models import User
from rest_framework import generics, viewsets, request
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from cards.models import Cards, Game, UserGameMapping, UserGameCardStatus, Scoreboard
from cards.serializers import RegisterSerializer, CardsSerializer, User_Input
from .database_query import (card_get_all_query, user_status_query, user_game_mapping_id, random_number_check)
from .utiles import resume_random_number_check


class RegisterView(generics.CreateAPIView):
    """ user registration """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class CardsView(viewsets.ModelViewSet):
    """
    for create cards in db
    card_get_all_query() function import from database_query.py use for get all cards data
    """
    queryset = card_get_all_query()
    serializer_class = CardsSerializer


class GameToken(APIView):
    """
    create new game or new game token
    function Game() is import from models.py and use for get random numbers as game token
    """
    serializer_class = User_Input

    def get(self, request):
        games = Game()
        game_token_check = Game.objects.filter(game_token=games.game_token).first()
        if not game_token_check:
            game = Game.objects.create(game_token=games.game_token)
            game_id_mapping = Game.objects.get(id=game.id)
            UserGameMapping.objects.create(game_id=game_id_mapping,
                                           user_id=request.user
                                           )
            return Response(game_id_mapping.id)


class Game_List(viewsets.ViewSet):

    def get(self, request, *args, **kwargs):
        complete_game = []
        incomplete_game = []
        games = UserGameMapping.objects.all().filter(user_id=request.user)
        for i in games:
            cards_count = UserGameCardStatus.objects.filter(user_game_id=i).count()
            complete_game.append({"total_game": i.id})
            if cards_count < 52:
                incomplete_game.append({'incomplete game': i.id})
        total_game = complete_game + incomplete_game

        return Response(total_game)


class Game_User_Status_View(APIView):

    def get(self, request, id=''):
        try:
            if id:
                user_resume_id = UserGameMapping.objects.filter(id=id).first()
            else:
                user_resume_id = UserGameMapping.objects.latest('id')
            list_of_cards = resume_random_number_check(user_resume_id)
            for list_item in list_of_cards:
                get_cards_id = Cards.objects.filter(card_type=list_item[0], card_number=list_item[1]).first()
                UserGameCardStatus.objects.create(
                    user_game_id=user_resume_id,
                    card_id=get_cards_id,
                    number_of_click=1
                )
            return Response(list_of_cards)
        except Exception as e:
            print(e)
            return Response("game not found")




# class Game_User_Status_View(APIView):
#     """for get different  cards and insert into (user_card_status)"""
#     def get(self, request):
#         """insert into UserGameCardStatus model and give response of sequence of cards"""
#         user_id = UserGameMapping.objects.latest('id').user_id.id
#         if user_id == request.user.id:
#             list_of_cards = random_number_check()
#             for list_item in list_of_cards:
#                 get_cards_id = Cards.objects.filter(card_type=list_item[0], card_number=list_item[1]).first()
#                 user_status_query(get_cards_id)
#             return Response(list_of_cards)
#         else:
#             return Response("start new game")


class Game_Result(APIView):
    """
    for return game result and insert data in scoreboard model
    """

    def get(self, request):

        if UserGameCardStatus.objects.filter(user_game_id=user_game_mapping_id()).count():
            last_entry = UserGameCardStatus.objects.filter(user_game_id=user_game_mapping_id()).latest('id')
            if last_entry:
                result = last_entry.card_id.card_number
                Scoreboard.objects.create(
                    user_game_id=last_entry.user_game_id,
                    game_status=False
                )
                if result == "A":
                    Scoreboard.game_status = True
                    return Response("winner")
                else:
                    return Response("Loser")
            else:
                return Response("game not played yet")


class Game_Reset(APIView):
    """for game reset"""

    def get(self, request):
        try:
            UserGameCardStatus.objects.filter(user_game_id=user_game_mapping_id()).delete()
            return Response("Game has been reset")
        except Exception as e:
            print(f'error --  {e}')


class Check_Remain_Card(APIView):
    """for check count of remaining cards """

    def get(self, request):
        total_card_enter = UserGameCardStatus.objects.filter(user_game_id=user_game_mapping_id()).count()
        total_remain = 52 - total_card_enter
        return Response(total_remain)
