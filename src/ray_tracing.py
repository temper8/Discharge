def default_pp():
    p = {
    "Freq": [ 5.0, 'GHz', "RF frequency, GHz"],
    "xmi1": [2.0, 'Mi1/Mp', "Mi1/Mp,  relative mass of ions 1"],
    "zi1": [1.0, 'float', "charge of ions 1"],
    "xmi2": [16.0, 'Mi2/Mp', " Mi2/Mp,  relative mass of ions 2"],
    "zi2": [8.0, 'float', "charge of ions 2"],
    "dni2": [0.03, 'Ni2/Ni1', "Ni2/Ni1, relative density of ions 2"],
    "xmi3": [1.0, 'Mi3/Mp', "Mi3/Mp,  relative mass of ions 3"],
    "zi3": [1.0, 'float', "charge of ions 3"],
    "dni3": [0.0, 'Ni3/Ni1', "Ni3/Ni1, relative density of ions 3"]
    }
    return ('Physical parameters', p)

def default_alphas():
    p = {
        "itend0": [0, 'int', "if = 0, no alphas"],
        "energy": [30.0, 'MeV', "max. perp. energy of alphas (MeV)"],
        "factor": [1.0, 'float', "factor in alpha source"],
        "dra": [0.3, 'dr/a', "relative alpha source broadening (dr/a)"],
        "kv": [30, 'int', "V_perp  greed number"]
    }
    return ('Parameters for alphas calculations', p)

def default_numerical():
    p = {
        "nr":     [30,'int', "radial grid number  <= 505"],
        "hmin1":  [1.e-6, 'float', "rel.(hr) min. step in the Fast comp. mode, <1.d0"],
        "rrange": [ 1.e-4, 'float', "rel.(hr) size of a 'turning' point region, <1.d0"],
        "eps":    [1.e-6, 'float', "accuracy"],
        "hdrob":  [1.5, 'float', "h4 correction"],
        "cleft":  [0.7, 'float', "left Vz plato border shift (<1)"],
        "cright": [1.5, 'float', "right Vz plato border shift (>1)"],
        "cdel":   [0.25, 'float', "(left part)/(Vz plato size)"],
        "rbord":  [0.999, 'float', "relative radius of reflection, <1."],
        "pchm":   [0.2, 'float', "threshold between 'strong' and weak' absorption, <1."],
        "pabs":   [1.e-2, 'float', "part of remaining power interp. as absorption"],
        "pgiter": [1.e-4, 'float', "relative accuracy to stop iterations"],
        "ni1":    [20,'int', "grid number in the left part of Vz plato"],
        "ni2":    [20,'int', "grid number in the right part of Vz plato"],
        "niterat":  [99,'int', "maximal number of iterations"],
        "nmaxm(1)": [20,'int', "permitted reflections at 0 iteration"],
        "nmaxm(2)": [20,'int', "permitted reflections at 1 iteration"],
        "nmaxm(3)": [20,'int', "permitted reflections at 2 iteration"],
        "nmaxm(4)": [20,'int', "permitted reflections at 3 iteration"],
        "maxstep2": [1000,'int', "maximal steps' number in Fast comp. mode"],
        "maxstep4": [1000,'int', "maximal steps' number in Slow comp. mode"]
    }
    return ('Numerical parameters', p)

def default_option():
    p = {
        'ipri': [2,'int', 'printing output monitoring: 0,1,2,3,4'],
        'iw': [1,'int', 'initial mode (slow=1, fast=-1)'],
        'ismth': [0,'int', 'if=0, no smoothing in Ne(rho),Te(rho),Ti(rho)'],
        'ismthalf': [0,'int', 'if=0, no smoothing in D_alpha(vperp)'],
        'ismthout': [1,'int', 'if=0, no smoothing in output profiles'],
        'inew': [-1,'int', "inew=0 for usual tokamak&Ntor_grill; 1 or 2 for g' in ST&Npol_grill"],
        'itor': [1,'int', '+-1, Btor direction in right coord{drho,dteta,dfi}'],
        'ipol': [1,'int', '+-1, Bpol direction in right coord{drho,dteta,dfi}']
    }
    return ('Options', p)


def default_grill_parameters():
    p = {
        'Zplus': [11,'float', 'upper grill corner in centimeters'],
        'Zminus': [-11,'float', 'lower grill corner in centimeters'],
        'ntet': [21,'int', 'theta grid number'],
        'nnz': [51,'int','iN_phi grid number'],
        'total power': [1,'%','total power in positive spectrum']
    }
    return ('grill parameters', p)      

