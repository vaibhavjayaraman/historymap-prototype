from django.http import HttpResponse 

def no_wiki_article_icon(request):
    image_data = "pictures/no_wiki_article.png"
    with open(image_data, "rb") as f:
        return HttpResponse(f.read(), content_type="image/png")
    return HttpResponse(image_data, content_type="image/png")
