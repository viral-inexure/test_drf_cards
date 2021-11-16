from django.urls import path, include
from rest_framework import routers
from .views import (RegisterView, CardsView, GameToken, Game_User_Status_View, Game_Reset,
                    Game_Result, Check_Remain_Card, Game_List)
app_name = 'cards'
router = routers.DefaultRouter()
router.register('cards', CardsView, basename='cards')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_auth.urls')),
    # path('api-auth/login', include('rest_auth.urls')), # for login
    # path('admin/admin/logout/', include('rest_auth.urls')), # for logout
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('game/start/', GameToken.as_view(), name='user_game'),
    path('game/play/', Game_User_Status_View.as_view(), name='user_game_status'),
    path('game/play/<int:id>/', Game_User_Status_View.as_view(), name='user_game_resume'),
    path('game/reset/', Game_Reset.as_view(), name='game_reset'),
    path('game/result/', Game_Result.as_view(), name='game_result'),
    path('total_remain_card/', Check_Remain_Card.as_view(), name='check_remain_card'),
    path('game/game_list/', Game_List.as_view({'get': 'get'}), name='game_list'),
    # path('game/resume/', Game_Resume.as_view(), name='game_resume'),
]
