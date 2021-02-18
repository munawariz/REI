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