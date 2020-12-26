from siswa.models import MataPelajaran, Nilai

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

def zip_pelnilai(siswa, semester):        
    matapelajaran = MataPelajaran.objects.filter(kelas=siswa.kelas)
        
    list_id = [matapelajaran.pk for matapelajaran in matapelajaran]
    list_pelajaran = [matapelajaran.nama for matapelajaran in matapelajaran]
    list_pengetahuan = [pengetahuan(matapelajaran, siswa, semester) for matapelajaran in matapelajaran]
    list_keterampilan = [keterampilan(matapelajaran, siswa, semester) for matapelajaran in matapelajaran]

    return zip(list_id, list_pelajaran, list_pengetahuan, list_keterampilan)