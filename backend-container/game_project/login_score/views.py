from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
from .models import custom_game, player_info, player_shop
import random, json
import sqlite3

def login_score(request):

    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT nickname, best_score FROM player_info ORDER BY best_score DESC LIMIT 3")
    result_top = cursor.fetchall()

    player1_nickname = result_top[0][0]
    player2_nickname = result_top[1][0]
    player3_nickname = result_top[2][0]

    player1_best_score = result_top[0][1]
    player2_best_score = result_top[1][1]
    player3_best_score = result_top[2][1]

    data = {"player_1": player1_nickname, 
            "player_2": player2_nickname, 
            "player_3": player3_nickname,
            "score_1": player1_best_score,
            "score_2": player2_best_score,
            "score_3": player3_best_score}
    
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
            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()

            coin_DB = 0
            best_score_DB = 0
            shop_DB = '1,0,0,0,0'

            cursor.execute("SELECT coin, best_score FROM player_info WHERE nickname=?", (nickname,))
            if cursor.fetchone() is None: 
                player_info_to = player_info()
                player_info_to.nickname = nickname
                player_info_to.coin = 0
                player_info_to.best_score = 0
                player_info_to.save()
            else: 
                result = cursor.fetchone()
                if result:
                    coin_DB, best_score_DB = result

            cursor.execute("SELECT item1, item2, item3, item4, item5 FROM player_shop WHERE nickname=?", (nickname,))
            if cursor.fetchone() is None: 
                player_shop_to = player_shop()
                player_shop_to.nickname = nickname
                player_shop_to.item1 = 1
                player_shop_to.item2 = 0
                player_shop_to.item3 = 0
                player_shop_to.item4 = 0
                player_shop_to.item5 = 0
            else:
                result_shop = cursor.fetchone()
                if result_shop:
                    item1, item2, item3, item4, item5 = result_shop
                    shop_DB = [item1, item2, item3, item4, item5]
                    shop_DB = ','.join(map(str, shop_DB))
                    shop_DB = str(shop_DB)
            conn.close()
            return JsonResponse({'coin_DB':  coin_DB,'best_score_DB': best_score_DB, 'shop_DB': shop_DB})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    
    nickname = "player_"
    number = str(random.randint(1, 100000))
    nickname = nickname+number
    data_render = {"nickname": nickname, "static_platform": static_platform, "static_background": static_background, "static_obstacle": static_obstacle}    

    if request.method == 'POST':
        nickname_from_base = request.POST.get("nickname")
        if nickname_from_base == "":
            nickname_from_base = "player_"
            number = str(random.randint(1, 100000))
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
            item1, item2, item3, item4, item5 = shop_to_db.split(',')
            nickname = data_api_to_DB['nickname_post']

            conn = sqlite3.connect('db.sqlite3')  
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM player_info WHERE nickname=?", (nickname,))
            if cursor.fetchone() is None: 
                player_info_to = player_info()
                player_info_to.nickname = nickname
                player_info_to.coin = coin_to_DB
                player_info_to.best_score = best_score_to_DB
                player_info_to.save()
            else:   
                cursor.execute("SELECT coin, best_score FROM player_info WHERE nickname=?", (nickname,))
                result = cursor.fetchone()
                if result:
                    coin_now, best_score_delete = result
                coin_sum = int(coin_now) + int(coin_to_DB)
                cursor.execute("UPDATE player_info SET coin=?, best_score=? WHERE nickname=?", (coin_sum, best_score_to_DB, nickname))
                conn.commit()
            cursor.close()
            conn.close()
            
            conn = sqlite3.connect('db.sqlite3') 
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM player_shop WHERE nickname=?", (nickname,))
            if cursor.fetchone() is None: # записи нет, создаем новую
                player_shop_to = player_shop()
                player_shop_to.nickname = nickname
                player_shop_to.item1 = item1
                player_shop_to.item2 = item2
                player_shop_to.item3 = item3
                player_shop_to.item4 = item4
                player_shop_to.item5 = item5
                player_shop_to.save()
            else:   # запись есть, обновляем значения в соответствующих столбцах
                cursor.execute("UPDATE player_shop SET item1=?, item2=?, item3=?, item4=?, item5=?  WHERE nickname=?", (item1, item2, item3, item4, item5, nickname))
                conn.commit()
            cursor.close()
            conn.close()

        return HttpResponseRedirect('/')

