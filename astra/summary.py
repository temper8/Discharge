import os
import ipywidgets as widgets
from IPython.display import display
from ipywidgets.widgets.widget_button import ButtonStyle
from ipywidgets.widgets.widget_layout import Layout
from ipywidgets.widgets.widget_output import Output

output = []

race_file = ''

def info():
    print(race_file)

def widget():
    global output
    output = widgets.Output()
    filenames = next(os.walk(os.path.abspath('races/')), (None, None, []))[2]

    def on_value_change(change):
        global race_file
        race_file = change['new']
        with output:
            print(race_file)


    w_sbr = widgets.Select(
        options=filenames,
        #value='',
        description='Races:',
        disabled=False
    )

    w_sbr.observe(on_value_change, names='value')

    #hb1 = widgets.HBox(widget_list[1:4])
    hb2 = widgets.HBox([ w_sbr])
    header = widgets.Label('Select race', layout = {'width': '100%'} )
    return widgets.VBox([header, hb2, output])