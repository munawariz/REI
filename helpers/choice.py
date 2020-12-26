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
    ('1', 'Ganjil'),
    ('2', 'Genap')
]

MATAPELAJARAN_CHOICE = [
    ('NA', 'Normatif Adaptif'),
    ('WS', 'Kejuruan'),
    ('MULOK', 'Muatan Lokal')
]

def tingkat_list_decide(tingkat_sekolah):
    if tingkat_sekolah:
        if tingkat_sekolah.tingkat == 'SMK':
            return [
                ('1', 'I'),
                ('2', 'II'),
                ('3', 'III'),
                ('4', 'IV'),
                ('5', 'V'),
                ('6', 'VI'),
            ]
        elif tingkat_sekolah.tingkat == 'SMP':
            return [
                ('7', 'VII'),
                ('8', 'VIII'),
                ('9', 'IX'),            
            ]
        elif tingkat_sekolah.tingkat == 'SMA':
            return [
                ('10', 'X'),
                ('11', 'XI'),
                ('12', 'XII'),            
            ]
        elif tingkat_sekolah.tingkat == 'SMK':
            return [
                ('10', 'X'),
                ('11', 'XI'),
                ('12', 'XII'),
                ('13', 'XIII'),
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