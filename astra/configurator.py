def default_astra_config():
    cfg = [
        ["astra_path", "\home\Astra", "Path to astra user folder"],
        ["exp", "readme", "exp file name"],
        ["equ", "showdata", "equ file name"],
        ["option1", "op1", "option 1"],
        ["option2", "op2", "option 2"]
    ]
    return ('Astra config', cfg)

def default_sbr_config():
    cfg = [
        ["sbr1", "\home\Astra", "subrutine 1"],
        ["sbr2", "readme", "subrutine 2"],
        ["sbr3", "showdata", "subrutine 3"],
        ["sbr4", "", "subrutine 4"],
        ["sbr5", "", "subrutine 5"]
    ]
    return ('Subrutine config', cfg)

def default_config():
    astra_cfg = default_astra_config()
    sbr_cfg = default_sbr_config()
    return dict([astra_cfg, sbr_cfg])    

import ipywidgets as widgets
from IPython.display import display

def widget_config(cfg):
    tab_children = []
    all_items = []
    for pp in cfg.items():
        items = [widgets.Text(value=p[1], sync=True, description=p[0], disabled=False) for p in pp[1] ]
        all_items.append(items)
        tab_children.append(widgets.GridBox(items, layout=widgets.Layout(grid_template_columns="repeat(3, 300px)")))
    tab = widgets.Tab()
    tab.children = tab_children
    for id, p in enumerate(cfg.items()):
        tab.set_title(id, p[0])

    save_btn = widgets.Button(
        description='Save config',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Save config',
        icon='check' # (FontAwesome names without the `fa-` prefix)
    )
    #save_btn.on_click(save_changes)
    return widgets.VBox([widgets.Label('Astra configuration'), tab, save_btn])
