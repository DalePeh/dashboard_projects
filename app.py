import pandas as pd
import numpy as np
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px

# Load data
df = pd.read_csv('data/box_office.csv')

# KPI Calculations
def get_kpi(phase, kpi):
	phase_df = df[df['Phase'] == phase]
	if kpi == 'highest_gross':
		row = phase_df.loc[phase_df['Box office gross Worldwide'].idxmax()]
	elif kpi == 'lowest_gross':
		row = phase_df.loc[phase_df['Box office gross Worldwide'].idxmin()]
	elif kpi == 'highest_rt':
		row = phase_df.loc[phase_df['Rotten Tomatoes Rating'].idxmax()]
	else:
		return None
	return row


# Chronological phase order
phase_order = ['Phase One', 'Phase Two', 'Phase Three', 'Phase Four', 'Phase Five']
phases = ['All Phases'] + [p for p in phase_order if p in df['Phase'].unique()]


# Graph functions
def get_figures(filtered_df, legend_rt=False, legend_earnings=False, legend_timeline=False):
	palette = px.colors.qualitative.Vivid
	def shorten_title(title):
		if len(title) > 16:
			return title[:13] + '...'
		return title
	filtered_df = filtered_df.copy()
	filtered_df['ShortTitle'] = filtered_df['Film'].apply(shorten_title)

	# Always sort Rotten Tomatoes graph by rating
	filtered_df = filtered_df.sort_values('Rotten Tomatoes Rating', ascending=False)

	rt_bar = px.bar(
		filtered_df,
		x='ShortTitle',
		y='Rotten Tomatoes Rating',
		color='Phase',
		color_discrete_sequence=palette,
		title='Rotten Tomatoes Ratings by Movie',
		labels={'Rotten Tomatoes Rating': 'Rotten Tomatoes (%)', 'ShortTitle': 'Movie'},
		hover_name='Film',
		hover_data={'Rotten Tomatoes Rating': False}
	)
	rt_bar.update_traces(hovertemplate='%{hovertext}<br>%{y}%')
	rt_bar.update_layout(xaxis_tickangle=-45, xaxis_title='Movie', yaxis_title='Rotten Tomatoes (%)',
						plot_bgcolor='#111', paper_bgcolor='#111', font_color='#FFD700', showlegend=legend_rt,
						xaxis=dict(tickfont=dict(size=11)))

	# Always sort Earnings graph by release date
	pie_df = filtered_df.copy()
	pie_df['U.S. release date'] = pd.to_datetime(pie_df['U.S. release date'], errors='coerce')
	pie_df = pie_df.sort_values('U.S. release date')
	pie = px.pie(
		pie_df,
		names='Film',
		values='Box office gross Worldwide',
		title='Total Earnings Distribution',
		color_discrete_sequence=palette,
		hole=0.3,
		hover_name='Film',
		hover_data={'Box office gross Worldwide': False}
	)
	pie.update_traces(hovertemplate='%{label}<br>$%{value:,}')
	pie.update_layout(
		plot_bgcolor='#111',
		paper_bgcolor='#111',
		font_color='#FFD700',
		showlegend=legend_earnings,
		font=dict(size=18),
		legend=dict(font=dict(size=16)),
		margin=dict(t=40, b=40, l=40, r=40)
	)

	# Always sort Timeline graph by release date
	temp_df = filtered_df.copy()
	temp_df['U.S. release date'] = pd.to_datetime(temp_df['U.S. release date'], errors='coerce')
	temp_df = temp_df.sort_values('U.S. release date')
	line = px.line(
		temp_df,
		x='U.S. release date',
		y='Box office gross Worldwide',
		color='Phase',
		color_discrete_sequence=palette,
		title='Box Office Performance Timeline',
		hover_name='Film',
		hover_data={'Box office gross Worldwide': False}
	)
	line.update_traces(hovertemplate='%{hovertext}<br>$%{y:,}')
	line.update_layout(xaxis_title='Release Date', yaxis_title='Worldwide Gross ($)',
					  plot_bgcolor='#111', paper_bgcolor='#111', font_color='#FFD700', showlegend=legend_timeline)

	return rt_bar, pie, line

# App Layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, '/assets/dashboard.css'], suppress_callback_exceptions=True)
app.title = 'MCU Cinematic Dashboard'


def kpi_card(row, kpi_title):
	# Only show relevant info for each KPI
	if 'Grossing' in kpi_title:
		return html.Div([
			html.Img(src=row['movie_image'], style={'width': '100%', 'height': '140px', 'objectFit': 'cover'}),
			html.Div([
				html.H6(row['Film'], style={'fontSize': '1.2rem', 'margin': '12px 0 0 12px'}),
				html.P(kpi_title, style={'fontSize': '1.1rem', 'marginLeft': '12px'}),
				html.P(f"Gross: ${int(row['Box office gross Worldwide']):,}", style={'fontSize': '1.1rem', 'marginLeft': '12px'}),
			])
		], className='kpi-card-small')
	elif 'Rotten' in kpi_title:
		return html.Div([
			html.Img(src=row['movie_image'], style={'width': '100%', 'height': '140px', 'objectFit': 'cover'}),
			html.Div([
				html.H6(row['Film'], style={'fontSize': '1.2rem', 'margin': '12px 0 0 12px'}),
				html.P(kpi_title, style={'fontSize': '1.1rem', 'marginLeft': '12px'}),
				html.P(f"RT: {row['Rotten Tomatoes Rating']}%", style={'fontSize': '1.1rem', 'marginLeft': '12px'}),
			])
		], className='kpi-card-small')


