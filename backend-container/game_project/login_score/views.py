from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
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

    static_platform_mappings = {
        "platform_1": "img/platform/platform_1.png",
        "platform_2": "img/platform/platform_3.png",
        "platform_3": "img/platform/platform_3.png"
    }
    static_background_mappings = {
        "background_1": "img/background/background_1/background_1",
        "background_2": "img/background/background_2/background_2",
        "background_3": "img/background/background_2/background_2"
    }
    static_obstacle_mappings = {
        "obstacle_1": "img/obstacle/obstacle_1.jpg",
        "obstacle_2": "img/obstacle/obstacle_2.jpg",
        "obstacle_3": "img/obstacle/obstacle_2.jpg"
    }

    for elements in custom_game.objects.all():
        static_platform = static_platform_mappings.get(elements.platforms, "")
        static_background = static_background_mappings.get(elements.backgrounds, "")
        static_obstacle = static_obstacle_mappings.get(elements.obstacle, "")

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'GET':
            nickname = request.GET.get('nikname_get', None)
            coin_DB = 100
            best_score_DB = 2
            shop_DB = '1,1,0,0,0'
            return JsonResponse({'coin_DB':  coin_DB,'best_score_DB': best_score_DB, 'shop_DB': shop_DB})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    
    nickname = "player_"
    number = str(random.randint(103, 138))
    nickname = nickname+number
    data_render = {"nickname": nickname, "static_platform": static_platform, "static_background": static_background, "static_obstacle": static_obstacle}    

    if request.method == 'POST':
        nickname_from_base = request.POST.get("nickname")
        if nickname_from_base == "":
            nickname_from_base = "player_"
            number = str(random.randint(103, 138))
            nickname_from_base = nickname_from_base+number
        data_render = {"nickname": nickname_from_base, "static_platform": static_platform, "static_background": static_background, "static_obstacle": static_obstacle}

    return render(request, "index.html", context = data_render)

def api_response(request):
        if request.method == 'POST':
            data_api_to_DB = json.loads(request.body)
            coin_DB = data_api_to_DB['coin_DB']
            coin_from_local_storage = data_api_to_DB['coin_from_local_storage']
            coin_to_DB = int(coin_from_local_storage) - int(coin_DB)
            best_score_to_DB = data_api_to_DB['best_score_from_local_storage']
            shop_to_db = data_api_to_DB['shop_from_local_storage']
            nickname = data_api_to_DB['nickname_post']
            print(nickname, coin_to_DB, best_score_to_DB, shop_to_db)
        return HttpResponseRedirect('/')