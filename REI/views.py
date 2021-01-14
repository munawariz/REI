from django.shortcuts import render

def error_404(request, exception=None):
    request.session['page'] = 'Error 404'
    return render(request, 'pages/errors/404.html')