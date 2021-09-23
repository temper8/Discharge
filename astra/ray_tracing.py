def default_pp():
    p = dict([
    ("Freq", [ 5.0, "RF frequency, GHz"]),
    ("xmi1", [2.0, "Mi1/Mp,  relative mass of ions 1"]),
    ("zi1", [1.0, "charge of ions 1"]),
    ("xmi2", [16.0, " Mi2/Mp,  relative mass of ions 2"]),
    ("zi2", [8.0, "charge of ions 2"]),
    ("dni2", [0.03, "Ni2/Ni1, relative density of ions 2"]),
    ("xmi3", [1.0, "Mi3/Mp,  relative mass of ions 3"]),
    ("zi3", [1.0, "charge of ions 3"]),
    ("dni3", [0.0, "Ni3/Ni1, relative density of ions 3"])
    ])
    return ('Physical parameters', p)

def default_alphas():
    p = dict([
        ("itend0", [0, "if = 0, no alphas"]),
        ("energy", [30.0, "max. perp. energy of alphas (MeV)"]),
        ("factor", [1.0, "factor in alpha source"]),
        ("dra", [0.3, "relative alpha source broadening (dr/a)"]),
        ("kv", [30.0, "V_perp  greed number"])
    ])
    return ('Parameters for alphas calculations', p)

def default_numerical():
    p = dict([
        ("nr",[ 30, "radial grid number  <= 505"]),
        ("hmin1",[ 1.e-6, "rel.(hr) min. step in the Fast comp. mode, <1.d0"]),
        ("rrange", [ 1.e-4, "rel.(hr) size of a 'turning' point region, <1.d0"]),
        ("eps", [1.e-6, "accuracy"]),
        ("hdrob", [1.5, "h4 correction"]),
        ("cleft", [0.7 , "left Vz plato border shift (<1)"]),
        ("cright", [ 1.5, "right Vz plato border shift (>1)"]),
        ("cdel",[0.25 , "(left part)/(Vz plato size)"]),
        ("rbord", [ 0.999, "relative radius of reflection, <1."]),
        ("pchm", [0.2, "threshold between 'strong' and weak' absorption, <1."]),
        ("pabs",[ 1.e-2 , "part of remaining power interp. as absorption"]),
        ("pgiter", [1.e-4 , "relative accuracy to stop iterations"]),
        ("ni1", [20 , "grid number in the left part of Vz plato"]),
        ("ni2", [20, "grid number in the right part of Vz plato"]),
        ("niterat", [99, "maximal number of iterations"]),
        ("nmaxm(1)", [20, "permitted reflections at 0 iteration"]),
        ("nmaxm(2)", [20, "permitted reflections at 1 iteration"]),
        ("nmaxm(3)", [20, "permitted reflections at 2 iteration"]),
        ("nmaxm(4)", [20, "permitted reflections at 3 iteration"]),
        ("maxstep2", [1000, "maximal steps' number in Fast comp. mode"]),
        ("maxstep4", [1000, "maximal steps' number in Slow comp. mode"])
    ])
    return ('Numerical parameters', p)

def default_option():
    p =  dict([
        ('ipri', [2, 'printing output monitoring: 0,1,2,3,4']),
        ('iw', [1, 'initial mode (slow=1, fast=-1)']),
        ('ismth', [0, 'if=0, no smoothing in Ne(rho),Te(rho),Ti(rho)']),
        ('ismthalf', [0, 'if=0, no smoothing in D_alpha(vperp)']),
        ('ismthout', [1, 'if=0, no smoothing in output profiles']),
        ('inew', [-1, "inew=0 for usual tokamak&Ntor_grill; 1 or 2 for g' in ST&Npol_grill"]),
        ('itor', [1, '+-1, Btor direction in right coord{drho,dteta,dfi}']),
        ('ipol', [1, '+-1, Bpol direction in right coord{drho,dteta,dfi}'])
        ])
    return ('Options', p)


def default_grill_parameters():
    p = dict([
        ('Zplus', [11,'upper grill corner in centimeters']),
        ('Zminus', [-11,'lower grill corner in centimeters']),
        ('ntet',[21, 'theta grid number']),
        ('nnz',[51 ,'iN_phi grid number'])
        ])
    return ('grill parameters and input LH spectrum', p)      

def default_parameters():
    pp = default_pp()
    ap = default_alphas()
    nm = default_numerical()
    op = default_option()
    gl = default_grill_parameters()
    return dict([pp, ap, nm, op, gl])

import os
from IPython.core.display import JSON
import ipywidgets as widgets
from IPython.display import display
import json

all_items = []
parameters = []
output = []
parameters_file = "ray_tracing_cfg.json"



def init_parameters():
    global parameters
    parameters = default_parameters()

def save_parameters():
    fp = os.path.abspath(parameters_file)
    with open( fp , "w" ) as write:
        json.dump( parameters , write, indent = 2 )

def update_widget_items():
    no_changes = True    
    for items, (_, par) in zip(all_items, parameters.items()):
        for w, (p, v) in zip(items, par.items()):
            if (w.value != v[0]):
                no_changes = False
                v[0] = w.value
                with output:
                    print(p, w.value)
    return no_changes

def widget():    
    global parameters
    global all_items
    global output
    tab_children = []
    all_items = []
    output = widgets.Output()
    for _, par in parameters.items():
        items = [widgets.FloatText(value=v[0], sync=True, description=p, disabled=False) for p, v in par.items() ]
        all_items.append(items)
        tab_children.append(widgets.GridBox(items, layout=widgets.Layout(grid_template_columns="repeat(3, 300px)")))    

    def prepare_click(b):
        with output:
                print("prepare ")

    def reset_click(b):
        with output:
                print("reset ")

    def load_click(b):
        with output:
                print("load ")

    def save_click(b):
        no_changes = update_widget_items()
        if no_changes:
            with output:
                print("no changes")
        else:
            save_parameters()
            with output:
                print("save parameters")

    tab = widgets.Tab()
    tab.children = tab_children
    for id, p in enumerate(parameters.items()):
        tab.set_title(id, p[0])

    reset_btn = widgets.Button(
        description='Reset parameters',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Reset parameters',
        icon='check' # (FontAwesome names without the `fa-` prefix)
    )

    load_btn = widgets.Button(
        description='Load parameters',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Load parameters',
        icon='check' # (FontAwesome names without the `fa-` prefix)
    )

    save_btn = widgets.Button(
        description='Save parameters',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Save parameters',
        icon='check' # (FontAwesome names without the `fa-` prefix)
    )

    prepare_btn = widgets.Button(
        description='Prepare to run',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Prepare to run',
        icon='check' # (FontAwesome names without the `fa-` prefix)
    )   

    save_btn.on_click(save_click)
    load_btn.on_click(load_click)
    reset_btn.on_click(reset_click)
    prepare_btn.on_click(prepare_click)
    
    btn_box = widgets.HBox([load_btn, save_btn, reset_btn, prepare_btn])

    return widgets.VBox([widgets.Label('Ray-tracing configuration'), tab, btn_box, output])         