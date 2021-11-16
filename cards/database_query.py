import random
from rest_framework.response import Response
from cards.models import Cards, UserGameCardStatus, UserGameMapping


def card_get_all_query():
    """get cards all data"""
    card_data = Cards.objects.all()
    return card_data


def user_game_mapping_id():
    """get current game id"""

    last_game_user_id = UserGameMapping.objects.latest('id')
    return last_game_user_id


def user_status_query(get_cards_id, click_count=1):
    """
    user user_game_status insert query
    game_game_id in value 'user_game_mapping_id' function called which is in database_query.py
    'get_cards_id' param contain card_id
    click_count is for number of time game button clicked
    """
    try:
        UserGameCardStatus.objects.create(
            user_game_id=user_game_mapping_id(),
            card_id=get_cards_id,
            number_of_click=click_count
        )
    except TypeError:
        return Response("{error: user_id or card_id None}")


def check_duplicate():
    """
    compare Cards db and UserGameCardStatus db
    for return two last remaining cards
    """
    cards = card_get_all_query()
    for cards_data in cards:
        cards1 = UserGameCardStatus.objects.filter(user_game_id=user_game_mapping_id(), card_id=cards_data.id).first()
        if not cards1:
            return cards_data


def randomly_check():
    """
    randomly choose cards and validate that card already use before in same game
    and then function return validated card
    """
    random_number = random.choices(range(1, 53), k=1)
    print(random_number)
    cards_detail_id = Cards.objects.get(id=random_number[0])
    cards_check = UserGameCardStatus.objects.filter(card_id=cards_detail_id,
                                                    user_game_id=user_game_mapping_id())
    print(cards_check)
    if not cards_check:
        return cards_detail_id


def cards_type_number(game_last_card):
    """this function return card_type and card_number"""
    return [game_last_card.card_type, game_last_card.card_number]


def user_game_status_card_check(number):
    """for check cards count in db return True or False"""
    return UserGameCardStatus.objects.filter(user_game_id=user_game_mapping_id()).count() == number


def random_number_check():
    """get random cards in sequence of 5"""
    ls = []
    while True:
        if len(ls) == 5:
            break
        cards_data = randomly_check()
        game_last_card = check_duplicate()
        if cards_data:
            if cards_type_number(cards_data) not in ls:
                ls.append(cards_type_number(cards_data))
        elif user_game_status_card_check(50):
            if cards_type_number(game_last_card) not in ls:
                ls.append(cards_type_number(game_last_card))
                return ls
        elif user_game_status_card_check(51):
            if cards_type_number(game_last_card) not in ls:
                ls.append(cards_type_number(game_last_card))
                return ls
        elif user_game_status_card_check(52):
            break
    return ls
