# -*- coding: utf-8 -*-
import re

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import generic
from django_twilio.decorators import twilio_view
from twilio.twiml.messaging_response import MessagingResponse

from .models import Game, UserScore


class IndexView(generic.ListView):
    template_name = "games/index.html"
    context_object_name = "games_list"

    def get_queryset(self):
        return Game.objects.order_by("name")


class ScoresView(generic.ListView):
    template_name = "games/scores.html"
    context_object_name = "score_list"

    def get_queryset(self):
        return UserScore.objects.order_by("game_score")


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
    wordle_pat = r"^(?P<name>Wordle) (?P<id>\d+) (?P<score>\d+).*\n\n(?P<entry>[\W\n]+)"
    try:
        return re.match(wordle_pat, sms_body).groupdict()
    except AttributeError:
        raise


@twilio_view
def process_sms(request):
    """Process received message."""
    # TODO: figure out how to prevent multiple submissions
    print(request.POST)
    # Get sms for processing. If no body we return an empty string so
    # that subsequent things can still execute.
    sms_body = request.POST.get("Body", "")

    # Process by game type
    if "Wordle" in sms_body:
        # Do wordle parsing
        # TODO: fix this hard-coded game_id
        game_id = 1
        game = get_object_or_404(Game, pk=game_id)
        print(game)
        print(request.POST)
        res = parse_wordle(sms_body)

        score = UserScore(
            game=game,
            phone_number=request.POST["From"],
            submit_date=timezone.now(),
            game_date=timezone.now().date(),
            submission=res["entry"],
            game_score=int(res["score"]),
            full_message=sms_body,
        )
        score.save()

        msg = "Wordle score processed"

    else:
        msg = "Unable to process message"

    r = MessagingResponse()
    r.message(msg)

    return r
