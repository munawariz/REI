from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from django.views.generic import View, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from .models import Sekolah, Semester
from .forms import SekolahForm, SemesterForm
from django.db.models.deletion import ProtectedError
from django.core.paginator import Paginator
from REI.decorators import staftu_required
from helpers import get_initial, form_value

@method_decorator(login_required, name='dispatch')
class detail_sekolah(View):
    def get(self, request):
        sekolah = Sekolah.objects.get()
        sekolah_form = SekolahForm(initial=get_initial(sekolah))
        context = {
            'sekolah_form': sekolah_form,
        }
        return render(request, 'pages/detail-sekolah.html', context)

    def post(self, request):
        sekolah_form = SekolahForm(request.POST)
        if sekolah_form.is_valid():
            Sekolah.objects.update(**form_value(sekolah_form))
            return redirect('detail-sekolah')
    
@method_decorator(staftu_required, name='dispatch')
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

@method_decorator(staftu_required, name='dispatch')
class buat_semester(View):
    def post(self, request):
        semester_form = SemesterForm(request.POST)
        try:
            if semester_form.is_valid():
                semester = Semester.objects.create(**form_value(semester_form), is_active=False)
            return redirect('list-semester')
        except ValidationError:
            return redirect(f"{reverse('list-semester')}?validation_error=True")

@method_decorator(staftu_required, name='dispatch')
class aktifkan_semester(View):
    def get(self, request, semester):
        semester = Semester.objects.get(pk=semester)
        semester.is_active = True
        semester.save()
        return redirect('list-semester')

@method_decorator(staftu_required, name='dispatch')
class hapus_semester(View):
    def get(self, request, semester):
        try:
            Semester.objects.get(pk=semester).delete()
            return redirect('list-semester')
        except ProtectedError:
            return redirect(f"{reverse('list-semester')}?protected_error=True")