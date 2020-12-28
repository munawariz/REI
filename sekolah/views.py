from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from django.views.generic import View, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from .models import Semester
from .forms import SemesterForm
from django.db.models.deletion import ProtectedError
from django.core.paginator import Paginator

@method_decorator(login_required, name='dispatch')
class list_semester(View):
    def get(self, request):
        if 'search' in request.GET and request.GET['search'] != '':
            list_semester = Semester.objects.filter(
                Q(tahun_mulai__icontains=request.GET['search']) |
                Q(tahun_akhir__icontains=request.GET['search']) |
                Q(semester__icontains=request.GET['search'])
            ).order_by('-tahun_mulai', '-tahun_akhir', '-semester')
        else:
            list_semester = Semester.objects.all().order_by('-tahun_mulai', '-tahun_akhir', '-semester')
        
        paginator = Paginator(list_semester, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        number_of_pages = [(number+1) for number in range(page_obj.paginator.num_pages)]
        context = {
            'list_semester': page_obj,
            'page_obj': page_obj,
            'create_form': SemesterForm(),
            'number_of_pages': number_of_pages,
        }
        return render(request, 'pages/semester.html', context)

class buat_semester(View):
    def post(self, request):
        semester_form = SemesterForm(request.POST)
        try:
            if semester_form.is_valid():
                semester = Semester.objects.create(
                    tahun_mulai=semester_form.cleaned_data['tahun_mulai'],
                    tahun_akhir=semester_form.cleaned_data['tahun_akhir'],
                    semester=semester_form.cleaned_data['semester'],
                    is_active=False)
            return redirect('list-semester')
        except ValidationError:
            return redirect(f"{reverse('list-semester')}?validation_error=True")

class aktifkan_semester(View):
    def get(self, request, semester):
        semester = Semester.objects.get(pk=semester)
        semester.is_active = True
        semester.save()
        return redirect('list-semester')

class hapus_semester(View):
    def get(self, request, semester):
        try:
            Semester.objects.get(pk=semester).delete()
            return redirect('list-semester')
        except ProtectedError:
            return redirect(f"{reverse('list-semester')}?protected_error=True")