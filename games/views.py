# -*- coding: utf-8 -*-
import re

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .models import Game, UserScore


class IndexView(generic.ListView):
    template_name = "games/index.html"
    context_object_name = "games_list"

    def get_queryset(self):
        return Game.objects.order_by("name")


class DetailView(generic.DetailView):
    model = Game
    template_name = "games/detail.html"


# def index(request):
#     games_list = Game.objects.order_by("id")
#     context = {"games_list": games_list}
#     return render(request, "games/index.html", context)


# def detail(request, game_id):
#     return HttpResponse("You're looking at game %s." % game_id)


def parse_wordle(sms_body):
    pat = r"^(?P<name>\w+) (?P<id>\d+) (?P<score>\d+)"
    try:
        return re.match(pat, sms_body).groupdict()
    except AttributeError:
        raise


@csrf_exempt
def process_sms(request):
    game_id = 1
    game = get_object_or_404(Game, pk=game_id)
    print(game)
    print(request.POST)
    res = parse_wordle(request.POST["Body"])
    score = UserScore(
        game=game,
        phone_number=request.POST["From"],
        submit_date=timezone.now(),
        game_date=timezone.now().date(),
        submission=request.POST["Body"],
        game_score=int(res["score"]),
    )
    score.save()
    print(request.POST)
    return HttpResponse("sms received")
