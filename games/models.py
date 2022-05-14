# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.utils import timezone


class Game(models.Model):
    """Wordle-like game."""

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    site_url = models.URLField()

    def __str__(self):
        return self.name


class Solution(models.Model):
    """Game result."""

    game = models.ForeignKey(Game, on_delete=CASCADE)
    solution = models.JSONField()
    pub_date = models.DateField("date published")

    def __str__(self):
        return "GameSolution"

    def is_todays_solution(self):
        return self.pub_date == timezone.now().date


class UserScore(models.Model):
    """Submitted game score."""

    game = models.ForeignKey(Game, on_delete=CASCADE)
    phone_number = CharField(max_length=255)
    submit_date = models.DateTimeField("date submitted")
    game_date = models.DateField("Date parsed from sms")
    submission = models.CharField(max_length=255)
    game_score = models.IntegerField()
    full_message = models.CharField(max_length=255)

    def __str__(self):
        return "UserScore"
