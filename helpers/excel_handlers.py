import pandas as pd
import json
from sekolah.models import Kelas
from helpers import active_semester

def extract_and_clean_siswa(file):
    excel = pd.read_excel(file, dtype={'NIS':str, 'NISN':str})
    json_string = json.loads(excel.to_json(orient='records', date_format='iso'))

    models_cols = ['nis', 'nisn', 'nama', 'email', 'tempat_lahir', 'tanggal_lahir', 
    'gender', 'agama', 'alamat', 'sekolah_asal', 'diterima_di_tingkat', 
    'nama_ayah', 'nama_ibu', 'nama_wali', 'kelas']
    semester = active_semester()
    cleaned_json = []
    for data in json_string:
        if data['NISN']: 
            data['NISN'] = data['NISN'][0:10]
        if data['NIS']:
            data['NIS'] = data['NIS'][0:9]
        data['Tanggal Lahir'] = data['Tanggal Lahir'][0:10]
        if str(data['Gender']).lower() == 'pria' or str(data['Gender']).lower() == 'laki-laki':
            data['Gender'] = 'P'
        else:
            data['Gender'] = 'W'
        data['Kelas'] = str(data['Kelas']).replace(' ', '-')
        try:
            data['Kelas'] = Kelas.objects.get(nama=data['Kelas'], semester=semester)
        except Kelas.DoesNotExist:
            data['Kelas'] = None

        values = data.values()
        siswa = {}
        for key, value in zip(models_cols, values):
            siswa[key] = value
        cleaned_json.append(siswa)

    return cleaned_json