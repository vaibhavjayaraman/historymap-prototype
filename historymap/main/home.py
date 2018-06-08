from django.shortcuts import render
from historymap.main.models import Article
from historymap.main.models import Year
from historymap.users.models import UserArticle
from historymap.users.models import UserYear
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from datetime import datetime
import json
from django.http import JsonResponse

def item_item_recommender_results(user):
    """Returns recommended articles that one should visit based off previous visits and other users"""
    return None

def wiki_article_post_request(request)
    """Handles analytics for when wiki_articles are interacted with"""
    user_auth = False
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

def year_post_request(request):
    """Handles analytics for when someone interacts with a particular year."""
    user_auth = True
    year = request.POST.get('year')
    user = request.user
    year_obj = None
    user_year_obj = None
    wiki_year_timeline = None
    with transaction.atomic():
        try:
            year_obj = Year.objects.select_for_update().get(year = year)
        except ObjectDoesNotExist:
            year_obj = Year(year)
        if request.user.is_authenticated:
            try:
                user_year_obj = UserYear.objects.select_for_update().get(year = year, user = user)
            except ObjectDoesNotExist:
                user_year_obj = UserYear(year, user)
        year_obj.times_requested += 1
        wiki_year_timeline = year_obj.wikipedia_timeline
        year_obj.save()

    if wiki_year_timeline == None:
        wiki_year_timeline = "We are currently working to add timeline data to this year!"
    if user_year_obj != None:
        user_year_obj.times_requested += 1
        user_year_obj.last_visited = datetime.now()
        user_year_obj.save()

    return wiki_year_timeline

def wiki_year_timeline(request):
    timeline = year_post_request(request)
    data = {
            'timeline': timeline,
    }
    return JsonResponse(data)
    
def home(request):
    user = None
    i2i_rs = None
    if request.method == 'POST':
        if request.name == "wiki_article":
            wiki_article_post_request(request)
    if request.user.is_authenticated:
        user = request.user
        item_item_rs = item_item_recommender_results(user)
        i2i_rs = json.dumps(item_item_rs)
    args = {'user': user, 'i2i_collab_filter': i2i_rs}
    return render(request, 'main/home.html', args)
