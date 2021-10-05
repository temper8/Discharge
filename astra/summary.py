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

def info():
    print(selected_races)

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
        disabled=False
    )
    widget_races.observe(on_value_change, names='value')

    #hb1 = widgets.HBox(widget_list[1:4])
    hb2 = widgets.HBox([widget_races])
    header = widgets.Label('Select race :', layout = {'width': '100%'} )
    
    return widgets.VBox([header, hb2, output])