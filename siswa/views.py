from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from django.views.generic import View, UpdateView
from .models import Siswa, Nilai
from .forms import NilaiForm, SiswaForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from helpers.configuration import semester as active_semester, calculate_age
@method_decorator(login_required, name='dispatch')
class list_siswa(View):
    def get(self, request):
        if 'search' in request.GET and request.GET['search'] != '':
            list_siswa = Siswa.objects.filter(
                Q(kelas__semester=active_semester) &
                (Q(nama__icontains=request.GET['search']) | Q(nis__istartswith=request.GET['search']) |
                Q(nisn__istartswith=request.GET['search']) | Q(email__icontains=request.GET['search']) |
                Q(tempat_lahir__icontains=request.GET['search']) | Q(tanggal_lahir__icontains=request.GET['search']) |
                Q(agama__icontains=request.GET['search']))
                ).order_by('nis')
        else:
            list_siswa = Siswa.objects.filter(kelas__semester=active_semester).order_by('nis')

        paginator = Paginator(list_siswa, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        number_of_pages = [(number+1) for number in range(page_obj.paginator.num_pages)]
        context = {
            'list_siswa': page_obj,
            'page_obj': page_obj,
            'number_of_pages': number_of_pages,
        }
        return render(request,  'pages/siswa.html', context)

@method_decorator(login_required, name='dispatch')
class detail_siswa(UpdateView):
    model = Siswa
    template_name = 'pages/detail-siswa.html'
    form_class = SiswaForm
    slug_field = 'nis'
    slug_url_kwarg = 'nis'
    success_url = '/dashboard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usia'] = calculate_age(context['object'].tanggal_lahir)
        return context