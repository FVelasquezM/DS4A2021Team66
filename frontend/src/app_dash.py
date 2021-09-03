import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from dash_functions import apply_thresh_predict

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# dash application
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def image_layout():
    """
    Renders the dash app layout based on user callbacks

    classes: 10 classes of classified objects
    Graph(img): Tiff image figure with colored polygons depending on selected classes
    Checklist: Checkboxes of classes  
    Graph(bars): Bar plot of number of objects per selected class
    Dropdown : Select classification threshold for the model

    """
    classes = ['Buildings', 'Manmade structures', 'Road', 'Track', 'Trees',
               'Crops', 'Waterway', 'Standing water', 'Large vehicle', 'Small vehicle']

    try:
        return html.Div([html.Div([
            dcc.Graph(id='img',
                      config={'displayModeBar': True}, style={'margin-right': '1rem'})]),
            html.Div([

                dcc.Checklist(
                    id='class_buttons',
                    options=[{'label': i, 'value': j}
                             for j, i in enumerate(classes)],
                    value=list(range(len(classes))),
                ),
                dcc.Graph(id='bars',
                          config={'displayModeBar': False})], id='right-side'),

            html.Div([html.P(
                [
                    "Classification Threshold",
                ], id='cl'), dcc.Dropdown(id='thresh',
                                          options=[
                                              {'label': round(i*0.1, 1), 'value': round(i*0.1, 1)} for i in range(1, 10)
                                          ],

                                          clearable=False,
                                          value=0.5
                                          )], id='menu'),

        ], id='container')
    except:
        return html.Div('no image uploaded yet')


app.layout = image_layout


@app.callback(
    Output('img', 'figure'),
    Output('bars', 'figure'),
    Input('class_buttons', 'value'),
    Input('thresh', 'value'))
def update_figure(class_, thresh):
    """
    callback: Receives 2 inputs.
         Inputs: classes selected from the checkboxes and classification threshold applied. 
         Outputs: image figure and bars figure
    Re-render graphs based on classes checked and threshold applied 

    Parameters
    ----------
    class_:list
        list of classes checked
    thresh:float 
        Number between 0 and 1
    """
    img, bars = apply_thresh_predict(class_, thresh)

    return img, bars


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0')
