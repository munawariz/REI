from sekolah.models import Ekskul, KKM, TahunPelajaran
from siswa.models import MataPelajaran, Nilai, NilaiEkskul, Siswa
from . import active_tp

def get_active_kelas(nis):
    siswa = Siswa.objects.get(nis=nis)
    return siswa.kelas.get(tahun_pelajaran=active_tp())

def pengetahuan(matapelajaran, siswa, semester):
    nil = Nilai.objects.filter(matapelajaran=matapelajaran, siswa=siswa, semester=semester)
    if nil:
        for nil in nil:
            return nil.pengetahuan
    else:
        return 0

def keterampilan(matapelajaran, siswa, semester):
    nil = Nilai.objects.filter(matapelajaran=matapelajaran, siswa=siswa, semester=semester)
    if nil:
        for nil in nil:
            return nil.keterampilan
    else:
        return 0

def get_kkm(matapelajaran, tp):
    return KKM.objects.get_or_create(matapelajaran=matapelajaran, tahun_pelajaran=tp)[0]

def zip_pelnilai(siswa, semester):
    kelas = siswa.kelas.get(tahun_pelajaran=semester.tahun_pelajaran)
    matapelajaran = MataPelajaran.objects.filter(kelas=kelas).order_by('kelompok', 'nama')
        
    list_id = [matapelajaran.pk for matapelajaran in matapelajaran]
    list_pelajaran = [matapelajaran.nama for matapelajaran in matapelajaran]
    list_pengetahuan = [pengetahuan(matapelajaran, siswa, semester) for matapelajaran in matapelajaran]
    list_keterampilan = [keterampilan(matapelajaran, siswa, semester) for matapelajaran in matapelajaran]

    return zip(list_id, list_pelajaran, list_pengetahuan, list_keterampilan)

def zip_nilrapor(siswa, semester):
    kelas = siswa.kelas.get(tahun_pelajaran=semester.tahun_pelajaran)
    matapelajaran = MataPelajaran.objects.filter(kelas=kelas).order_by('kelompok', 'nama')
    tp = TahunPelajaran.objects.get(pk=semester.tahun_pelajaran.pk)
        
    list_id = [matapelajaran.pk for matapelajaran in matapelajaran]
    list_pelajaran = [matapelajaran.nama for matapelajaran in matapelajaran]
    list_pengetahuan = [pengetahuan(matapelajaran, siswa, semester) for matapelajaran in matapelajaran]
    list_kkmpeng = [get_kkm(matapelajaran, tp).pengetahuan for matapelajaran in matapelajaran]
    list_kkmket = [get_kkm(matapelajaran, tp).keterampilan for matapelajaran in matapelajaran]
    list_keterampilan = [keterampilan(matapelajaran, siswa, semester) for matapelajaran in matapelajaran]
    list_nilaiakhir = [((pengetahuan(matapelajaran, siswa, semester) + keterampilan(matapelajaran, siswa, semester)) / 2) for matapelajaran in matapelajaran]
    list_predikat = []
    list_statuspeng = [True if (pengetahuan(matapelajaran, siswa, semester) < get_kkm(matapelajaran, tp).pengetahuan) else False for matapelajaran in matapelajaran]
    list_statusket = [True if (keterampilan(matapelajaran, siswa, semester) < get_kkm(matapelajaran, tp).keterampilan) else False for matapelajaran in matapelajaran]

    for nilai in list_nilaiakhir:
        if nilai <= 100 and nilai >= 86:
            list_predikat.append('A')
        elif nilai <= 85 and nilai >= 71:
            list_predikat.append('B')
        elif nilai <= 70 and nilai >= 56:
            list_predikat.append('C')
        else:
            list_predikat.append('D')

    return zip(list_id, list_pelajaran, list_pengetahuan, list_kkmpeng, list_statuspeng, list_keterampilan, list_kkmket, list_statusket, list_nilaiakhir, list_predikat)

def zip_eksnilai(siswa, semester):
    nilai_ekskul = NilaiEkskul.objects.select_related('ekskul').filter(siswa=siswa, semester=semester)
    
    list_id_nilai = [obj.pk for obj in nilai_ekskul]
    list_id_ekskul = [obj.ekskul.pk for obj in nilai_ekskul]
    list_ekskul = [obj.ekskul for obj in nilai_ekskul]
    list_nilai = [obj.nilai for obj in nilai_ekskul]
    list_jenis = [obj.ekskul.jenis for obj in nilai_ekskul]

    return zip(list_id_ekskul, list_id_nilai, list_ekskul, list_nilai, list_jenis)

def zip_pelkkm(queryset_matapelajaran, tp):
    list_matapelajaran = [MataPelajaran.objects.get(pk=matapelajaran.pk) for matapelajaran in queryset_matapelajaran]
    list_kkm = [get_kkm(matapelajaran, tp) for matapelajaran in queryset_matapelajaran]

    return zip(list_matapelajaran, list_kkm)

def has_ekskul(siswa, semester):
    nilai_ekskul = NilaiEkskul.objects.select_related('ekskul').filter(siswa=siswa, semester=semester)
    if nilai_ekskul:
        return True
    else:
        return False

def has_mapel(kelas):
    mapel = MataPelajaran.objects.filter(kelas=kelas)
    if mapel:
        return True
    else:
        return False

def get_pengetahuan(siswa, semester, kelas):
    matapelajaran = MataPelajaran.objects.filter(kelas=kelas).order_by('kelompok', 'nama')
    return [pengetahuan(mapel, siswa, semester) for mapel in matapelajaran]

def get_keterampilan(siswa, semester, kelas):
    matapelajaran = MataPelajaran.objects.filter(kelas=kelas).order_by('kelompok', 'nama')
    return [keterampilan(mapel, siswa, semester) for mapel in matapelajaran]

def list_siswa_status(list_siswa, semester):
    finished = []
    unfinished = []
    status = {}
    kelas = get_active_kelas(list_siswa.values_list('nis', flat=True)[0])
    for siswa in list_siswa:
        if 0 in get_pengetahuan(siswa, semester, kelas) or 0 in get_keterampilan(siswa, semester, kelas):
            unfinished.append(siswa.nis)
            status[siswa] = False
        else:
            finished.append(siswa.nis)
            status[siswa] = True
    
    return finished, unfinished, status

        