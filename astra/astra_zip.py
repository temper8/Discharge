from zipfile import ZipFile
from datetime import datetime
import zipfile
import os
import astra

my_zip_file = ''

def set_zip_file(f):
    global my_zip_file
    my_zip_file = f

def new_zip_file():
    global my_zip_file
    dt_string = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    my_zip_file = 'race_{0}.zip'.format(dt_string)

def pack_all():
    new_zip_file()
    pack_config()
    astra.init_config()
    astra_home = astra.config['Astra config']['astra_path'][0]
    src = astra_home + '/lhcd/out' 
    dst = '/lhcd/out/'
    pack_folder_to_ZipFile(src,dst)
    print( ' pack folder: ' + dst)

def pack_config():
    with ZipFile('races/'+ my_zip_file, 'w', compression=zipfile.ZIP_BZIP2, compresslevel = 9) as zip:
        zip.write("astra_config.json")      
        zip.write("ray_tracing_cfg.json")      

def pack_folder_to_ZipFile(src, dst):
    
    filenames = next(os.walk(src), (None, None, []))[2]
    with ZipFile('races/'+ my_zip_file, 'a', compression=zipfile.ZIP_BZIP2, compresslevel = 9) as zip:
        # writing each file one by one
        for file in filenames:
            zip.write(src + "/" + file, dst + file)    

import json

def get_astra_config(f):
    with ZipFile('races/'+ f) as zip:
        with zip.open('astra_config.json') as myfile:
                config = json.load(myfile)
    return config