from django.http.response import Http404
from sekolah.models import MataPelajaran
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View, UpdateView
from .models import Absensi, Siswa, Nilai
from .forms import NilaiForm, SiswaForm, AbsenForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from helpers.nilai_helpers import zip_pelnilai
from helpers import calculate_age, active_semester

@method_decorator(login_required, name='dispatch')
class list_siswa(View):
    def get(self, request):
        if 'search' in request.GET and request.GET['search'] != '':
            list_siswa = Siswa.objects.filter(
                Q(kelas__semester=active_semester()) &
                (Q(nama__icontains=request.GET['search']) | Q(nis__istartswith=request.GET['search']) |
                Q(nisn__istartswith=request.GET['search']) | Q(email__icontains=request.GET['search']) |
                Q(tempat_lahir__icontains=request.GET['search']) | Q(tanggal_lahir__icontains=request.GET['search']) |
                Q(agama__icontains=request.GET['search']))
                ).order_by('nis')
        else:
            list_siswa = Siswa.objects.filter(kelas__semester=active_semester()).order_by('nis')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usia'] = calculate_age(context['object'].tanggal_lahir)
        return context

    def get_success_url(self):
        return reverse('detail-siswa', kwargs={'nis':self.kwargs['nis']})

@method_decorator(login_required, name='dispatch')
class nilai_siswa(View):
    def get(self, request, nis):
        active_siswa = Siswa.objects.get(nis=nis)
        
        context = {
            'siswa': active_siswa,
            'usia': calculate_age(active_siswa.tanggal_lahir),
            'data': zip_pelnilai(active_siswa, active_semester()),
        }
        return render(request, 'pages/nilai-siswa.html', context)

    def post(self, request, nis):
        try:                
            active_siswa = Siswa.objects.get(nis=nis)
            data = zip_pelnilai(active_siswa, active_semester())
            completed = True
            for id_, matapelajaran, pengetahuan, keterampilan in data:
                matapelajaran = MataPelajaran.objects.get(id=id_)
                nilai_pengetahuan = int(request.POST[f'pengetahuan-{id_}'])
                nilai_keterampilan = int(request.POST[f'keterampilan-{id_}'])
                if nilai_pengetahuan == 0 or nilai_keterampilan == 0:
                    completed = False
                obj, created = Nilai.objects.update_or_create(
                    siswa=active_siswa, matapelajaran=matapelajaran, semester=active_semester(),
                    defaults={'pengetahuan': nilai_pengetahuan, 'keterampilan': nilai_keterampilan}
                )
            return redirect('detail-siswa', nis=nis)
        except Siswa.DoesNotExist: 
            raise Http404

@method_decorator(login_required, name='dispatch')
class absen_siswa(View):
    def get(self, request, nis):
        active_siswa = Siswa.objects.get(nis=nis)
        absen, created = Absensi.objects.get_or_create(
            siswa=active_siswa, semester=active_semester(),
            defaults={'izin': 0, 'sakit': 0, 'bolos': 0})
        initial = {
            'izin': absen.izin,
            'sakit': absen.sakit,
            'bolos': absen.bolos,
        }
        absen_form = AbsenForm(initial=initial)
        context = {
            'siswa': active_siswa,
            'absen_form': absen_form,
        }
        return render(request, 'pages/absen-siswa.html', context)

    def post(self, request, nis):
        active_siswa = Siswa.objects.get(nis=nis)
        absen_form = AbsenForm(request.POST)
        if absen_form.is_valid():
            absen = Absensi.objects.filter(siswa=active_siswa, semester=active_semester())
            absen.update(
                izin=absen_form.cleaned_data['izin'],
                sakit=absen_form.cleaned_data['sakit'],
                bolos=absen_form.cleaned_data['bolos'])
            return redirect('detail-siswa', nis=nis)
        else:
            return redirect('absen-siswa', nis=nis)