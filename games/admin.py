# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Game, Solution, UserScore

admin.site.register(Game)
admin.site.register(Solution)
admin.site.register(UserScore)