# Dash callbacks for interactivity
from dash.dependencies import Input, Output

app.layout = html.Div([
	html.H1('MCU Cinematic Dashboard'),
	dcc.Store(id='selected-phase', data='All Phases'),
	html.Div([
		html.Div([
			# Quadrant 1: Top Left (Phase selector + KPI cards)
			html.Div([
				html.Div([
					dbc.Button('All Phase', id='btn-all-phase', color='warning', className='phase-btn'),
					dbc.Button('Phase One', id='btn-phase-one', color='warning', className='phase-btn'),
					dbc.Button('Phase Two', id='btn-phase-two', color='warning', className='phase-btn'),
					dbc.Button('Phase Three', id='btn-phase-three', color='warning', className='phase-btn'),
					dbc.Button('Phase Four', id='btn-phase-four', color='warning', className='phase-btn'),
					dbc.Button('Phase Five', id='btn-phase-five', color='warning', className='phase-btn'),
				], className='phase-buttons'),
				html.Div(id='kpi-cards', className='kpi-row-small'),
			], className='quadrant quadrant-1'),
			# Quadrant 2: Top Right (Timeline)
			html.Div([
				dbc.Checkbox(id='legend-toggle-timeline', value=False, label='Show Legend', style={'marginBottom': '8px'}),
				dcc.Graph(id='timeline-graph', className='graph-box quadrant quadrant-2')
			], className='quadrant quadrant-2'),
			# Quadrant 3: Bottom Left (Rotten Tomatoes)
			html.Div([
				dbc.Checkbox(id='legend-toggle-rt', value=False, label='Show Legend', style={'marginBottom': '8px'}),
				dcc.Graph(id='rt-graph', className='graph-box quadrant quadrant-3', style={'height': '600px'})
			], className='quadrant quadrant-3'),
			# Quadrant 4: Bottom Right (Earnings)
			html.Div([
				dbc.Checkbox(id='legend-toggle-earnings', value=False, label='Show Legend', style={'marginBottom': '8px'}),
				dcc.Graph(id='earnings-graph', className='graph-box quadrant quadrant-4', style={'height': '600px'})
			], className='quadrant quadrant-4'),
		], className='dashboard-main'),
		html.Br(),
		html.P('Data Source: MCU Box Office Wikipedia', style={'textAlign': 'center', 'color': '#888'}),
	])
])

# Callback to update selected phase
from dash.dependencies import Input, Output, State

@app.callback(
	Output('selected-phase', 'data'),
	[Input('btn-all-phase', 'n_clicks'),
	 Input('btn-phase-one', 'n_clicks'),
	 Input('btn-phase-two', 'n_clicks'),
	 Input('btn-phase-three', 'n_clicks'),
	 Input('btn-phase-four', 'n_clicks'),
	 Input('btn-phase-five', 'n_clicks')],
	[State('selected-phase', 'data')]
)
def select_phase(btn_all, btn_one, btn_two, btn_three, btn_four, btn_five, current):
	ctx = dash.callback_context
	if not ctx.triggered:
		return current
	btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
	if btn_id == 'btn-phase-one':
		return 'Phase One'
	elif btn_id == 'btn-phase-two':
		return 'Phase Two'
	elif btn_id == 'btn-phase-three':
		return 'Phase Three'
	elif btn_id == 'btn-phase-four':
		return 'Phase Four'
	elif btn_id == 'btn-phase-five':
		return 'Phase Five'
	else:
		return 'All Phases'

# Callback to update dashboard
@app.callback(
	[Output('kpi-cards', 'children'),
	 Output('rt-graph', 'figure'),
	 Output('earnings-graph', 'figure'),
	 Output('timeline-graph', 'figure')],
	[Input('selected-phase', 'data'),
	 Input('legend-toggle-rt', 'value'),
	 Input('legend-toggle-earnings', 'value'),
	 Input('legend-toggle-timeline', 'value')]
)
def update_dashboard(selected_phase, legend_rt, legend_earnings, legend_timeline):
	if selected_phase == 'All Phases':
		filtered_df = df.copy()
	else:
		filtered_df = df[df['Phase'] == selected_phase]

	# KPIs for selected phase
	kpi_cards = []
	for kpi, title in zip(['highest_gross', 'lowest_gross', 'highest_rt'],
						  ['Highest Grossing', 'Lowest Grossing', 'Highest Rotten Tomatoes']):
		row = get_kpi(selected_phase if selected_phase != 'All Phases' else filtered_df['Phase'].iloc[0], kpi)
		if row is not None:
			kpi_cards.append(kpi_card(row, title))

	# Graphs
	fig_rt, fig_earnings, fig_timeline = get_figures(
		filtered_df,
		legend_rt=legend_rt,
		legend_earnings=legend_earnings,
		legend_timeline=legend_timeline
	)
	return kpi_cards, fig_rt, fig_earnings, fig_timeline


# Expose server for Gunicorn
server = app.server

if __name__ == '__main__':
	import os
	port = int(os.environ.get('PORT', 8050))
	app.run_server(debug=False, host='0.0.0.0', port=port)
