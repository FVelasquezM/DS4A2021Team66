import os
import numpy as np
import pandas as pd
import shapely.wkt
import tifffile as tiff
from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
from app_functions import api_request

# corine landcover colors for each class
a = '0.7'
c = [f'rgba(204, 0, 77,{a})', f'rgba(255, 0, 0,{a})', f'rgba(217,101,69 ,{a})', f'rgb(194, 194, 194 )', f'rgba(0,166,0,{a})', f'rgba(255,255,0,{a})', f'rgba(0,204,242,{a})',
     f'rgba(166,166,255,{a})', f'rgba(0,0,0,{a})', f'rgba(69, 63, 63,{a})']


def preproces_img():
    """
    Read tiff image and preprocess to keep only 3 channels (RGB)

    """

    img_file = tiff.imread('src/data/img.tiff')
    img_file = np.rollaxis(img_file, 0, 3)
    img = np.zeros((img_file.shape[0], img_file.shape[1], 3))
    img[:, :, 0] = img_file[:, :, 4]  # red
    img[:, :, 1] = img_file[:, :, 2]  # green
    img[:, :, 2] = img_file[:, :, 1]  # blue

    return img


def create_figure(class_):
    """
    Reads polygons dataframe and selects the polygons per selected class
    Creates a figure with selected classes colored by its corresponding color

    Parameters
    ----------
    class_: list
        List of selected clases
    """

    polygons = pd.read_csv('src/data/polygons.csv')
    p = polygons['Multi'].apply(lambda x: shapely.wkt.loads(x))
    img = preproces_img()

    fig = px.imshow(img)

    for i in class_:
        for geom in p[i].geoms:
            xs, ys = geom.exterior.xy
            fig.add_trace(go.Scatter(x=list(xs), y=list(ys), fill='tozeroy',
                                     fillcolor=c[i], mode='lines', line=dict(color=c[i])))  # fill down to xaxis

    # style of figure
    fig.layout.margin.t, fig.layout.margin.r, fig.layout.margin.l, fig.layout.margin.b = 30, 0, 0, 0

    fig.update_layout(showlegend=False, width=500, height=450)
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                       'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig


def create_bar_chart(class_):
    """
    Reads polygons dataframe and selects the class and number of objects per selected class
    Creates a bar chart of selected classes and the number of objects with its corresponding colors

    Parameters
    ----------
    class_: list
        List of selected clases
    """

    polygons = pd.read_csv('src/data/polygons.csv')
    df = polygons.iloc[class_]
    cc = [c[i] for i in class_]
    fig = go.Figure(data=[go.Bar(x=df['class'], y=df['poly'], marker_color=cc, textposition="auto", text=df['poly'], textfont=dict(
        size=18,
        color="white",
    ))])

    # style of figure
    fig.update_layout(showlegend=False, width=500, height=300)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                       'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    return fig


prev = [0.5]


def apply_thresh_predict(class_, thresh):
    """
    If threshold different than 0.5 and different than previous selected threshold (only make request
    if threshold has changed) make request to backed api model
    Creates image and bar chart figures with corresponding filters

    Parameters
    ----------
    class_: list
        List of selected clases
    thresh: float 
        Threshold applied. To be classified a prediction values has to be equal or greater than threshold 
    """

    prev.append(thresh)
    if thresh and (prev[-2] != thresh):
        file_img = open(Path('src/data/img.tiff'), 'rb').read()
        api_request(file_img, thresh)

    img = create_figure(class_)
    bars = create_bar_chart(class_)
    del prev[0]

    return img, bars
