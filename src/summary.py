import os
from ipython_genutils.py3compat import with_metaclass
import ipywidgets as widgets
from IPython.display import display
from ipywidgets.widgets.widget_button import ButtonStyle
from ipywidgets.widgets.widget_layout import Layout
from ipywidgets.widgets.widget_output import Output
from race import Race

output = []

race_file = ''
selected_races = []
widget_races = []
header = []

def print_columns(cols):
    w = 50
    for k,_ in enumerate(cols[0]):
        s = ''
        for j,_ in enumerate(cols):
            s = s + cols[j][k] + ' '*(w-len(cols[j][k]))
        print(s)    


def print_info(options):
    #print(selected_races)
    w = 50 
    races = [Race(r) for r in selected_races]
    summary = [ r.summary() for r in races]
    rt_summary = [ r.rt_summary(options) for r in races]
    
    for s, rt in zip(summary, rt_summary):
        s.extend(rt)
    
    for s, f in zip(summary, selected_races):
        x = (w-len(f))//2
        s.insert(0, ' '*x + f + ' '*x)
    #print(s)
    print_columns(summary)


def widget():
    global selected_races
    global widget_races
    global header
    global output
    output = widgets.Output()
    filenames = next(os.walk(os.path.abspath('races/')), (None, None, []))[2]
    filenames = [f for f in filenames if f.endswith('zip') ]

    def on_value_change(change):
        global header
        global selected_races
        selected_races = widget_races.value
        header.value = 'Select race : '  + str(widget_races.value)

    widget_races = widgets.SelectMultiple(
        options=filenames,
        #value='',
        description='Races:',
        disabled=False,
        layout=widgets.Layout(width='500px', height = '160px')
    )
    widget_races.observe(on_value_change, names='value')

    #hb1 = widgets.HBox(widget_list[1:4])
    hb2 = widgets.HBox([widget_races])
    header = widgets.Label('Select race :', layout = {'width': '100%'} )
    
    return widgets.VBox([header, hb2, output])