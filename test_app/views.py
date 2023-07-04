from django.shortcuts import render
from .forms import InputForm

def landing_page(request):
    context = {}
    context['form'] = InputForm()
    return render(request, 'landing.html', context)