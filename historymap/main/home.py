from django.shortcuts import render
from historymap.main.models import Article
from historymap.users.models import UserArticle
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from datetime import datetime
import json

def item_item_recommender_results(user):
    """Returns recommended articles that one should visit based off previous visits and other users"""
    return None

def home(request):
    user_auth = False
    if request.method == 'POST':
        article_interaction = request.POST.get('interaction_type', default = 0)
        url = request.POST.get('url', default = 0)
        title = request.POST.get('title', default = 0)
        lat = request.POST.get('lat', default = None);
        lon = request.POST.get('lon', default = None);
        with transaction.atomic():
            try: 
                article = Article.objects.select_for_update().get(url = url, title = title, lat = lat, lon = lon)
            except ObjectDoesNotExist:
                article = Article(url = url, title = title, lat = lat, lon = lon)
            if request.user.is_authenticated and (article_interaction == 'hover' or article_interaction == 'click' or article_interaction == 'search'):
                #need to evaluate all of those conditions since we do not want a user_article to be created on generation
                user_auth = True 
                try:
                    user_article = UserArticle.objects.select_for_update().get(url = url, title = title, user = request.user)
                    user_article.last_visited = datetime.now()
                except ObjectDoesNotExist:
                    user_article = UserArticle(url = url, title = title, user = request.user, )
            if article_interaction == 'generation':
                article.times_generated += 1
            elif article_interaction == 'hover':
                article.times_hovered_over += 1
                if request.user.is_authenticated:
                    user_article.times_hovered_over += 1
            elif article_interaction == 'click':
                article.times_clicked_on += 1
                if request.user.is_authenticated:
                    user_article.times_clicked_on += 1
            elif article_interaction == "search":
                article.times_searched += 1
                if request.user.is_authenticated:
                    user_article.times_searched += 1
            else:
                return HttpResponse('Error')
            article.save()
            if user_auth:
                user_article.save()
    if request.user.is_authenticated:
        item_item_rs = item_item_recommender_results(request.user)
        i2i_rs = json.dumps(item_item_rs)
        args = {'user': request.user, 'i2i_collab_filter': i2i_rs}
    else:
        args = {'user': None, 'i2i_collab_filter': None}
    return render(request, 'main/home.html', args)
