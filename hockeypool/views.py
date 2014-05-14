from django.shortcuts import render
from models import *

def index(request):
        posts = Post.objects.all().order_by("id")
        posts = posts.reverse()[:5]
	mainFrame = { 'posts' : posts }
	sideFrame = {}
        context = {'page_name' : 'Home', 'main' : mainFrame, 'side' : sideFrame}
        return render(request, 'hockeypool/index.html', context)



