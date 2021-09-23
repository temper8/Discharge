def default_astra_config():
    cfg = dict([
        ("astra_path", ["\home\Astra", "Astra folder", "Path to astra user folder"]),
        ("option1", ["op1", "option1", "option 1"]),
        ("exp_file", ["readme", "exp file", "exp file name"]),
        ("option2", ["op2", "option2", "option 2"]),
        ("equ_file", ["showdata", "equ file", "equ file name"])
    ])
    return ('Astra config', cfg)

def default_sbr_config():
    cfg = dict([
        ("sbr1", ["", "subrutine 1"]),
        ("sbr2", ["", "subrutine 2"]),
        ("sbr3", ["", "subrutine 3"]),
        ("sbr4", ["", "subrutine 4"]),
        ("sbr5", ["", "subrutine 5"])
    ])
    return ('Subrutine config', cfg)

def default_config():
    astra_cfg = default_astra_config()
    sbr_cfg = default_sbr_config()
    return dict([astra_cfg, sbr_cfg])    

import os
import ipywidgets as widgets
from IPython.display import display

output = []
config = []
all_items = []
config_file ='astra_config.json'
import json

def init_config():
    global config
    config = default_config()
    load_config()

def reset_config(b):
    global config
    output.clear_output()
    config = default_config()    
    copy_config()
    with output:
        print('reset_config')


def copy_config():
    for items, (_, cfg) in zip(all_items, config.items()):
        for w, (_,v) in zip(items, cfg.items()):
            if (w.value != v[0]):
                w.value = v[0]

def load_config():
    global config
    fp = os.path.abspath(config_file)
    if os.path.exists(fp):
        with open(fp) as json_file:
            config = json.load(json_file)

def load_config_click(b):
    global config
    output.clear_output()
    load_config()
    copy_config()   
    with output:
        print('load_config')

def save_config():
    fp = os.path.abspath(config_file)
    with open( fp , "w" ) as write:
        json.dump( config , write, indent = 2 )

def save_changes(b):
    output.clear_output()
    no_changes = True
    # можно сделать лучше - по ключам проходится
    for items, (_, cfg) in zip(all_items, config.items()):
        for w, (_,v) in zip(items, cfg.items()):
            if (w.value != v[0]):
                no_changes = False
                v[0] = w.value
                with output:
                    print(w.value, v)
    if no_changes:
        with output:
            print("no changes")
    else:                
        save_config()
        with output:
            print("save config")

import shutil   
def prepare_astra(b):
    astra_home = config['Astra config']['astra_path'][0]
    exp_file = config['Astra config']['exp_file'][0]
    exp_path = astra_home + '/exp/' + exp_file
    equ_file = config['Astra config']['equ_file'][0]
    equ_path = astra_home + '/equ/' + equ_file
    with output:
            print("Astra home " + astra_home)    
            shutil.copyfile(exp_file, exp_path)
            shutil.copyfile(equ_file, equ_path)    
            print(" copy " + exp_file + ' to ' + exp_path)
            print(" copy " + equ_file + ' to ' + equ_path)
            print(" Please run astra by command: ./a4/.exe/astra " + exp_file + ' ' + equ_file)


def widget():
    global all_items
    global output
    output = widgets.Output()
    tab_children = []
    all_items = []
    for _, cfg in config.items():
        items = [widgets.Text(value=v[0], sync=True, description=v[1], disabled=False) for key, v in cfg.items() ]
        all_items.append(items)
        tab_children.append(widgets.GridBox(items, layout=widgets.Layout(grid_template_columns="repeat(2, 400px)")))
    tab = widgets.Tab()
    tab.children = tab_children
    for id, p in enumerate(config.items()):
        tab.set_title(id, p[0])

    save_btn = widgets.Button(
        description='Save config',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Save config',
        icon='check' # (FontAwesome names without the `fa-` prefix)
       
    )
    load_btn = widgets.Button(
        description='Load config',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Load config',
        icon='check' # (FontAwesome names without the `fa-` prefix)
    )
    reset_btn = widgets.Button(
        description='Rest config',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Reset config',
        icon='check' # (FontAwesome names without the `fa-` prefix)
    )    
    prepare_btn = widgets.Button(
        description='Prepare to run astra',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Prepare to run astra',
        icon='check' # (FontAwesome names without the `fa-` prefix)
    )    

    save_btn.on_click(save_changes)
    load_btn.on_click(load_config_click)
    reset_btn.on_click(reset_config)
    prepare_btn.on_click(prepare_astra)
    
    btn_box = widgets.HBox([load_btn, save_btn, reset_btn, prepare_btn])
    return widgets.VBox([widgets.Label('Astra configuration'), tab, btn_box, output])

def summary():
    init_config()
    print(" ======  ASTRA summary =====")
    astra_home = config['Astra config']['astra_path']
    exp_file = config['Astra config']['exp_file']
    equ_file = config['Astra config']['equ_file']
    
    print('{0:12}  {1}'.format(astra_home[1], astra_home[0]))
    print('{0:12}  {1}'.format(exp_file[1], exp_file[0]))
    print('{0:12}  {1}'.format(equ_file[1], equ_file[0]))