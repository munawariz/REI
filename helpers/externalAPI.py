import requests
from REI.settings import MEDIA_ROOT
import os

def avatarAPI(subjek):
    if subjek.nip: 
        output_dir = f'{MEDIA_ROOT}avatar/guru'
        image_name = subjek.nip
    else: 
        output_dir = f'{MEDIA_ROOT}avatar/siswa'
        image_name = subjek.nis
    image = requests.get(f'https://ui-avatars.com/api/?name={subjek.nama}&background=random&size=100')
    if not os.path.isdir(output_dir): os.makedirs(output_dir)
    if image.status_code == 200:
        with open(f"{output_dir}/{image_name}.png", 'wb') as f:
            f.write(image.content)
        f.close()
        return f"{output_dir}/{image_name}.png"
    else:
        raise Exception
    