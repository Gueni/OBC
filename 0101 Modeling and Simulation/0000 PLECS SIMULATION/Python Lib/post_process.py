
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
from collections import OrderedDict
import re
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

def extract_comments(filename):
    prefix_list = []
    comment_list = []

    with open(filename, 'r') as file:
        for line in file:
            # Look for '#?' anywhere in the line
            if '#?' in line:
                start_index = line.index('#?')
                prefix = line[start_index+2:start_index+2+8]
                rest_of_comment = line[start_index+2+8:].strip()

                prefix_list.append(prefix)
                comment_list.append(rest_of_comment)
    
    return prefix_list, comment_list

def convert_to_ordereddict(d):
    # Base case: if d is not a dictionary, return it as is
    if not isinstance(d, dict):
        return d
    # Recursively convert each nested dictionary to OrderedDict
    return OrderedDict((key, convert_to_ordereddict(value)) for key, value in d.items())

def delete_keys_from_dict(keys_to_delete, input_dict,key2):
    for key in keys_to_delete:
            del input_dict[key2][key]
    return input_dict

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
    LLC                 = ['HS1','HS2','LS1','LS2','SRHS1','SRHS2','SRLS1','SRLS2','RC1','RC2','RC3','RC4','HS3','LS3']             
    PFC                 = ['HS1','HS2','LS1','LS2']
    mdlvar_flat         = delete_keys_from_dict(LLC, mdl.ModelVars,'LLC')
    mdlvar_flat         = delete_keys_from_dict(PFC, mdlvar_flat,'PFC')
    mdlvar_flat         = flatten_dict(convert_to_ordereddict(copy.deepcopy(mdl.ModelVars)))
    file_path           = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/Model_Parameters.py"  # Replace with your Python file path
    unit ,comments      = extract_comments(file_path)
    table_fig           = go.Figure(data=[go.Table(
        header=dict(values=["PARAMETERS", "VALUES" , "UNITS","COMMENTS"],
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[list(mdlvar_flat.keys()), list(mdlvar_flat.values()) ,unit ,comments  ],
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
