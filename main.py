""" for enter card data 52 cards"""

# ls1 = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
# ls2 = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
# for i in ls1:
#     for j in ls2:
#         print(f'{i} of {j}')
#         c = Cards.objects.create(card_type=i, card_number=j)
#         c.save()

print('hell')
a = 52
user = int(input("enter number :"))
print(user)
b = a % user
print(b)