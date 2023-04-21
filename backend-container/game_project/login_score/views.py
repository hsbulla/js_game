from django.shortcuts import render
from django.http import HttpResponse
import random
from login_score import utils



def login_score(request):

    player_nicknames_score = []
    for i in range(3):
        random.shuffle(utils.player_nicknames)
        nick = random.choice(utils.player_nicknames)
        player_nicknames_score.append(nick)
    player1_nickname, player2_nickname, player3_nickname = player_nicknames_score

    player_scores = []
    for i in range(3):
        score = random.randint(513, 730)
        player_scores.append(score)
    player_scores.sort()
    player_scores.reverse()
    player1_score, player2_score, player3_score = player_scores

    data = {"player_1": player1_nickname, 
            "player_2": player2_nickname, 
            "player_3": player3_nickname,
            "score_1": player1_score,
            "score_2": player2_score,
            "score_3": player3_score}
    
    return render(request, "base.html", context= data) 


def login_request(request):

    nickname = request.POST.get("nickname")
    if nickname == "":
        nickname = "player_"
        number = str(random.randint(103, 138))
        nickname = nickname+number

    data = {"nickname": nickname}

    return render(request, "index.html", context = data)