def default_parameters():
    pp = default_pp()
    ap = default_alphas()
    nm = default_numerical()
    op = default_option()
    gl = default_grill_parameters()
    sp = ('LH spectrum', {'Ntor':[], 'Amp':[]}) 
    return dict([pp, ap, nm, op, gl, sp])


import os
import shutil
import ipywidgets as widgets
from IPython.display import display
import json
import matplotlib.pyplot as plt
import astra

all_items = []
parameters = []
output = []
parameters_file = "data/ray_tracing_cfg.json"

def divide_spectrum():
    sp = [x for x in zip(parameters['LH spectrum']['Ntor'], parameters['LH spectrum']['Amp'])]
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
    #print(len(out_lines))

    power = parameters['grill parameters']['total power'][0]
    out_lines.append(str(power) + '	-88888. !0.57 first value=part(%) of total power in positive spectrum.\n')
    out_lines.append('!!negative Nfi; P_LH(a.units); points number<1001, arbitrary spacing.\n')

    for s in sp_neg:
        out_lines.append(str(s[0]) + "   " + str(s[1])+"\n")
    #print(len(out_lines))
    return out_lines


def prepare_dat_file():
    lines = []
    def item_to_line(name, v):
        vs = str(v[0])
        return '  ' + vs + ' '*(9-len(vs)) + "  ! " + name + ' '*(15-len(name)) + v[2] + '\n'

    for section_name, items in parameters.items():
        if section_name == "LH spectrum":
            print('prepare: '+ section_name)      
            lines += prepare_spectrum()
        else:
            lines.append("!"*15 + " "+ section_name + " "+ "!"*(60-len(section_name)) + "\n")
            lines += [ item_to_line(name, v) for name, v in items.items() if name !='total power']
    return lines

def prepare_rt_dat():
    lines = prepare_dat_file()
    file_path = os.path.abspath("data/rt_cfg.dat")
    with open(file_path, 'w') as f:
        for line in lines:
            f.write(line)

def init_parameters():
    global parameters
    parameters = default_parameters()
    load_parameters()

def parse_sepktr(lines):
    positive = True
    pos_spektr = { 'Ntor': [], 'Amp': []  }
    neg_spektr = { 'Ntor': [], 'Amp': []  }
    for l in lines[53:]:
        v = l.split()
        if v[0] == '!!negative':
            positive = False
            continue
        if v[1] == '-88888.':
            power = float(v[0])
            continue
        if positive:
            pos_spektr['Ntor'].append(float(v[0]))
            pos_spektr['Amp'].append(float(v[1]))
        else:
            neg_spektr['Ntor'].append(float(v[0]))
            neg_spektr['Amp'].append(float(v[1]))
    #print(pos_spektr)
    spektr = { 'Ntor': [], 'Amp': []  }
    for (x,y) in zip(reversed(neg_spektr['Ntor']), reversed(neg_spektr['Amp'])):
        spektr['Ntor'].append(-x)
        spektr['Amp'].append(y)
    for (x,y) in zip(pos_spektr['Ntor'], pos_spektr['Amp']):
        spektr['Ntor'].append(x)
        spektr['Amp'].append(y)        
    return (power, spektr)

def parse_parameters(lines):
    param = default_parameters()
    #'Physical parameters'
    
    row = 1
    for key, p in param['Physical parameters'].items():
        v = lines[row].split()
        row = row + 1
        p[0] = float(v[0])

    #'Parameters for alphas calculations'
    #print(lines[10])
    row = 11    
    for key, p in param['Parameters for alphas calculations'].items():
        v = lines[row].split()
        row = row + 1
        #print(v)
        if p[1] == 'int':
            p[0] = int(v[0])    
        else:
            p[0] = float(v[0])
        #print(key, p)
    #'Numerical parameters'
    #print(lines[16])
    row = 17    
    for key, p in param['Numerical parameters'].items():
        v = lines[row].split()
        row = row + 1
        if p[1] == 'int':
            p[0] = int(v[0])    
        else:
            p[0] = float(v[0])
        #print(key, p)

    #'options'
    #print(lines[38])
    row = 39    
    for key, p in param['Options'].items():
        v = lines[row].split()
        row = row + 1
        if p[1] == 'int':
            p[0] = int(v[0])    
        else:
            p[0] = float(v[0])
        #print(key, p)

    #'grill parameters'
    #print(lines[47])
    row = 48    
    for key, p in param['grill parameters'].items():
        if key != 'total power':
            v = lines[row].split()
            row = row + 1
            if p[1] == 'int':
                p[0] = int(v[0])    
            else:
                p[0] = float(v[0])
            #print(key, p)
    (power, param['LH spectrum']) = parse_sepktr(lines)
    param['grill parameters']['total power'][0] = power
    return param

