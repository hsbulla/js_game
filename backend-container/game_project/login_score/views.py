from django.shortcuts import render
from django.http import HttpResponse
from login_score import utils
from .models import custom_game
import random, json

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

    custom_game_elements = custom_game.objects.all()
    for elements in custom_game_elements:
        custom_game_elements_platforms = elements.platforms
        custom_game_elements_backgrounds = elements.backgrounds
        custom_game_elements_obstacle = elements.obstacle

    if custom_game_elements_platforms == "platform_1":
        static_platform = "img/platform/platform_1.png"
    if custom_game_elements_platforms == "platform_2":
        static_platform = "img/platform/platform_3.png"
    if custom_game_elements_platforms == "platform_3":
        static_platform = "img/platform/platform_3.png"
    
    if custom_game_elements_backgrounds == "background_1":
        static_background = "img/background/background_1/background_1"
    if custom_game_elements_backgrounds == "background_2":
        static_background = "img/background/background_2/background_2"
    if custom_game_elements_backgrounds == "background_3":
        static_background = "img/background/background_2/background_2"

    if custom_game_elements_obstacle == "obstacle_1":
        static_obstacle = "img/obstacle/obstacle_1.jpg"
    if custom_game_elements_obstacle == "obstacle_2":
        static_obstacle = "img/obstacle/obstacle_2.jpg"
    if custom_game_elements_obstacle == "obstacle_3":
        static_obstacle = "img/obstacle/obstacle_2.jpg"

    nickname = request.POST.get("nickname")
    if nickname == "":
        nickname = "player_"
        number = str(random.randint(103, 138))
        nickname = nickname+number
        
    data_render = {"nickname": nickname, "static_platform": static_platform, "static_background": static_background, "static_obstacle": static_obstacle}

    return render(request, "index.html", context = data_render)
