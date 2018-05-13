from django.shortcuts import render

def home(request):
    if request.method == 'POST':
        article_interaction = request.data.get('database', default = 0)
        if article_interaction == 'generation':
        elif article_interaction == 'hover':
        elif article_interaction == 'click':
        else:
            return HttpResponse('Error!')

    return render(request, 'main/home.html')
