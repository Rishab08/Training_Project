from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_view(request):
	return render(request, "pols/home.html")

def action(request):
	djtext=request.GET.get('email','default')
	print(djtext)
	return render(request,"pols/login.html")

	
