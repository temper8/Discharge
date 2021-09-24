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
        ("kv", [30, "V_perp  greed number"])
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
from typing import DefaultDict
from IPython.core.display import JSON
import ipywidgets as widgets
from IPython.display import display
import json
import matplotlib.pyplot as plt

all_items = []
parameters = []
output = []
parameters_file = "ray_tracing_cfg.json"

def divide_spectrum():
    sp = [x for x in zip(parameters['Spectrum']['Ntor'], parameters['Spectrum']['Amp'])]
    sp_pos = [ (s[0], s[1]) for s in sp if s[0]>0]
    sp_neg = [ (-s[0], s[1]) for s in sp if s[0]<0]
    sp_neg = list(reversed(sp_neg))
    return sp_pos, sp_neg

def prepare_spectrum():
    out_lines = []
    sp_pos, sp_neg = divide_spectrum()
    out_lines.append("!!positive Nfi; P_LH(a.units); points<1001\n")
    for s in sp_pos:
        out_lines.append(str(s[0]) + "   " + str(s[1])+"\n")
    with output:    
        print(len(out_lines))

    power = 1.0
    out_lines.append(str(power) + '	-88888. !0.57 first value=part(%) of total power in positive spectrum.\n')
    out_lines.append('!!negative Nfi; P_LH(a.units); points number<1001, arbitrary spacing.\n')

    for s in sp_neg:
        out_lines.append(str(s[0]) + "   " + str(s[1])+"\n")
    with output:
        print(len(out_lines))
    return out_lines


def prepare_dat_file():
    lines = []
    def item_to_line(name, v):
        vs = str(v[0])
        return '  ' + vs + ' '*(9-len(vs)) + "  ! " + name + ' '*(15-len(name)) + v[1] + '\n'

    for section_name, items in parameters.items():
        if section_name == "Spectrum":
            with output:
                print(section_name)      
            lines += prepare_spectrum()
        else:
            lines.append("!"*15 + " "+ section_name + " "+ "!"*(60-len(section_name)) + "\n")
            lines += [ item_to_line(name, v) for name, v in items.items()]
    return lines

def prepare_rt_dat():
    lines = prepare_dat_file()
    file_path = os.path.abspath("rt_cfg.dat")
    with open(file_path, 'w') as f:
        for line in lines:
            f.write(line)

def init_parameters():
    global parameters
    parameters = default_parameters()
    load_parameters()

def load_parameters():
    global parameters
    fp = os.path.abspath(parameters_file)
    if os.path.exists(fp):
        with open(fp) as json_file:
            parameters = json.load(json_file)   

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

import os
import shutil
import astra

def remove_folder_contents(path):
    shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path)

def pick_up_results(b):
    astra_home = astra.config['Astra config']['astra_path'][0]
    src = astra_home + '/lhcd/out' 
    dst = 'out/'
    filenames = next(os.walk(src), (None, None, []))[2]
    remove_folder_contents(dst)
    for f in filenames:
        shutil.copyfile(src + "/"+ f, dst + f)
    with output:
            print( ' src folder:')
            print( ' '+ src)
            print(' Files:' + str(len(filenames)))    
            print(" dest " + dst) 

def prepare_astra():
    astra_home = astra.config['Astra config']['astra_path'][0]
    exp_file = astra.config['Astra config']['exp_file'][0]
    equ_file = astra.config['Astra config']['equ_file'][0]
    dat_file = 'rt_cfg.dat'
    dat_path = astra_home + '/lhcd/' + dat_file
    out_folder = astra_home + '/lhcd/out' 
    with output:
            print(" Astra home " + astra_home)    
            shutil.copyfile(dat_file, dat_path)
            print(" Copy " + dat_file + ' to ' + dat_path)
            remove_folder_contents(out_folder)
            print(' Clear folder: ' + out_folder)
            print(" Please run astra by command: ./a4/.exe/astra " + exp_file + ' ' + equ_file)

