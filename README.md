# Marrakesh Friction Tracker V3

A professional Streamlit dashboard application for tracking driver friction points in Marrakesh operations.

## Features

- **File Upload**: Drag-and-drop CSV file uploader in the sidebar
- **Smart Fallback**: Automatic demo data generation (800 rows) if no file is uploaded
- **KPI Dashboard**: Key metrics including Total Leads, In Training, Active Drivers, and Top Friction Reason
- **Visualizations**: 
  - Funnel Volume by Station (bar chart colored by status)
  - Top Friction Reasons (horizontal bar chart)
- **Action List**: Drivers currently in Training_In_Progress status
- **Export**: Download processed data as CSV

## Data Format

The CSV file should contain the following columns:
- `Station`: Station name (e.g., "Bab Doukkala", "Airport", "Gueliz")
- `Status`: Driver status - `Contacted`, `Tea_Station_Visit`, `Docs_Submitted`, `Training_In_Progress`, or `Active`
- `Friction_Reason`: Friction reason based on status:
  - Contact/Tea Station: `Not_Interested`, `Trust_Issue`, `None`
  - Docs: `Permit_Scan_Fail`, `CIN_Expired`, `None`
  - Training: `GPS_Confusion`, `Failed_Tech_Quiz`, `Skipped_Session`, `None`
  - Active: `None`

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Deployment

### ⚠️ Important: Netlify is NOT Suitable

**Netlify cannot host Streamlit apps** because Streamlit requires a persistent server process, while Netlify is designed for static sites. If you see a `netlify.toml` file in this repo, it's included for reference only and will not work for deployment.

### ✅ Recommended: Streamlit Cloud (Free & Easy)

**Streamlit Cloud** is the best option for deploying Streamlit apps:

1. Push your code to GitHub (already done if you're reading this)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository (`yassine1993/uber-dash`)
6. Set the main file path to `app.py`
7. Click "Deploy"

Your app will be live in minutes with a URL like: `https://your-app-name.streamlit.app`

### Alternative Deployment Platforms

If you prefer other options:

- **Render**: https://render.com (Free tier available)
- **Railway**: https://railway.app (Free tier available)
- **Heroku**: https://heroku.com (Paid)
- **Fly.io**: https://fly.io (Free tier available)

## Logo

Place your Uber logo PNG file in the root directory (named `logo.png`, `uber.png`, or similar) and it will automatically appear in the header.

## Requirements

- Python 3.11+
- Streamlit 1.28.0+
- Pandas 2.0.0+
- Plotly 5.17.0+

## Status Definitions

- **Contacted**: Ambassador approached driver at taxi stand, pitched value proposition, logged phone number
- **Tea Station Visit**: Driver physically sat down at Greenlight Hub/Tent (High Intent)
- **Docs Submitted**: All legal documents scanned and uploaded
- **Training In Progress**: Documents approved, currently learning App/GPS usage
- **Active**: Successfully completed first paid trip within last 7 days
