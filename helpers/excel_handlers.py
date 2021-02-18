import pandas as pd
import json
from sekolah.models import Kelas
from helpers import active_semester, active_tp

def append_df_to_excel(filename, df, sheet_name='Sheet1', startrow=None,
                       truncate_sheet=False, 
                       **to_excel_kwargs):
    # ignore [engine] parameter if it was passed
    if 'engine' in to_excel_kwargs:
        to_excel_kwargs.pop('engine')

    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        writer.save()

def extract_and_clean_siswa(file):
    excel = pd.read_excel(file, dtype={'NIS':str, 'NISN':str})
    json_string = json.loads(excel.to_json(orient='records', date_format='iso'))

    tp = active_tp()
    cleaned_json = []
    for data in json_string:
        if not data['NISN'].startswith('00'):
            data['NISN'] = '00'+data['NISN']
        data['NISN'] = data['NISN'][0:10]
        data['NIS'] = data['NIS'][0:9]
        
        data['Tanggal Lahir'] = data['Tanggal Lahir'][0:10]
        if data['Gender'].lower() == 'pria' or data['Gender'].lower() == 'laki-laki':
            data['Gender'] = 'P'
        else:
            data['Gender'] = 'W'
        
        try:
            data['Kelas'] = data['Kelas'].replace(' ', '-')
            data['Kelas'] = Kelas.objects.get(nama=data['Kelas'], tahun_pelajaran=tp)
        except Kelas.DoesNotExist:
            data['Kelas'] = None
        except AttributeError:
            data['Kelas'] = None
            
        siswa = {}
        for key, value in data.items():
            key = str(key).lower().replace(' ', '_')
            siswa[key] = value
        cleaned_json.append(siswa)

    return cleaned_json