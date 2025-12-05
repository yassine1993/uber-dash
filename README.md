# Marrakesh Friction Tracker

A professional Streamlit dashboard application for tracking driver friction points in Marrakesh operations.

## Features

- **File Upload**: Drag-and-drop CSV file uploader in the sidebar
- **Smart Fallback**: Automatic demo data generation (800 rows) if no file is uploaded
- **KPI Dashboard**: Key metrics including Total Leads, Active Drivers, Conversion Rate, and Top Friction Reason
- **Visualizations**: 
  - Volume by Station (bar chart colored by status)
  - Top Friction Reasons (horizontal bar chart)
- **Action List**: Drivers stuck at 'Docs_Submitted' status
- **Export**: Download processed data as CSV

## Data Format

The CSV file should contain the following columns:
- `Station`: Station name (e.g., "Bab Doukkala", "Airport")
- `Status`: Driver status (Contacted, Tea_Station_Visit, Docs_Submitted, Active)
- `Friction_Reason`: Reason for friction (Permit_Scan_Fail, App_Confusion, None)

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

## Netlify Deployment

**Note:** Streamlit apps are typically best deployed on [Streamlit Cloud](https://streamlit.io/cloud) (free and easy). However, if deploying to Netlify:

1. Connect your repository to Netlify
2. The `netlify.toml` file is already configured
3. You may need to use Netlify's serverless functions or consider alternative deployment methods

**Recommended:** For easiest deployment, use Streamlit Cloud:
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository and deploy!

## Logo

Place your Uber logo PNG file in the root directory (named `logo.png`, `uber.png`, or similar) and it will automatically appear in the header.

## Requirements

- Python 3.11+
- Streamlit 1.28.0+
- Pandas 2.0.0+
- Plotly 5.17.0+

