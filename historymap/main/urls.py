from django.conf.urls import url
from historymap.main.home import wiki_year_timeline
from historymap.main.icon import no_wiki_article_icon
urlpatterns = [
        url(r'^wiki_timeline/$', wiki_year_timeline, name="wiki_year_timeline"), 
        url(r'^no_wiki_article_icon/$',no_wiki_article_icon, name="no_wiki_article_icon"),  
]
