from django.conf.urls import url
from historymap.main.home import wiki_year_timeline
urlpatterns = [
        url(r'^wiki_timeline/$', wiki_year_timeline, name="wiki_year_timeline"), 
]
