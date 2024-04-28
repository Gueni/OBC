import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import webbrowser
import Model_Parameters as mdl
#?----------------------------------------------------------------------------------------------------------------------------------------
def gen_plots(resFile, html_file, OPEN=False):
    df         = pd.read_csv(resFile)
    fig        = make_subplots(rows=len(mdl.Waveforms), cols=1, subplot_titles=tuple(mdl.Waveforms))
    for i, _ in enumerate(df.columns[1:], start=1):
        fig.add_trace(go.Scatter(x=df.iloc[:,0], y=df.iloc[:,i], mode='lines', name=mdl.Waveforms[i-1]), row=i, col=1)
    
    fig.update_layout(
        title_text=None,
        showlegend=False,
        title=dict(
            font=dict(
                family="Arial",  
                size=30  
            )
        )
    )
    fig.update_layout(height=300*len(mdl.Waveforms))  
    # Title of your HTML page
    title = "Single Phase EV Onboard Charger with PFC and LLC Resonant Converter"

    # HTML content with the title
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
    </head>
    <body>
        <h1>{title}</h1>
    </body>
    </html>
    """
    with open(html_file, "w") as f:
        f.write(html_content)
        f.write("<hr>")
        f.write(fig.to_html(full_html = False,include_plotlyjs='cdn'))

    f.close()
    # fig.write_html(html_file, include_plotlyjs='cdn')
    
    if OPEN:
        webbrowser.open(html_file)
#?----------------------------------------------------------------------------------------------------------------------------------------
