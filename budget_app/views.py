from django.shortcuts import render



def home_page(request):
    template_name = "homepage.html"
    return render(request, template_name)