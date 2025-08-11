
# MCU Cinematic Dashboard

## Overview

The MCU Cinematic Dashboard is a visually rich, interactive dashboard for exploring Marvel Cinematic Universe movie data. Built with Python, Dash, and Plotly, it provides quadrant-based visualizations, KPI cards, and responsive design for desktop and mobile.

## Features
- Quadrant layout: KPI cards, Rotten Tomatoes ratings, Box Office timeline, and Total Earnings pie chart
- Responsive design for all devices
- Toggleable legends for graphs
- Sorting and filtering logic for clear data presentation
- Movie posters in KPI cards (square aspect for best visuals)
- Data source attribution

## Data
- Data file: `data/box_office.csv`
- Columns: Phase, Film, Year_Release, U.S. release date, Box office gross (US/Canada, Other territories, Worldwide), Rotten Tomatoes Rating, CinemaScore, Budget, Director, Producer, movie_image


## Installation & Setup

### Local Python Installation
1. **Clone the repository**
	```bash
	git clone <your-repo-url>
	cd mcu dashboard
	```

2. **Create and activate a Python environment**
	```bash
	python -m venv venv
	source venv/bin/activate  # On Windows: venv\Scripts\activate
	```

3. **Install dependencies**
	```bash
	pip install -r requirements.txt
	```

4. **Run the dashboard**
	```bash
	python app.py
	```
	The dashboard will be available at http://127.0.0.1:8050/

### Docker Installation
1. **Build the Docker image**
	```bash
	docker build -t mcu-dashboard .
	```

2. **Run the Docker container**
	```bash
	docker run -p 8050:8050 mcu-dashboard
	```
	The dashboard will be available at http://localhost:8050/

## Usage
- Select a phase using the buttons to filter KPIs and graphs
- View KPI cards for highest/lowest grossing and highest RT rating movies
- Explore quadrant graphs:
  - **Rotten Tomatoes Ratings** (bottom left): sorted by rating, toggle legend
  - **Box Office Timeline** (top right): sorted by release date, toggle legend
  - **Total Earnings Pie** (bottom right): sorted by release date, toggle legend, large and readable
- All graphs and cards are responsive and visually optimized

## Customization
- To update data, replace `data/box_office.csv` with your own MCU movie data
- To adjust styles, edit `assets/dashboard.css`

## Troubleshooting
- If you encounter missing dependencies, run `pip install -r requirements.txt`
- For best results, use a modern browser (Chrome, Edge, Firefox)

## Credits
- Data source: MCU Box Office Wikipedia
- Dashboard by Dale

---

Enjoy exploring the MCU Cinematic Dashboard!