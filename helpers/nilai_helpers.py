from siswa.models import MataPelajaran, Nilai, NilaiEkskul

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

def zip_eksnilai(siswa, semester):
    nilai_ekskul = NilaiEkskul.objects.filter(siswa=siswa, semester=semester)
    
    list_id_nilai = [obj.pk for obj in nilai_ekskul]
    list_id_ekskul = [obj.ekskul.pk for obj in nilai_ekskul]
    list_ekskul = [obj.ekskul for obj in nilai_ekskul]
    list_nilai = [obj.nilai for obj in nilai_ekskul]

    return zip(list_id_nilai, list_id_ekskul, list_ekskul, list_nilai)