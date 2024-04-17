
#?----------------------------------------------------------------------------------------------------------------------------------------
import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots
import webbrowser
#?----------------------------------------------------------------------------------------------------------------------------------------
def gen_plots(resFile,html_file,open=False):
    """_summary_

    Args:
        resFile (_type_)        : _description_
        html_file (_type_)      : _description_
        open (bool, optional)   : _description_. Defaults to False.
    """
    data                            = pd.read_csv(resFile)      
    column_names                    = data.iloc[0] 
    voltage_data ,current_data      = [],[] 
    for i, column in enumerate(data.columns[1:], start=1): 
        if i % 2 == 1:
            voltage_data.append(go.Scatter(x=data["Time"], y=data[column], mode='lines', name=column_names[column]))
        else:
            current_data.append(go.Scatter(x=data["Time"], y=data[column], mode='lines', name=column_names[column]))
    fig = make_subplots(rows=2, cols=1, subplot_titles=("Voltage", "Current"))
    for trace in voltage_data: 
        fig.add_trace(trace, row=1, col=1)
    for trace in current_data: 
        fig.add_trace(trace, row=2, col=1)
    fig.update_layout(height=600, width=800, title_text="Voltage and Current Data", showlegend=True)
    fig.write_html(html_file) 
    if open: 
        webbrowser.open(html_file)
#?----------------------------------------------------------------------------------------------------------------------------------------