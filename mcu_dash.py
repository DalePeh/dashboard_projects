import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template


#Load Template
load_figure_template("superhero")

#create a dash app
app = dash.Dash(__name__,  external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {'background': 'black'}

# get data
df=pd.read_csv('Data/box_office.csv')

# a group by of yearly earning
yearly_earning= df.groupby(['Year_Release', 'Phase'])['Box office gross Worldwide'].sum()
df_year_earning = pd.DataFrame(yearly_earning)

#rename columns box office gross worldwide to total earning
df_year_earning = df_year_earning.rename(columns={'Box office gross Worldwide': 'Total Earnings'})

# reset_index for df_year_earning
df_year_earning = df_year_earning.reset_index()

# change year as category
df['Year_Release'] = pd.to_datetime(df['Year_Release']).dt.strftime('%Y')

# define color for each mcu movie phase
colors = {
	'Phase One': 'Green',
    'Phase Two': 'Indigo',
    'Phase Three': 'Gold',
    'Phase Four': 'HotPink',
    'Phase Five': 'BurlyWood'
}

# define dropdown options
dropdown_options = [{'label': 'All Phases', 'value': 'All Phases'},
					{'label': 'Phase One', 'value': 'Phase One'},
					{'label': 'Phase Two', 'value': 'Phase Two'},
					{'label': 'Phase Three', 'value': 'Phase Three'},
					{'label': 'Phase Four', 'value': 'Phase Four'},
					{'label': 'Phase Five', 'value': 'Phase Five'},]


# app layout
app.layout = html.Div(style={
    'backgroundColor': '#000000',
    'padding': '10px',
    'borderRadius': '5px',
    'border': '2px solid black',
    'height': '135vh',
    'fontFamily': 'Helvetica',
    'backgroundImage': 'url(https://fandomwire.com/wp-content/uploads/2019/04/MCU-GROUP-cover.png)',
    'backgroundPosition': 'center',
    'backgroundRepeat': 'repeat',
    'backgroundSize': 'cover'
},

	children=[
		html.H1(children='MCU Movies Performance',
				style={'textAlign': 'top-left',
						'fontSize': 40,
						'font-weight': 'bold',
						'color': 'white',
						'marginTop': '10px',
						'marginBottom': '20px', 
                        'display': 'inline-block'}),
        html.H3(id='phase_display', className='phase_subtitle', children='',
            style={'fontSize': 30,
            'color': '#FAFAD2',
            'margin-left': '20px',
            'display': 'inline-block'}),

		dcc.Dropdown(
			id='phase_dropdown',
			options=dropdown_options,
			value='All Phases',
			style={'width': '33%'}),
    
        html.Div('Select to view results', style={
            'color':'white' 
            }),

		html.Div([
            dcc.Graph(id='box_office_chart', style={'width': '33%', 'height': '350px', 'display': 'inline-block'}),
            dcc.Graph(id='pie_chart', style={'width': '38%', 'height': '350px', 'display': 'inline-block'}),
            dcc.Graph(id='line_chart', style={'width': '29%', 'height': '350px', 'display': 'inline-block'}),
        ] , style={'margin': '5px'}),

        html.H3(
            children='Movie Trivia', 
            style={
            'background-color': 'rgba(0, 0, 0, 0.8)',
            'border-radius': '10px',
            'padding': '10px',
            'color': 'Linen','marginTop': '15px'}),

        html.Div(className='row', children=[
            html.Div(className='col-md-4', children=[
                html.Div(className='card', children=[
                    html.Div(className='card-header', children='Highest Grossing Movie', style={'font-weight': 'bold'}),
                    html.Div(className='card-body', style={'display': 'flex', 'flex-direction': 'row'}, children=[
                        html.H5(id='grossing_title', className='card-title', children='', style={
                            'font-weight': 'bold',
                            'margin-right': '5px'
                            }),
                        html.Img(id='grossing_image', className='card-img-top', style={
                            'object-fit': 'cover',
                            'width': '120px',
                            'height': '160px'}),
                        html.P(id='grossing_text', className='card-text', children='', style={'margin-left': '10px'}),
                    ]),
                ]),
            ]),

            html.Div(className='col-md-4', children=[
                html.Div(className='card', children=[
                    html.Div(className='card-header', children='Highest Rated Movie', style={'font-weight': 'bold'}),
                    html.Div(className='card-body', style={'display': 'flex', 'flex-direction': 'row'}, children=[
                        html.H5(id='rated_title', className='card-title', style={
                            'font-weight': 'bold',
                            'margin-right': '5px'}, children=''),
                        html.Img(id='rated_image', className='card-img-top', style={
                            'object-fit': 'cover', 
                            'width': '120px',
                            'height': '160px'}),
                        html.P(id='rated_text', className='card-text', children='', style={'margin-left': '10px'}),
                    ]),
                ]),
            ]),

            html.Div(className='col-md-4', children=[
                html.Div(className='card', children=[
                    html.Div(className='card-header', children='Most Expensive Movie', style={'font-weight': 'bold'}),
                    html.Div(className='card-body', style={'display': 'flex', 'flex-direction': 'row'}, children=[
                        html.H5(id='expensive_title', className='card-title', children='', style={
                            'font-weight': 'bold',
                            'margin-right': '5px'}),
                        html.Img(id='expensive_image', className='card-img-top', style={
                            'object-fit': 'cover',
                            'width': '120px',
                            'height': '160px'}),
                        html.P(id='expensive_text', className='card-text', style={'margin-left': '10px'}, children=''),
                    ]),
                ]),
            ]),
        ]),

        html.Div([
            html.Br(),
            html.A('Visit My Home Page', href='https://lhprojectportfolio.w3spaces.com/')
            ], style={
                'font-size': '10px',
                'color': 'white',
                'textAlign': 'center',
                'margin': 'auto'})
    
    ]
)

#Define app call back Phase sub-title
@app.callback(
    Output('phase_display', 'children'),
    [Input('phase_dropdown', 'value')])

def update_phase_title(phase):
    filtered_df = df[df['Phase'] == phase]

    if phase == 'All Phases':
        phase_display = "All Phases"
    else:
        phase_display = f"{filtered_df.iloc[0]['Phase']}"

    return phase_display

# Define app callback of bar chart
@app.callback(
	Output('box_office_chart', 'figure'),
	[Input('phase_dropdown', 'value')]
)
def update_box_office_chart(phase):
	if phase == 'All Phases':
		filtered_df = df
	else:
		filtered_df = df[df['Phase'] == phase]

	data = [go.Bar(
        x=filtered_df['Film'],
        y=filtered_df['Box office gross Worldwide'],
        hoverinfo='x+y',
        marker=dict(color=filtered_df['Phase'].map(colors))
	)]

	layout = go.Layout(
		title=dict(
			text='Worldwide Box Office',
			font=dict(family='Helvetica'),
			x=0
		),
		xaxis=dict(title=' ', tickfont=dict(size=10)),
		yaxis=dict(title='Box Office Amount', tickprefix='$'),
		plot_bgcolor='rgba(0, 0, 0, 0.7)',
		paper_bgcolor='rgba(0, 0, 0, 0.7)',
		font=dict(color='white', family='Helvetica'),
		bargap=0.2,
	)

	fig = go.Figure(data=data, layout=layout)
	fig.update_layout(title_font=dict(size=20))

	return fig

# Define app callback of pie chart
@app.callback(
    Output('pie_chart', 'figure'),
    [Input('phase_dropdown', 'value')]
)
def update_pie_chart(phase):
    if phase == 'All Phases':
        filtered_df = df
    else:
        filtered_df = df[df['Phase'] == phase]

    data = [go.Pie(
        labels=filtered_df['Film'],
        values=filtered_df['Box office gross Worldwide'],
        hole=0.38,
        hoverinfo='label+percent',
        )]

    layout = go.Layout(
        title=dict(
            text='Movie Box Office Share',
            font=dict(family='Helvetica'),
        ),
        plot_bgcolor='rgba(0, 0, 0, 0.7)',
        paper_bgcolor='rgba(0, 0, 0, 0.7)',
        font=dict(color='white', family='Helvetica'),
        legend=dict(
            x=1,
            y=1,
            traceorder='normal',
            font=dict(size=5),
            bgcolor='rgba(0,0,0,0)'))

    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(title_font=dict(size=20))

    return fig

# Define app callback of Line Chart
@app.callback(
    Output('line_chart', 'figure'),
    [Input('phase_dropdown', 'value')]
)
def update_line_chart(phase):
    if phase == 'All Phases':
        filtered_df_year_earning = df_year_earning
    else:
        filtered_df_year_earning = df_year_earning[df_year_earning['Phase'] == phase]

    data = [go.Line(
        x=filtered_df_year_earning['Year_Release'],
        y=filtered_df_year_earning['Total Earnings'],
        hoverinfo='x+y'
        
        )]

    layout = go.Layout(
        title=dict(
            text='Total Earning by Year',
            font=dict(family='Helvetica'),
        ),
        xaxis=dict(title='Year', tickangle=90),
        yaxis=dict(title='Total Earnings', tickprefix='$'),
        plot_bgcolor='rgba(0, 0, 0, 0.7)',
        paper_bgcolor='rgba(0, 0, 0, 0.7)',
        font=dict(color='white', family='Helvetica')
    )

    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(title_font=dict(size=20))

    return fig

#Define app Callback for cards
@app.callback(
    [Output("grossing_image", "src"),
     Output("grossing_title", "children"),
     Output("grossing_text", "children"),
     Output("rated_image", "src"),
     Output("rated_title", "children"),
     Output("rated_text", "children"),
     Output("expensive_image", "src"),
     Output("expensive_title", "children"),
     Output("expensive_text", "children")],
    [Input("phase_dropdown", "value")])

def update_cards(phase):
    if phase == 'All Phases':
        filtered_df = df
    else:
        filtered_df = df[df['Phase'] == phase]

    # Highest Grossing Movie
    highest_grossing_movie = filtered_df[filtered_df["Box office gross Worldwide"] == filtered_df["Box office gross Worldwide"].max()]
    grossing_image = highest_grossing_movie.iloc[0]["movie_image"]
    grossing_title = highest_grossing_movie.iloc[0]['Film']
    grossing_text = f"{highest_grossing_movie.iloc[0]['Film']} was released on {highest_grossing_movie.iloc[0]['U.S. release date']}. It took in a total of ${highest_grossing_movie.iloc[0]['Box office gross Worldwide']:,.0f} in Worldwide Box Office."

    # Highest Rated Movie
    highest_rated_movie = filtered_df[filtered_df["Rotten Tomatoes Rating"] == filtered_df["Rotten Tomatoes Rating"].max()]
    rated_image = highest_rated_movie.iloc[0]["movie_image"]
    rated_title = highest_rated_movie.iloc[0]["Film"]
    rated_text = f"{highest_rated_movie.iloc[0]['Film']} Rotten Tomatoes Rating is {highest_rated_movie.iloc[0]['Rotten Tomatoes Rating']}" + '%. ' f"It recieved a CinemaScore® of {highest_rated_movie.iloc[0]['CinemaScore']}"

    # Most Expensive Movie
    most_expensive_movie = filtered_df[filtered_df["Budget"] == filtered_df["Budget"].max()]
    expensive_image = most_expensive_movie.iloc[0]["movie_image"]
    expensive_title = most_expensive_movie.iloc[0]['Film']
    expensive_text = f"{most_expensive_movie.iloc[0]['Film']} was produced with a budget of ${most_expensive_movie.iloc[0]['Budget']:,.0f}."

    return (grossing_image, grossing_title, grossing_text,
            rated_image, rated_title, rated_text,
            expensive_image, expensive_title, expensive_text)

if __name__ == '__main__':
	app.run_server(host='0.0.0.0', port=8080)

