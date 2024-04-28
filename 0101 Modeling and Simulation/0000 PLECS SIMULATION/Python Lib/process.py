import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import webbrowser

def gen_plots(resFile, html_file, open=False):
    data = pd.read_csv(resFile)
    column_names = data.iloc[0]
    num_plots = len(data.columns) - 1
    
    fig = make_subplots(rows=num_plots, cols=1, subplot_titles=tuple(column_names[1:]))
    
    for i, column in enumerate(data.columns[1:], start=1):
        fig.add_trace(go.Scatter(x=data["Time"], y=data[column], mode='lines', name=column_names[column]), row=i, col=1)
    
    fig.update_layout(title_text="Voltage and Current Data", showlegend=False)
    fig.update_layout(height=300*num_plots)  # Dynamic height
    
    fig.write_html(html_file)
    
    if open:
        webbrowser.open(html_file)



#?----------------------------------------------------------------------------------------------------------------------------------------