from django.http import request
from django.shortcuts import render
from django.views.generic import View

def placeholder(request):
    return render(request, 'index.html')

class dashboard(View):
    def get(self, request):
        return render(request, 'pages/dashboard.html')