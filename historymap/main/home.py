from django.shortcuts import render
from historymap.main.models import Article
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import json

def item_item_recommender_results(user):
    """Returns recommended articles that one should visit based off previous visits and other users"""
    return None

def home(request):
    if request.method == 'POST':
        article_interaction = request.POST.get('interaction_type', default = 0)
        url = request.POST.get('url', default = 0)
        title = request.POST.get('title', default = 0)
        with transaction.atomic():
            try: 
                article = Article.objects.select_for_update().get(url = url, title = title)
            except ObjectDoesNotExist:
                article = Article(url = url, title = title)
            if article_interaction == 'generation':
                article.times_generated += 1
            elif article_interaction == 'hover':
                article.times_hovered_over += 1
            elif article_interaction == 'click':
                article.times_clicked_on += 1
            elif article_interaction == "search":
                article.times_searched += 1
            else:
                return HttpResponse('Error')
            article.save()
    if request.user.is_authenticated:
        item_item_rs = item_item_recommender_results(request.user)
        i2i_rs = json.dumps(item_item_rs)
        args = {'user': request.user, 'i2i_collab_filter': i2i_rs}
    else:
        args = {'user': None, 'i2i_collab_filter': None}
    print(args['user'])
    return render(request, 'main/home.html', args)
