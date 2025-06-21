
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
import plotly.graph_objs as go
import plotly.subplots as sp
#?----------------------------------------------------------------------------------------------------------------------------------------

def png_to_hex_base64():
    imghexdata                  = ''
    img_path                    = (os.path.join(os.getcwd(), "Modeling and Simulation/PLECS SIMULATION/Model/png/OBC.png")).replace("\\", "/") 
    screen                      = screeninfo.get_monitors()[0]
    screen_width, screen_height = screen.width, screen.height
    target_width                = int(screen_width * 0.5)  
    target_height               = int(screen_height * 0.4)  
    try:
        with Image.open(img_path) as img:
            resized_img         = img.resize((target_width, target_height), resample=Image.LANCZOS)
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
    items                   = {}
    for k, v in d.items():
        new_key             = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key]  = v
    return items

def extract_comments(filename):
    prefix_list                     = []
    comment_list                    = []

    with open(filename, 'r') as file:
        for line in file:
            if '#?' in line:
                start_index         = line.index('#?')
                prefix              = line[start_index+2:start_index+2+8]
                rest_of_comment     = line[start_index+2+8:].strip()

                prefix_list.append(prefix)
                comment_list.append(rest_of_comment)
    
    return prefix_list, comment_list

def convert_to_ordereddict(d):
    if not isinstance(d, dict):
        return d
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
    ToFile              = ['sim_idx','utc_numeric','ToFile_path','logfile','output_html','Traces']
    mdlvar_flat         = delete_keys_from_dict(ToFile, copy.deepcopy(mdl.ModelVars),'ToFile')
    mdlvar_flat         = flatten_dict(convert_to_ordereddict(mdlvar_flat))
    file_path           = "Modeling and Simulation/PLECS SIMULATION/Python Lib/Model_Parameters.py"  
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
        fig.update_yaxes(title_text=mdl.Units[i], row=i+1, col=1)
    fig.update_layout(height=300*len(mdl.Waveforms))  
    title        = f"OBC_{mdl.ModelVars['ToFile']['utc_numeric']}_{mdl.ModelVars['ToFile']['sim_idx']}_MOHAMED_GUENI"
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
                                <img src="data:image/png;base64,{png_to_hex_base64()}" alt="flyback.png">
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

import plotly.graph_objects as go
import plotly.subplots as sp
import webbrowser

def plot_ac_analysis_sweep(results_list, html_file, OPEN=False):
    """
    Plots the magnitude (Gr) and phase (Gi) for multiple iterations with a logarithmic frequency axis.

    Parameters:
    - results_list: A list of dictionaries, each containing 'F', 'Gr', and 'Gi' values.
    - html_file: The file path to save the HTML output.
    - mdl: The model object containing AnalysisOpts and other metadata.
    - OPEN: If True, the HTML file will be opened in the default web browser.
    """

    # Create a subplot with 2 rows: one for Gr and one for Gi
    fig = sp.make_subplots(rows=2, cols=1, shared_xaxes=True,
                           subplot_titles=('Magnitude (Gr)', 'Phase (Gi)'),
                           vertical_spacing=0.20)

    # Loop through each result and add traces for Gr and Gi
    for idx, data in enumerate(results_list):
        frequencies = data['F']
        Gr_values = data['Gr'][0]
        Gi_values = data['Gi'][0]

        # Add Magnitude (Gr) plot
        fig.add_trace(
            go.Scatter(x=frequencies, y=Gr_values, mode='lines',
                       name=f'Magnitude (Gr) Iteration {idx+1}',
                       showlegend=True),
            row=1, col=1
        )

        # Add Phase (Gi) plot
        fig.add_trace(
            go.Scatter(x=frequencies, y=Gi_values, mode='lines',
                       name=f'Phase (Gi) Iteration {idx+1}',
                       showlegend=True),
            row=2, col=1
        )
    
    # Update layout
    fig.update_layout(
        autosize=True,
        title_text='AC Sweep Analysis',
        xaxis_title='Frequency (Hz)',
        yaxis_title='Magnitude (dB)',
        yaxis2_title='Phase (deg)',
        margin=dict(l=50, r=50, t=100, b=50),
        height=600
    )

    # Ensure logarithmic x-axis
    fig.update_xaxes(type='log', title_text='Frequency (Hz)', row=1, col=1)
    fig.update_xaxes(type='log', title_text='Frequency (Hz)', row=2, col=1)
    
    # Extracting and flattening model variables for the table
    mdlvar_flat = flatten_dict(convert_to_ordereddict(mdl.AnalysisOpts))
    
    # Create a table with model variables
    table_fig = go.Figure(data=[go.Table(
        header=dict(values=["PARAMETERS", "VALUES"],
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[list(mdlvar_flat.keys()), list(mdlvar_flat.values())],
                   fill_color='lavender',
                   align='left')
    )])

    # HTML title
    title = f"AC Sweep Analysis_{mdl.ModelVars['ToFile']['utc_numeric']}_{mdl.ModelVars['ToFile']['sim_idx']}_MOHAMED_GUENI"
    
    # Create the HTML structure
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
    """
    
    # Write the HTML file with the embedded Plotly figure
    with open(html_file, "w") as f:
        f.write(html_content)
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(table_fig.to_html(full_html=False, include_plotlyjs=False))

    # Optionally open the HTML file
    if OPEN:
        webbrowser.open(html_file)



#?----------------------------------------------------------------------------------------------------------------------------------------