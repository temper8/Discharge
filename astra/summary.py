import os
import ipywidgets as widgets
from IPython.display import display
from ipywidgets.widgets.widget_button import ButtonStyle
from ipywidgets.widgets.widget_layout import Layout
from ipywidgets.widgets.widget_output import Output
from race import Race

output = []

race_file = ''

R1 = []

def info():
    print(race_file)
    R1.print_summary()

def widget():
    global output
    global R1
    output = widgets.Output()
    filenames = next(os.walk(os.path.abspath('races/')), (None, None, []))[2]

    def on_value_change(change):
        global race_file
        global R1
        race_file = change['new']
        R1 = Race(race_file)
        output.clear_output()
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