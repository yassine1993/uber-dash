# Marrakesh Friction Tracker V3

A professional Streamlit dashboard application for tracking driver friction points in Marrakesh operations.

## Features

- **File Upload**: Drag-and-drop CSV file uploader in the sidebar
- **Smart Fallback**: Automatic demo data generation (800 rows) if no file is uploaded
- **KPI Dashboard**: Key metrics including Total Leads, In Training, Active Drivers, Conversion Rate (with 20% threshold), and Top Friction Reason
- **Lead Source Analysis**: Breakdown of leads by source (Performance Marketing, Referral, Physical) with conversion rates
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
- `Lead_Source`: Source of the lead:
  - Performance Marketing: `Performance_Marketing_FB`, `Performance_Marketing_TikTok`, `Performance_Marketing_Google`
  - Referral: `Referral`
  - Physical: `Physical_Tent`, `Physical_Hub`

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
