from django.contrib.auth.models import User
from .models import Cards, UserGameCardStatus
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from constants import (USERNAME, EMAIL, PASSWORD, PASSWORD2)


class RegisterSerializer(serializers.ModelSerializer):
    """ registration for every user"""
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (USERNAME, EMAIL, PASSWORD, PASSWORD2)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = ['card_type', 'card_number']

    def validate(self, attrs):
        card_check = Cards.objects.filter(card_type=attrs['card_type'], card_number=attrs['card_number'])
        if card_check:
            raise serializers.ValidationError({"cards": "cards already exist."})
        return attrs

    def create(self, validated_data):
        cards_data = Cards.objects.create(
            card_type=validated_data['card_type'],
            card_number=validated_data['card_number']
        )
        cards_data.save()
        return validated_data


class User_Input(serializers.Serializer):
    user_input = serializers.IntegerField()
    