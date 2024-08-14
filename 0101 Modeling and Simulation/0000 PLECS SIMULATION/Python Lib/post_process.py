
#?----------------------------------------------------------------------------------------------------------------------------------------
#?                                  ____             __     ____
#?                                 / __ \____  _____/ /_   / __ \_________  ________  __________
#?                                / /_/ / __ \/ ___/ __/  / /_/ / ___/ __ \/ ___/ _ \/ ___/ ___/
#?                               / ____/ /_/ (__  ) /_   / ____/ /  / /_/ / /__/  __(__  |__  ) 
#?                              /_/    \____/____/\__/  /_/   /_/   \____/\___/\___/____/____/  
#?     
#?----------------------------------------------------------------------------------------------------------------------------------------                         
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import webbrowser
import Model_Parameters as mdl
import os
import base64
from PIL import Image
import screeninfo
import copy
#?----------------------------------------------------------------------------------------------------------------------------------------

def png_to_hex_base64():
    imghexdata      = ''
    img_path        = (os.path.join(os.getcwd(), "0101 Modeling and Simulation/0000 PLECS SIMULATION/Model/png/OBC.png")).replace("\\", "/") 
    screen = screeninfo.get_monitors()[0]
    screen_width, screen_height = screen.width, screen.height
    target_width    = int(screen_width * 0.5)  
    target_height   = int(screen_height * 0.4)  
    try:
        with Image.open(img_path) as img:
            resized_img = img.resize((target_width, target_height), resample=Image.LANCZOS) #todo : get the size of screen and make a ratio 
            resized_img.save("img.png")
        img.close()
    except IOError:
        print("Unable to resize image")
    with open("img.png", "rb") as f:
        encoded_image = base64.b64encode(f.read())
    f.close()
    with open("image.txt", "w") as f:
        f.write(encoded_image.decode("utf-8"))
    f.close()
    with open("image.txt","r") as tempF:
        newlines = tempF.readlines()
        for singleline in newlines:
            imghexdata +=singleline
    tempF.close()  
    if os.path.isfile("image.txt") and os.path.exists("image.txt"):
        os.remove("image.txt")
    if os.path.isfile("img.png") and os.path.exists("img.png"):
        os.remove("img.png")
    return imghexdata

def flatten_dict(d, parent_key='', sep='.'):
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items

def gen_plots(resFile, html_file, OPEN=False):
    df                  = pd.read_csv(resFile)
    fig                 = make_subplots(rows=len(mdl.Waveforms), cols=1, subplot_titles=tuple(mdl.Waveforms))
    for i, _ in enumerate(df.columns[1:], start=1):
        fig.add_trace(go.Scatter(x=df.iloc[:,0], y=df.iloc[:,i], mode='lines', name=mdl.Waveforms[i-1]), row=i, col=1)
    fig.update_layout   (
        plot_bgcolor='#e9f5f9',
        title_text      =   "OBC WAVEFORMES",
        showlegend      =   False,
        title           =   dict(font    =  dict(family  ="Arial", size=30 ))
                        )
    mdlvar_flat         = flatten_dict(copy.deepcopy(mdl.ModelVars))
    del mdlvar_flat['scopes']
    del mdlvar_flat['ToFile']
    table_fig           = go.Figure(data=[go.Table(
        header=dict(values=["Parameter", "Value"],
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[list(mdlvar_flat.keys()), list(mdlvar_flat.values())],
                   fill_color='lavender',
                   align='left')
    )])

    for i in range(len(mdl.Waveforms)):
        fig.update_xaxes(title_text="Time [s]", row=i+1, col=1)
    fig.update_layout(height=300*len(mdl.Waveforms))  
    title        = f"Single Phase EV OBC_{mdl.utc_numeric}_{mdl.sim_idx}"
    html_content = f"""
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>{title}</title>
                        </head>
                        <body>
                            <div class="center">
                                <img src="data:image/png;base64,{png_to_hex_base64()}" alt="OBC.png">
                            </div>
                        </body>
                        </html>
                    """
    with open(html_file, "w") as f:
        f.write('<style>.center {display: flex;justify-content: center;}</style>')
        f.write(html_content)
        f.write(fig.to_html(full_html = False,include_plotlyjs='cdn'))
        f.write(table_fig.to_html(full_html=False, include_plotlyjs=False))
    f.close()
    if OPEN:
        webbrowser.open(html_file)
#?----------------------------------------------------------------------------------------------------------------------------------------
