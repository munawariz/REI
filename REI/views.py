from django.shortcuts import render

def error_404(request, exception=None):
    request.session['page'] = 'Error 404'
    return render(request, 'pages/error/404.html')

def error_500(request, exception=None):
    request.session['page'] = 'Error 500'
    return render(request, 'pages/error/500.html')

def about_dev(request):
    request.session['page'] = 'About Dev'
    return render(request, 'pages/developer/about.html')