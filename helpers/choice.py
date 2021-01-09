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
            ('1', 'I'),
            ('2', 'II'),
            ('3', 'III'),
            ('4', 'IV'),
            ('5', 'V'),
            ('6', 'VI'),
            ('7', 'VII'),
            ('8', 'VIII'),
            ('9', 'IX'), 
            ('10', 'X'),
            ('11', 'XI'),
            ('12', 'XII'),
            ('13', 'XIII'),
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
            ('1', 'I'),
            ('2', 'II'),
            ('3', 'III'),
            ('4', 'IV'),
            ('5', 'V'),
            ('6', 'VI'),
            ('7', 'VII'),
            ('8', 'VIII'),
            ('9', 'IX'), 
            ('10', 'X'),
            ('11', 'XI'),
            ('12', 'XII'),
            ('13', 'XIII'),
        ]