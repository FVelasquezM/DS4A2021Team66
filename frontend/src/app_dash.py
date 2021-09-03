import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from dash_functions import apply_thresh_predict

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# dash application
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def image_layout():
    classes=['Buildings', 'Manmade structures','Road','Track'
                ,'Trees','Crops','Waterway','Standing water','Large vehicle','Small vehicle']
    
    # 1 inputs - classes that are being check as checkboxes and threshold selected from dropdown
    try:
        ## image figure with polygons colored depending on selected classes
        return html.Div([html.Div([
        dcc.Graph(id='img',
        config={'displayModeBar': True},style={'margin-right':'1rem'})]),
            html.Div([

        # chechboxes of classes
        dcc.Checklist(
                id='class_buttons',
                options=[{'label':i,'value': j} for j,i in enumerate(classes)],
                value=list(range(len(classes))),
            ),
        ## bar plot of number of polygons per selected class
        dcc.Graph(id='bars',
        config={'displayModeBar': False})],id='right-side'),
        
        ## classification threshold for our model
        html.Div([html.P(
            [
                "Classification Threshold",
      ],id='cl'),dcc.Dropdown(id='thresh',
    options=[
       {'label':round(i*0.1,1),'value':round(i*0.1,1)} for i in range(1,10)
    ],
    
   clearable=False,
    value=0.5
)  ],id='menu'),
          
    ],id='container')
    except:
        return html.Div('no image uploaded yet')


app.layout = image_layout

## callback receive outputs, call our function and returns two figures to be display
@app.callback(
    Output('img', 'figure'),
     Output('bars', 'figure'),
    Input('class_buttons', 'value'),
    Input('thresh', 'value'))
def update_figure(class_,thresh):
    img,bars=apply_thresh_predict(class_,thresh)
   
    return img,bars



if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0')




