import os
import ipywidgets as widgets
from IPython.display import display
from ipywidgets.widgets.widget_button import ButtonStyle
from ipywidgets.widgets.widget_layout import Layout

def default_config():
    cfg = {
        'Astra config':{
            "astra_path": ["\home\Astra", "Astra folder", "Path to astra user folder"],
            "comp_name": ["noname", "Computer name", "option 1"],
            "exp_file": ["readme", "exp file", "exp file name"],
            "equ_file": ["showdata", "equ file", "equ file name"],
            "copy_sbr": [False, "Copy subroutine", "Auto copy subroutine"]
        },
        'Subrutine config': {
            "sbr1": ["", "subrutine 1"],
            "sbr2": ["", "subrutine 2"],
            "sbr3": ["", "subrutine 3"],
            "sbr4": ["", "subrutine 4"],
            "sbr5": ["", "subrutine 5"]
        }
    }
    return cfg


output = []
config = []
all_items = []
config_file ='data/astra_config.json'
import json

def init_config():
    global config
    config = default_config()
    load_config()

def reset_config(b):
    global config
    output.clear_output()
    config = default_config()    
    update_widgets()
    with output:
        print('reset_config')


def update_widgets():
    widget_list[0].value = config['Astra config']['astra_path'][0]
    widget_list[1].value = config['Astra config']['comp_name'][0]    
    widget_list[2].value = config['Astra config']['exp_file'][0]
    widget_list[3].value = config['Astra config']['equ_file'][0]
    widget_list[4].value = config['Astra config']['copy_sbr'][0]    
        

def load_config():
    global config
    fp = os.path.abspath(config_file)
    if os.path.exists(fp):
        with open(fp) as json_file:
            cfg = json.load(json_file)
            config['Astra config'].update(cfg['Astra config'])

def load_config_click(b):
    global config
    output.clear_output()
    load_config()
    update_widgets()   
    with output:
        print('load_config')

def save_config():
    config['Astra config']['astra_path'][0] = widget_list[0].value 
    config['Astra config']['comp_name'][0] = widget_list[1].value     
    config['Astra config']['exp_file'][0] = widget_list[2].value 
    config['Astra config']['equ_file'][0] = widget_list[3].value 
    config['Astra config']['copy_sbr'][0] = widget_list[4].value 
    fp = os.path.abspath(config_file)
    with open( fp , "w" ) as write:
        json.dump( config , write, indent = 2 )

def save__config_click(b):
    output.clear_output()
    save_config()
    with output:
        print("Save config")


widget_list = []            
def widget():
    global widget_list
    global output
    output = widgets.Output()

    cfg = config['Astra config']
    widget_list.append(widgets.Text(
                                    value=cfg['astra_path'][0], 
                                    sync=True,
                                    description=cfg['astra_path'][1], 
                                    disabled=False, 
                                    layout=widgets.Layout(width='600px')))
    widget_list.append(widgets.Text(
                                    value=cfg['comp_name'][0], 
                                    sync=True,
                                    description=cfg['comp_name'][1], 
                                    disabled=False, 
                                    layout=widgets.Layout(width='300px')))                                    
    widget_list.append( widgets.Text(value=cfg['exp_file'][0], sync=True, description=cfg['exp_file'][1], disabled=False))
    widget_list.append( widgets.Text(value=cfg['equ_file'][0], sync=True, description=cfg['equ_file'][1], disabled=False))
    widget_list.append( widgets.Checkbox(value=cfg['copy_sbr'][0], description=cfg['copy_sbr'][1], disabled=False))

    path = os.path.abspath('exp_equ/')
    filenames = next(os.walk(path), (None, None, []))[2]
    exp_list = [f for f in filenames if f.endswith('exp') ]
    equ_list = [f for f in filenames if f.endswith('equ') ]

    def on_value_change(change):
        widget_list[2].value = change['new']
    def on_value_change2(change):
        widget_list[3].value = change['new']   

    w_exp = widgets.Select(
        options=exp_list,
        #value='',
        description='exp:',
        disabled=False
        )
    w_exp.observe(on_value_change, names='value')

    w_equ = widgets.Select(
        options=equ_list,
        #value='',
        description='equ:',
        disabled=False
        )    
    w_equ.observe(on_value_change2, names='value')        

    filenames = next(os.walk(os.path.abspath('sbr/')), (None, None, []))[2]
    w_sbr = widgets.Select(
        options=filenames,
        #value='',
        description='sbr:',
        disabled=False
    )   

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

    save_btn.on_click(save__config_click)
    load_btn.on_click(load_config_click)
    reset_btn.on_click(reset_config)

    
    btn_box = widgets.HBox([load_btn, save_btn, reset_btn])
    hb0 = widgets.HBox(widget_list[0:2])
    hb1 = widgets.HBox(widget_list[2:5])
    hb2 = widgets.HBox([w_exp, w_equ, w_sbr])
    header = widgets.Label('Astra configuration', layout = {'width': '100%'} )
    return widgets.VBox([header, hb0, hb1, hb2, btn_box, output])


def summary():
    init_config()
    print(" ======  ASTRA summary =====")
    astra_home = config['Astra config']['astra_path']
    exp_file = config['Astra config']['exp_file']
    equ_file = config['Astra config']['equ_file']
    
    print('{0:12}  {1}'.format(astra_home[1], astra_home[0]))
    print('{0:12}  {1}'.format(exp_file[1], exp_file[0]))
    print('{0:12}  {1}'.format(equ_file[1], equ_file[0]))