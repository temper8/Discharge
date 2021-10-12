import os
import shutil
import ipywidgets as widgets
from IPython.display import display
import json
import matplotlib.pyplot as plt
import astra
import datetime

output = []
wv1 = []
wv2 = []
w_exp = []
w_equ = []
w_text = []
w_home = []
w_comp = []
w_race = []
w_copy_sbr = []

import astra_zip
import ray_tracing

def clear_folder_contents(path):
    print(' Clear folder: ' + path)
    files = next(os.walk(path), (None, None, []))[2]
    for f in files:
        os.remove(os.path.join(path, f))

def copy_file(src, dst):
    try:
        shutil.copyfile(src, dst)
        print(f" copy {src} to {dst}")
 
    except shutil.SameFileError:
        print("Source and destination represents the same file.")
 
    except IsADirectoryError:
        print("Destination is a directory.")
 
    except PermissionError:
        print("Permission denied.")
 
    except:
        print(f"Error occurred while copying file: {src} to {dst}")



def prepare_astra_to_run():
    cfg = astra.config['Astra config']
    astra_home = cfg['astra_path'][0] 
    exp_file = cfg['exp_file'][0]
    exp_src = 'exp_equ/' + exp_file    
    exp_dst = astra_home + '/exp/' + exp_file
    equ_file = cfg['equ_file'][0]
    equ_src = 'exp_equ/' + equ_file
    equ_dst = astra_home + '/equ/' + equ_file
    dat_file = 'rt_cfg.dat'
    dat_path = astra_home + '/lhcd/' + dat_file
    out_folder = astra_home + '/lhcd/out' 
    dat_folder = astra_home + '/dat' 
    sbr_list = next(os.walk(os.path.abspath('sbr/')), (None, None, []))[2]
 
    print("Astra home " + astra_home)    
    copy_file(exp_src, exp_dst)
    copy_file(equ_src, equ_dst)    
    copy_file('data/'+dat_file, dat_path)
    clear_folder_contents(out_folder)
    clear_folder_contents(dat_folder)
               
    if cfg['copy_sbr'][0]:
        for sbr in sbr_list:
            sbr_file = 'sbr/'+ sbr
            srb_dst = astra_home + '/sbr/' + sbr
            copy_file(sbr_file, srb_dst)    
    print()
    print(" Please run astra by command: ./a4/.exe/astra " + exp_file + ' ' + equ_file)
    print()


def prepare_click(b):
    output.clear_output()
    with output:
        ray_tracing.load_parameters()
        ray_tracing.prepare_rt_dat()
        prepare_astra_to_run()

def pick_up_results(b):
    global output
    output.clear_output()
    with output:
        print(w_race.value)
        astra_zip.pack_all(w_race.value)


def generate_race_name(prefix):
    dt_string = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    return '{0}_{1}.zip'.format(prefix, dt_string)

def update_widget():
    astra.init_config()
    w_exp.value = astra.config['Astra config']['exp_file'][0]
    w_equ.value = astra.config['Astra config']['equ_file'][0]
    w_copy_sbr.value = astra.config['Astra config']['copy_sbr'][0]
    w_home.value = astra.config['Astra config']['astra_path'][0]
    w_comp.value = astra.config['Astra config']['comp_name'][0]    
    w_race.value = generate_race_name(astra.config['Astra config']['comp_name'][0])
    wv1.value = True
    wv2.value = True

def update_btn_click(b):
    update_widget()

def widget():
    global output
    global wv1
    global wv2
    global w_exp
    global w_equ    
    global w_home
    global w_comp   
    global w_race
    global w_copy_sbr


    output = widgets.Output()

    wv1 = widgets.Valid( value=False,  description='Astra Config')
    wv2 = widgets.Valid( value=False,  description='RT Config')

    w_exp = widgets.Text(value='exp_file', sync=True, description='exp file', disabled=True)
    w_equ = widgets.Text(value='equ_file', sync=True, description='equ file', disabled=True)
    w_copy_sbr =  widgets.Checkbox(value=False, description='copy sbr', disabled=True)
    w_home = widgets.Text(value='astra path', sync=True, description='Astra:', disabled=True, 
                                    layout=widgets.Layout(width='400px'))
    w_comp = widgets.Text(value='noname', sync=True, description='comp name', disabled=True, layout=widgets.Layout(width='200px'))

    w_race = widgets.Text(value='noname', sync=True, description='Race name', disabled=False, layout=widgets.Layout(width='400px'))


    update_btn = widgets.Button(
        description='Update',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Update parameters',
        icon='check' # (FontAwesome names without the `fa-` prefix)
    )

    prepare_btn = widgets.Button(
        description='Prepare to run',
        disabled=False,
        button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Prepare to run',
        icon='check' # (FontAwesome names without the `fa-` prefix)
    )   
       
    pick_up_btn = widgets.Button(
        description='Pick up results',
        disabled=False,
        button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Pick up results',
        icon='check' # (FontAwesome names without the `fa-` prefix)
    )   

    update_btn.on_click(update_btn_click)
    prepare_btn.on_click(prepare_click)
    pick_up_btn.on_click(pick_up_results)
    update_widget()

    v_box = widgets.HBox([wv1,  wv2])
    v_box2 = widgets.HBox([w_exp,  w_equ, w_copy_sbr])
    v_box3 = widgets.HBox([w_home,  w_comp])
    btn_box = widgets.HBox([update_btn,  prepare_btn, pick_up_btn])
    title = widgets.Label('Astra run configuration')
    return widgets.VBox([title, v_box, v_box2, v_box3, w_race, btn_box, output])         
    