def widget():    
    global parameters
    global all_items
    global output
    tab_children = []
    all_items = []
    output = widgets.Output()
    for name, par in parameters.items():
        if name == 'Spectrum':
            out = widgets.Output(layout= {'border': '1px solid blue', 'height': '300px', 'width': '100%'})
            with out:
                fig, ax = plt.subplots(constrained_layout=True, figsize=(5, 2.5))
                ax.plot(par['Ntor'], par['Amp'])                
            tab_children.append(widgets.Box([out]))    
        else:
            items = [widgets.FloatText(value=v[0], sync=True, description=p, disabled=False) for p, v in par.items() ]
            all_items.append(items)
            tab_children.append(widgets.GridBox(items, layout=widgets.Layout(grid_template_columns="repeat(3, 300px)")))    

    def prepare_click(b):
        prepare_rt_dat()
        prepare_astra()
        with output:
                print("prepare config for run rt")

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
    pick_up_btn = widgets.Button(
        description='Pick up results',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Pick up results',
        icon='check' # (FontAwesome names without the `fa-` prefix)
    )   

    save_btn.on_click(save_click)
    load_btn.on_click(load_click)
    reset_btn.on_click(reset_click)
    prepare_btn.on_click(prepare_click)
    pick_up_btn.on_click(pick_up_results)
    
    btn_box = widgets.HBox([load_btn, save_btn, reset_btn, prepare_btn, pick_up_btn])
    title = widgets.Label('Ray-tracing configuration')
    return widgets.VBox([title, tab, btn_box, output])         
    #return widgets.VBox([title, tab, btn_box, output], layout= { 'height': '400px'})

from collections import namedtuple

def read_bounds(f):
    Icms_path = os.path.abspath(f)
    file = open(Icms_path)

    header = file.readline().split()
    #print(header)
    lines = file.readlines()

    table = [line.split() for line in lines]
    table = list(filter(None, table))

    R = [float(row[0]) for row in table]
    Z = [float(row[1]) for row in table]
    return R, Z


def float_try(str):
    try:
        return float(str)
    except ValueError:
        return 0.0

def read_trajectories(f):
    Icms_path = os.path.abspath(f)
    file = open(Icms_path)

    header = file.readline().replace('=', '_').split()

    empty_ray = dict([ (h, []) for h in header ])

    lines = file.readlines()
    table = [line.split() for line in lines]
    table = list(filter(None, table))

    rays = []
    N_traj = 0
    #header.append('N_traj')
    TRay = namedtuple('Ray' , header)

    for row in table:
        if N_traj != int(row[12]):
            N_traj = int(row[12])
            ray = dict([ (h, []) for h in header ])
            rays.append(ray)
        for index, (p, item) in enumerate(ray.items()):
            item.append(float_try(row[index]))
    return rays, N_traj

def plot(f):
    rays, max_N_traj = read_trajectories(f)
    print("Number of traj "+ str(len(rays)) + "   Max N_traj "+ str(max_N_traj))
    plt.figure(figsize=(6,6))

    R, Z = read_bounds("out/lcms.dat")
    plt.plot(R, Z)

    for ray in rays:
        plt.plot(ray['R'], ray['Z'], alpha=0.5, linewidth=1)
 
    plt.show()

def summary4():
    print(" ====================  Ray tracing summary ====================")
    init_parameters()
    
    for name, par in parameters.items():
        if name != 'Spectrum':
            print(' ====== {0} ======'.format(name))
            lines = []
            for p, v in par.items():
                lines.append('{0:8}  {1}'.format(p, v[0]))
            max = len(lines)
            n = int(max/3) + 1
            #print(max, n)
            lines.append('')
            lines.append('')
            lines.append('')
            for i in range(n):
                print('{0:35}  {1:35} {2:35}'.format(lines[i], lines[i+n], lines[i+2* n]))


def summary():
    print(" ====================  Ray tracing summary ====================")
    init_parameters()
    lines = []
    for name, par in parameters.items():
        if name != 'Spectrum':
            lines.append('{0}'.format(name))
            for p, v in par.items():
                lines.append('{0:8}  {1}'.format(p, v[0]))
            #lines.append('')
    #print(lines)
    max = len(lines)
    n = int(max/3) + 1
    #print(max, n)
    lines.append('')
    lines.append('')
    for i in range(n):
        print('{0:35}  {1:35} {2:35}'.format(lines[i], lines[i+n], lines[i+2* n]))

def plot_spectrum():
    sp = parameters['Spectrum']
    fig, ax = plt.subplots(constrained_layout=True, figsize=(5, 2.5))
    ax.plot(sp['Ntor'], sp['Amp'])  