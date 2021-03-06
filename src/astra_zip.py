from zipfile import ZipFile
from datetime import datetime
import zipfile
import os
import astra

my_zip_file = ''

def set_zip_file(f):
    global my_zip_file
    my_zip_file = f

def pack_all(file_name):
    global my_zip_file
    my_zip_file = file_name
    pack_config()
    astra.init_config()
    astra_home = astra.config['Astra config']['astra_path'][0]
    src = astra_home + '/lhcd/out' 
    dst = '/lhcd/out'
    pack_folder_to_ZipFile(src,dst)
    print( ' pack folder: ' + dst)
    src = astra_home + '/dat' 
    dst = '/dat'
    pack_folder_to_ZipFile(src,dst)
    print( ' pack folder: ' + dst)
    pack_folder_to_ZipFile(os.path.abspath('sbr'),'/sbr')
    print('pack sbr')



def pack_config():
    with ZipFile('races/'+ my_zip_file, 'w', compression=zipfile.ZIP_BZIP2, compresslevel = 9) as zip:
        zip.write("data/astra_config.json", "astra_config.json",)      
        zip.write("data/ray_tracing_cfg.json", "ray_tracing_cfg.json")      

def pack_folder_to_ZipFile(src, dst):
    
    filenames = next(os.walk(src), (None, None, []))[2]
    #print(filenames)
    with ZipFile('races/'+ my_zip_file, 'a', compression=zipfile.ZIP_BZIP2, compresslevel = 9) as zip:
        # writing each file one by one
        for file in filenames:
            zip.write(src + "/" + file, dst + "/" + file)    

import json

def get_astra_config(f):
    with ZipFile('races/'+ f) as zip:
        with zip.open('astra_config.json') as myfile:
                config = json.load(myfile)
    return config

def get_rt_parameters(f):
    with ZipFile('races/'+ f) as zip:
        with zip.open('ray_tracing_cfg.json') as myfile:
                cfg = json.load(myfile)
    return cfg