def import_parameters(file_name):
    global parameters
    file_path = os.path.abspath(f"data/{file_name}")
    
    if os.path.exists(file_path):
        print(f"Import parameters from:{file_path}")
        with open(file_path) as f:
            lines = f.readlines()
    parameters = parse_parameters(lines)


def load_parameters():
    global parameters
    fp = os.path.abspath(parameters_file)
    if os.path.exists(fp):
        with open(fp) as json_file:
            parameters = json.load(json_file)   

def save_parameters():
    for items, (name, par) in zip(all_items, parameters.items()):
        if name != 'LH spectrum':
            for w, (p, v) in zip(items, par.items()):
                if (w.value != v[0]):
                    v[0] = w.value
                    with output:
                        print(p, w.value)

    fp = os.path.abspath(parameters_file)
    with open( fp , "w" ) as write:
        json.dump( parameters , write, indent = 2 )

def update_widget_items():
    for items, (name, par) in zip(all_items, parameters.items()):
        if name != 'LH spectrum':
            for w, (p, v) in zip(items, par.items()):
                if (w.value != v[0]):
                    w.value = v[0]
                    with output:
                        print(p, w.value)
        else:
            img = items #layout= {'border': '1px solid blue', 'height': '300px', 'width': '100%'})
            with plt.ioff():
                fig = plt.figure(figsize=(6, 3))
                plt.title(name)
                plt.plot(par['Ntor'], par['Amp'])
                buffer = io.BytesIO()
                fig.savefig(buffer, format="png")
                buffer.seek(0)
                img.value = buffer.read()
                #img = widgets.Image(value=image, format='png')
            #tab_children.append(out)   




style = {'description_width': '100px', "data-toggle": "tooltip"}
layout = {'width': '300px'}

def NumberTextWidget(des, v):
    if v[1] == 'int':
        return widgets.IntText(value=v[0], tooltip=v[1], description=des, disabled=False, style = style, layout= layout)
    else:
        return widgets.FloatText(value=v[0], description='{0} ({1})'.format(des,v[1]), disabled=False,style = style, layout= layout)

import io

def widget():    
    global parameters
    global all_items
    global output
    tab_children = []
    all_items = []
    output = widgets.Output()
    for name, par in parameters.items():
        if name == 'LH spectrum':
            with plt.ioff():
                fig = plt.figure(figsize=(6, 3))
                plt.title(name)
                plt.plot(par['Ntor'], par['Amp'])
                buffer = io.BytesIO()
                fig.savefig(buffer, format="png")
                buffer.seek(0)
                image = buffer.read()
                img = widgets.Image(value=image, format='png')
            all_items.append(img)
            tab_children.append(img)    
        else:
            items = [ NumberTextWidget(key, v) for key, v in par.items() ]
            all_items.append(items)
            tab_children.append(widgets.GridBox(items, layout=widgets.Layout(grid_template_columns="repeat(3, 300px)")))    



    def reset_click(b):
        global parameters
        output.clear_output()
        parameters = default_parameters()        
        update_widget_items()
        with output:
                print("reset ")

    def load_click(b):
        output.clear_output()
        load_parameters()
        update_widget_items()
        with output:
                print("load ")

    def save_click(b):
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
       
    save_btn.on_click(save_click)
    load_btn.on_click(load_click)
    reset_btn.on_click(reset_click)

    btn_box = widgets.HBox([load_btn, save_btn, reset_btn])
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
    fp = os.path.abspath(f)
    if os.path.exists(fp):
        rays, max_N_traj = read_trajectories(f)
        print("Number of traj "+ str(len(rays)) + "   Max N_traj "+ str(max_N_traj))
        plt.figure(figsize=(6,6))
        R, Z = read_bounds("out/lcms.dat")
        plt.plot(R, Z)
        for ray in rays:
            plt.plot(ray['R'], ray['Z'], alpha=0.5, linewidth=1)
        plt.show()
    else:
        print( 'file {0} not exits'.format(f))

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
    sp = parameters['LH spectrum']
    fig, ax = plt.subplots(constrained_layout=True, figsize=(5, 2.5))
    ax.plot(sp['Ntor'], sp['Amp'])  