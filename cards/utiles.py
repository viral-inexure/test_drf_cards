import random

from cards.models import UserGameCardStatus, UserGameMapping, Cards


def resume_randomly_check(game_id):
    """
    randomly choose cards and validate that card already use before in same game
    and then function return validated card
    """
    if game_id:
        random_number = random.choices(range(1, 53), k=1)
        print(random_number)
        cards_detail_id = Cards.objects.get(id=random_number[0])
        cards_check = UserGameCardStatus.objects.filter(card_id=cards_detail_id,
                                                        user_game_id=game_id)
        print(cards_check)
        if not cards_check:
            return cards_detail_id
    else:
        random_number = random.choices(range(1, 53), k=1)
        print(random_number)
        cards_detail_id = Cards.objects.get(id=random_number[0])
        cards_check = UserGameCardStatus.objects.filter(card_id=cards_detail_id,
                                                        user_game_id=UserGameMapping.objects.latest('id'))
        print(cards_check)
        if not cards_check:
            return cards_detail_id


def card_get_all_query():
    """get cards all data"""
    card_data = Cards.objects.all()
    return card_data


def resume_check_duplicate(game_id):
    """
    compare Cards db and UserGameCardStatus db
    for return two last remaining cards
    """
    cards = card_get_all_query()
    if game_id:
        for cards_data in cards:
            cards1 = UserGameCardStatus.objects.filter(user_game_id=game_id,
                                                       card_id=cards_data.id).first()
            if not cards1:
                return cards_data
    else:
        for cards_data in cards:
            cards1 = UserGameCardStatus.objects.filter(user_game_id=UserGameMapping.objects.latest('id'),
                                                       card_id=cards_data.id).first()
            if not cards1:
                return cards_data


def resume_cards_type_number(game_last_card):
    """this function return card_type and card_number"""
    return [game_last_card.card_type, game_last_card.card_number]


def resume_user_game_status_card_check(number, game_id):
    """for check cards count in db return True or False"""
    if game_id:
        return UserGameCardStatus.objects.filter(user_game_id=game_id).count() == number
    else:
        return UserGameCardStatus.objects.filter(user_game_id=UserGameMapping.objects.latest('id')).count() == number


def resume_random_number_check(game_id):
    """get random cards in sequence of 5"""
    ls = []
    while True:
        if len(ls) == 5:
            break
        cards_data = resume_randomly_check(game_id)
        game_last_card = resume_check_duplicate(game_id)
        if cards_data:
            if resume_cards_type_number(cards_data) not in ls:
                ls.append(resume_cards_type_number(cards_data))
        elif resume_user_game_status_card_check(50, game_id):
            if resume_cards_type_number(game_last_card) not in ls:
                ls.append(resume_cards_type_number(game_last_card))
                return ls
        elif resume_user_game_status_card_check(51, game_id):
            if resume_cards_type_number(game_last_card) not in ls:
                ls.append(resume_cards_type_number(game_last_card))
                return ls
        elif resume_user_game_status_card_check(52, game_id):
            break
    return ls
