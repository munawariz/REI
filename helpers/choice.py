GENDER_CHOICE = [
    ('P', 'Pria'),
    ('W', 'Wanita')
]

TINGKAT_SEKOLAH = [
    ('SD', 'Sekolah Dasar'),
    ('SMP', 'Sekolah Menengah Pertama'),
    ('SMA', 'Sekolah Menengah Atas'),
    ('SMK', 'Sekolah Menengah Kejuruan'),
]

SEMESTER_CHOICE = [
    ('Ganjil', 'Ganjil'),
    ('Genap', 'Genap')
]

MATAPELAJARAN_CHOICE = [
    ('NA', 'Normatif Adaptif'),
    ('WS', 'Kejuruan'),
    ('MULOK', 'Muatan Lokal')
]

def tingkat_choice(sekolah):
    if sekolah:
        if sekolah.tingkat == 'SD':
            return [
                ('1', '1'),
                ('2', '2'),
                ('3', '3'),
                ('4', '4'),
                ('5', '5'),
                ('6', '6'),
            ]
        elif sekolah.tingkat == 'SMP':
            return [
                ('7', '7'),
                ('8', '8'),
                ('9', '9'),            
            ]
        elif sekolah.tingkat == 'SMA':
            return [
                ('10', '10'),
                ('11', '11'),
                ('12', '12'),            
            ]
        elif sekolah.tingkat == 'SMK':
            return [
                ('10', '10'),
                ('11', '11'),
                ('12', '12'),
                ('13', '13'),
            ]
        else:
            return [
                ('1', '1'),
                ('2', '2'),
                ('3', '3'),
                ('4', '4'),
                ('5', '5'),
                ('6', '6'),
                ('7', '7'),
                ('8', '8'),
                ('9', '9'), 
                ('10', '10'),
                ('11', '11'),
                ('12', '12'),
                ('13', '13'),
            ]

KELAS_CHOICE = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
]

JENIS_EKSKUL = [
    ('Kepemimpinan', 'Kepemimpinan'),
    ('Keagamaan', 'Keagamaan'),
    ('Kesenian', 'Kesenian'),
    ('Olahraga', 'Olahraga'),              
    ('Lain-Lain', 'Lain-Lain'),
]

NILAI_EKSKUL = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
]

TINGKAT_KELAS_CHOICE = [
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6', '6'),
            ('7', '7'),
            ('8', '8'),
            ('9', '9'), 
            ('10', '10'),
            ('11', '11'),
            ('12', '12'),
            ('13', '13'),
        ]

TINGKAT_GELAR_CHOICE = [
    ('A.P.', 'Diploma 1'),
    ('A.Ma.', 'Diploma 2'),
    ('A.Md.', 'Diploma 3'),
    ('A.', 'Diploma 4'),
    ('S.', 'Sarjana'),
    ('M.', 'Magister'),
    ('Dr.', 'Doktor'),
]

JURUSAN_GELAR_CHOICE = (
    ('Administrasi', (
            ('A.B.', 'Administrasi Bisnis'),
            ('Pn.', 'Administrasi Fiskal'),
            ('Adm.', 'Administrasi Negara'),
            ('A.P.', 'Administrasi Perkantoran'),
            ('I.P.', 'Ilmu Perpustakaan'),
        )
    ),
    ('Ekonomi', (
            ('Ak.', 'Akuntansi'),
            ('E.', 'Ilmu Ekonomi'),
            ('E.', 'Manajemen'),
        )
    ),
    ('Kesehatan', (
            ('Farm.', 'Farmasi'),
            ('Gz.', 'Ilmu Gizi'),
            ('Keb.', 'Kebidanan'),
            ('Ked.', 'Kedokteran'),
            ('K.G.', 'Kedokteran Gigi'),
            ('K.H.', 'Kedokteran Hewan'),
            ('Kep.', 'Keperawatan'),
            ('K.M.', 'Kesehatan Masyrakat'),
            ('Psi.', 'Psikologi'),
        )
    ),
    ('Kesenian', (
            ('Ds.', 'Desain Komunikasi Visual'),
            ('Ds.', 'Desain Produk'),
            ('Sn.', 'Seni Kriya'),
            ('Sn.', 'Seni Musik'),
            ('Sn.', 'Seni Rupa'),
            ('Sn.', 'Seni Tari'),
        )
    ),
    ('Ilmu Budaya', (
            ('Hum.', 'Humaniora'),
            ('Fil.', 'Filsafat'),
            ('Hum.', 'Ilmu Sejarah'),
            ('Par.', 'Pariwisata'),
            ('S.', 'Sastra'),
        )
    ),
    
    ('Matematika & IPA', (
            ('Si.', 'Astronomi'),
            ('Si.', 'Biologi'),
            ('Si.', 'Fisika'),
            ('Si.', 'Geofisika'),
            ('Si.', 'Geologi'),
            ('Si.', 'Kimia'),
            ('Si.', 'Matematika'),
            ('Stat.', 'Statistika'),
        )
    ),
    ('Pendidikan', (
            ('Pd.', 'Bimbingan Konseling'),
            ('Pd.', 'Kebijakan Pendidikan'),
            ('Pd.', 'Manajemen Pendidikan'),
            ('Pd.', 'Pendidikan Luar Biasa'),
            ('Pd.', 'Pendidikan Luar Sekolah'),
            ('Pd.', 'PGPAUD'),
            ('Pd.', 'PGSD'),
            ('Pd.', 'Teknologi Pendidikan'),
        )
    ),
    ('Pertanian', (
            ('P.', 'Agribisnis'),
            ('P.', 'Agroteknologi'),
            ('P.', 'Ilmu Tanah'),
            ('Hut.', 'Kehutanan'),
            ('Pi.', 'Perikanan'),
            ('T.P.', 'Teknologi Hasil Pertanian'),
        )
    ),
    ('Sosial', (
            ('Ant.', 'Antropologi Sosial'),
            ('H.Int.', 'Hubungan Internasional'),
            ('H.', 'Hukum'),
            ('Si.', 'Geografi'),
            ('Sos.', 'Ilmu Kesejahteraan Sosial'),
            ('I.Kom.', 'Ilmu Komunikasi'),
            ('IP.', 'Ilmu Politik'),
            ('Sos.', 'Kriminologi'),
            ('Sos.', 'Sosiologi'),
        )
    ),
    ('Teknik', (
            ('Ars.', 'Arsitektur'),
            ('Kom.', 'Ilmu Komputer'),
            ('Kom.', 'Sistem Informasi'),
            ('Kom.', 'Teknik Informatika'),
            ('T.', 'Teknik Bioproses'),
            ('T.', 'Teknik Elektro'),
            ('T.', 'Teknik Elektronika'),
            ('T.', 'Teknik Fisika'),
            ('T.', 'Teknik Geodesi'),
            ('T.', 'Teknik Geofisika'),
            ('T.', 'Teknik Geologi'),
            ('T.', 'Teknik Industri'),
            ('T.', 'Teknik Kelautan'),
            ('T.', 'Teknik Kimia'),
            ('T.', 'Teknik Telekomunikasi'),
            ('T.', 'Teknik Lingkungan'),
            ('T.', 'Teknik Metalurgi'),
            ('T.', 'Teknik Mekatronika'),
            ('T.', 'Teknik Mesin'),
            ('T.', 'Teknik Nuklir'),
            ('T.', 'Teknik Otomotif'),
            ('T.', 'Teknik Permniyakan'),
            ('T.', 'Teknik Pertambangan'),
            ('T.', 'Teknik Sipil'),
            ('T.', 'Teknik Transportasi Laut'),
        )
    ),
)