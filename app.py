import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO
import random
import os

# Page configuration
st.set_page_config(
    page_title="Uber Marrakesh Ops",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Uber-style black/grey theme
st.markdown("""
    <style>
    .main {
        background-color: #000000;
    }
    .stApp {
        background-color: #000000;
    }
    .metric-card {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #333333;
    }
    h1 {
        color: #ffffff;
    }
    h2, h3 {
        color: #ffffff;
    }
    .stMarkdown {
        color: #ffffff;
    }
    .stDataFrame {
        background-color: #1a1a1a;
    }
    .info-box {
        background-color: #1a1a1a;
        padding: 25px;
        border-radius: 10px;
        border: 1px solid #333333;
        margin: 20px 0;
    }
    .feature-box {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #333333;
        margin: 15px 0;
    }
    .button-container {
        text-align: center;
        margin: 30px 0;
    }
    .attention-metric {
        color: #ff4444 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'df' not in st.session_state:
    st.session_state.df = None
if 'use_demo' not in st.session_state:
    st.session_state.use_demo = False

# Demo data generation function
def get_demo_data():
    """Generate realistic dummy data for the dashboard"""
    stations = [
        "Bab Doukkala", "Airport", "Gueliz", "Medina", "Hivernage",
        "Agdal", "Hay Riad", "Sidi Youssef Ben Ali", "Massira", "Targa"
    ]
    
    statuses = ["Contacted", "Tea_Station_Visit", "Docs_Submitted", "Training_In_Progress", "Active"]
    
    # Lead sources
    lead_sources = ["Performance_Marketing_FB", "Performance_Marketing_TikTok", "Performance_Marketing_Google", 
                    "Referral", "Physical_Tent", "Physical_Hub"]
    
    # Friction reasons based on status
    friction_mapping = {
        "Contacted": ["Not_Interested", "Trust_Issue", "None"],
        "Tea_Station_Visit": ["Not_Interested", "Trust_Issue", "None"],
        "Docs_Submitted": ["Permit_Scan_Fail", "CIN_Expired", "None"],
        "Training_In_Progress": ["GPS_Confusion", "Failed_Tech_Quiz", "Skipped_Session", "None"],
        "Active": ["None"]
    }
    
    # Status weights vary by lead source to reflect different conversion rates
    # Referral: ~53% conversion rate (Active status gets 53% weight)
    # Other sources: ~15-20% conversion rate (Active status gets 15-20% weight)
    status_weights_by_source = {
        "Referral": [0.10, 0.12, 0.15, 0.10, 0.53],  # High conversion: 53% Active
        "Physical_Tent": [0.15, 0.20, 0.25, 0.20, 0.20],  # 20% Active
        "Physical_Hub": [0.15, 0.20, 0.25, 0.20, 0.20],  # 20% Active
        "Performance_Marketing_FB": [0.20, 0.20, 0.25, 0.20, 0.15],  # 15% Active
        "Performance_Marketing_TikTok": [0.20, 0.20, 0.25, 0.20, 0.15],  # 15% Active
        "Performance_Marketing_Google": [0.20, 0.20, 0.25, 0.20, 0.15],  # 15% Active
    }
    
    # Distribution of lead sources
    lead_source_weights = [0.25, 0.20, 0.15, 0.15, 0.15, 0.10]  # Distribution of lead sources
    
    data = []
    for i in range(800):
        station = random.choice(stations)
        lead_source = random.choices(lead_sources, weights=lead_source_weights)[0]
        
        # Assign status based on lead source (to reflect different conversion rates)
        status_weights = status_weights_by_source[lead_source]
        status = random.choices(statuses, weights=status_weights)[0]
        
        # Assign friction reason based on status
        available_frictions = friction_mapping[status]
        friction_weights = [0.30, 0.30, 0.20, 0.20] if len(available_frictions) == 4 else [0.35, 0.35, 0.30]
        friction_reason = random.choices(available_frictions, weights=friction_weights[:len(available_frictions)])[0]
        
        data.append({
            "Station": station,
            "Status": status,
            "Friction_Reason": friction_reason,
            "Lead_Source": lead_source
        })
    
    return pd.DataFrame(data)

# CSV Template generation function
def get_csv_template():
    """Generate a CSV template with example rows"""
    template_data = {
        "Station": ["Bab Doukkala", "Airport", "Gueliz", "Medina", "Hivernage", "Agdal"],
        "Status": ["Contacted", "Tea_Station_Visit", "Docs_Submitted", "Training_In_Progress", "Active", "Contacted"],
        "Friction_Reason": ["None", "Permit_Scan_Fail", "CIN_Expired", "GPS_Confusion", "None", "Not_Interested"],
        "Lead_Source": ["Performance_Marketing_FB", "Physical_Tent", "Referral", "Performance_Marketing_TikTok", "Physical_Hub", "Performance_Marketing_Google"]
    }
    return pd.DataFrame(template_data)

# Logo and Header
logo_paths = ['logo.png', 'uber.png', 'Uber.png', 'logo.PNG', 'uber.PNG']
logo_found = None

for path in logo_paths:
    if os.path.exists(path):
        logo_found = path
        break

    # Landing Page
if not st.session_state.data_loaded:
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if logo_found:
            st.image(logo_found, width=150, use_container_width=False)
        st.markdown("<h1 style='text-align: center; color: #ffffff; margin-bottom: 5px;'>Uber Marrakesh Ops</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #cccccc; margin-top: 0; margin-bottom: 20px;'>Ambassador Performance & Friction Tracker</h3>", unsafe_allow_html=True)
        
        # Status Definitions - Always Visible
        st.markdown("""
        <div style='background-color: #1a1a1a; padding: 20px; border-radius: 8px; border: 1px solid #333333; margin: 20px 0;'>
            <h3 style='color: #ffffff; margin-bottom: 15px;'>ℹ️ Operational Status Definitions</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Use native Streamlit markdown for content
        st.markdown("**Contacted:** An Ambassador has approached the driver at a taxi stand, pitched the value proposition, and logged their phone number. *Goal: Move them to the Tea Station.*")
        st.markdown("")
        st.markdown("**Tea Station Visit:** The driver has physically sat down at a Greenlight Hub/Tent. This indicates \"High Intent\" (they invested time to drink tea and listen). *Goal: Start the document upload process.*")
        st.markdown("")
        st.markdown("**Docs Submitted:** All legal documents (Permit de Confiance, License, CIN, Carte Grise) have been scanned and uploaded to the system. *Goal: Verify documents and start tech training.*")
        st.markdown("")
        st.markdown("**Training In Progress:** Documents are valid, but the driver is currently undergoing the \"Tech Literacy\" module (learning to accept rides, use GPS, and understand safety guidelines). *Goal: Pass the \"First Trip\" simulation.*")
        st.markdown("")
        st.markdown("**Active:** The driver has successfully completed their first paid trip on the platform within the last 7 days. *Goal: Retention and \"Captain's Club\" entry.*")
        
        st.markdown("<hr style='border-color: #333333;'>", unsafe_allow_html=True)
    
    # Welcome Section
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        <div class="info-box">
            <h2 style='color: #ffffff; text-align: center; margin-bottom: 20px;'>Welcome to the Ambassador Performance & Friction Tracker</h2>
            <p style='color: #cccccc; font-size: 18px; line-height: 1.6; text-align: center;'>
                Track driver onboarding progress across Marrakesh operations. Monitor conversion funnels, 
                identify friction points, and optimize the journey from initial contact to active driver status.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # What We Track Section
    st.markdown("<h2 style='color: #ffffff; text-align: center; margin-top: 30px;'>What We Track</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3 style='color: #ffffff; margin-bottom: 15px;'>📍 Station Performance</h3>
            <p style='color: #cccccc; line-height: 1.6;'>
                Monitor driver volume and conversion rates across all Marrakesh stations. 
                Identify which stations are performing best and where improvements are needed.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h3 style='color: #ffffff; margin-bottom: 15px;'>📊 Driver Status Pipeline</h3>
            <p style='color: #cccccc; line-height: 1.6;'>
                Track drivers through the complete onboarding journey from initial contact 
                to active status, including the critical training phase.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3 style='color: #ffffff; margin-bottom: 15px;'>⚠️ Friction Analysis</h3>
            <p style='color: #cccccc; line-height: 1.6;'>
                Identify friction points at each stage:
                <ul style='color: #cccccc; line-height: 1.8;'>
                    <li><strong>Contact:</strong> Not Interested, Trust Issues</li>
                    <li><strong>Docs:</strong> Permit Scan Fail, CIN Expired</li>
                    <li><strong>Training:</strong> GPS Confusion, Failed Tech Quiz, Skipped Session</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h3 style='color: #ffffff; margin-bottom: 15px;'>🎯 Key Metrics</h3>
            <p style='color: #cccccc; line-height: 1.6;'>
                Real-time insights into:
                <ul style='color: #cccccc; line-height: 1.8;'>
                    <li>Total leads and active drivers</li>
                    <li>Drivers in training (needs attention)</li>
                    <li>Conversion rates by station</li>
                    <li>Top friction reasons</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: #333333; margin: 40px 0;'>", unsafe_allow_html=True)
    
    # Data Selection Section
    st.markdown("<h2 style='color: #ffffff; text-align: center; margin-top: 30px;'>Get Started</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #cccccc; text-align: center; font-size: 16px; margin-bottom: 30px;'>Choose how you'd like to load data to begin analyzing</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # CSV Format Information
        with st.expander("📋 CSV Format Requirements", expanded=True):
            st.markdown("""
            <div style='background-color: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333333;'>
                <h4 style='color: #ffffff; margin-bottom: 10px;'>Required Columns:</h4>
                <ul style='color: #cccccc; line-height: 1.8;'>
                    <li><strong>Station</strong> - Station name (e.g., "Bab Doukkala", "Airport", "Gueliz")</li>
                    <li><strong>Status</strong> - Driver status: <code>Contacted</code>, <code>Tea_Station_Visit</code>, <code>Docs_Submitted</code>, <code>Training_In_Progress</code>, or <code>Active</code></li>
                    <li><strong>Friction_Reason</strong> - Friction reason based on status:
                        <ul style='margin-top: 5px;'>
                            <li>Contact/Tea Station: <code>Not_Interested</code>, <code>Trust_Issue</code>, <code>None</code></li>
                            <li>Docs: <code>Permit_Scan_Fail</code>, <code>CIN_Expired</code>, <code>None</code></li>
                            <li>Training: <code>GPS_Confusion</code>, <code>Failed_Tech_Quiz</code>, <code>Skipped_Session</code>, <code>None</code></li>
                            <li>Active: <code>None</code></li>
                        </ul>
                    </li>
                    <li><strong>Lead_Source</strong> - Source of the lead:
                        <ul style='margin-top: 5px;'>
                            <li>Performance Marketing: <code>Performance_Marketing_FB</code>, <code>Performance_Marketing_TikTok</code>, <code>Performance_Marketing_Google</code></li>
                            <li>Referral: <code>Referral</code></li>
                            <li>Physical: <code>Physical_Tent</code>, <code>Physical_Hub</code></li>
                        </ul>
                    </li>
                </ul>
                <p style='color: #cccccc; margin-top: 15px;'>
                    <strong>Note:</strong> Column names are case-sensitive and must match exactly.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Download Template Button
            template_df = get_csv_template()
            template_csv = template_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV Template",
                data=template_csv,
                file_name="marrakesh_friction_template.csv",
                mime="text/csv",
                use_container_width=True,
                help="Download a template CSV file with example data and correct format"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # File Upload Section
        st.markdown("### 📁 Upload Your Data")
        uploaded_file = st.file_uploader(
            "Upload CSV File",
            type=['csv'],
            help="Upload a CSV file with columns: Station, Status, Friction_Reason, Lead_Source",
            key="file_uploader"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                # Validate required columns
                required_cols = ['Station', 'Status', 'Friction_Reason', 'Lead_Source']
                if not all(col in df.columns for col in required_cols):
                    st.error(f"❌ CSV must contain columns: {', '.join(required_cols)}")
                    st.info(f"Your CSV has columns: {', '.join(df.columns.tolist())}")
                else:
                    st.success(f"✅ File loaded successfully! Found {len(df)} rows.")
                    if st.button("🚀 Go to Dashboard", use_container_width=True, type="primary"):
                        st.session_state.df = df
                        st.session_state.use_demo = False
                        st.session_state.data_loaded = True
                        st.rerun()
            except Exception as e:
                st.error(f"❌ Error reading CSV file: {str(e)}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666666;'>— OR —</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Demo Data Section
        st.markdown("### 📊 Use Demo Data")
        st.markdown("<p style='color: #cccccc;'>Explore the dashboard with realistic sample data (800 rows)</p>", unsafe_allow_html=True)
        
        if st.button("🎮 Load Demo Data", use_container_width=True, type="secondary"):
            df = get_demo_data()
            st.session_state.df = df
            st.session_state.use_demo = True
            st.session_state.data_loaded = True
            st.rerun()

# Dashboard Page
else:
    df = st.session_state.df
    
    # Header with back button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if logo_found:
            st.image(logo_found, width=150, use_container_width=False)
        st.markdown("<h1 style='text-align: center; color: #ffffff; margin-bottom: 5px;'>Uber Marrakesh Ops</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #cccccc; margin-top: 0; margin-bottom: 20px;'>Ambassador Performance & Friction Tracker</h3>", unsafe_allow_html=True)
        
        # Status Definitions - Always Visible
        st.markdown("""
        <div style='background-color: #1a1a1a; padding: 20px; border-radius: 8px; border: 1px solid #333333; margin: 20px 0;'>
            <h3 style='color: #ffffff; margin-bottom: 15px;'>ℹ️ Operational Status Definitions</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Use native Streamlit markdown for content
        st.markdown("**Contacted:** An Ambassador has approached the driver at a taxi stand, pitched the value proposition, and logged their phone number. *Goal: Move them to the Tea Station.*")
        st.markdown("")
        st.markdown("**Tea Station Visit:** The driver has physically sat down at a Greenlight Hub/Tent. This indicates \"High Intent\" (they invested time to drink tea and listen). *Goal: Start the document upload process.*")
        st.markdown("")
        st.markdown("**Docs Submitted:** All legal documents (Permit de Confiance, License, CIN, Carte Grise) have been scanned and uploaded to the system. *Goal: Verify documents and start tech training.*")
        st.markdown("")
        st.markdown("**Training In Progress:** Documents are valid, but the driver is currently undergoing the \"Tech Literacy\" module (learning to accept rides, use GPS, and understand safety guidelines). *Goal: Pass the \"First Trip\" simulation.*")
        st.markdown("")
        st.markdown("**Active:** The driver has successfully completed their first paid trip on the platform within the last 7 days. *Goal: Retention and \"Captain's Club\" entry.*")
        
        st.markdown("<hr style='border-color: #333333;'>", unsafe_allow_html=True)
    
    # Sidebar with data info and reset option
    with st.sidebar:
        st.markdown("<h2 style='color: #ffffff;'>Data Source</h2>", unsafe_allow_html=True)
        
        if st.session_state.use_demo:
            st.info("📊 Using Demo Data")
            st.caption(f"Total rows: {len(df):,}")
        else:
            st.success("📁 Using Uploaded CSV")
            st.caption(f"Total rows: {len(df):,}")
        
        st.markdown("<hr style='border-color: #333333;'>", unsafe_allow_html=True)
        
        if st.button("🔄 Start Over", use_container_width=True):
            st.session_state.data_loaded = False
            st.session_state.df = None
            st.session_state.use_demo = False
            st.rerun()
    
    # Main Dashboard
    # KPI Metrics
    st.markdown("<h2 style='color: #ffffff; margin-top: 20px;'>Key Performance Indicators</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_leads = len(df)
    in_training = len(df[df['Status'] == 'Training_In_Progress'])
    active_drivers = len(df[df['Status'] == 'Active'])
    conversion_rate = (active_drivers / total_leads * 100) if total_leads > 0 else 0
    threshold = 20.0
    
    # Get top friction reason (excluding 'None')
    friction_counts = df[df['Friction_Reason'] != 'None']['Friction_Reason'].value_counts()
    top_friction = friction_counts.index[0] if len(friction_counts) > 0 else "None"
    
    with col1:
        st.metric(
            label="Total Leads",
            value=f"{total_leads:,}",
            delta=None
        )
    
    with col2:
        # In Training - Red/Attention color
        st.markdown(f"""
        <div style='background-color: #1a1a1a; padding: 15px; border-radius: 8px; border: 2px solid #ff4444;'>
            <div style='color: #cccccc; font-size: 14px; margin-bottom: 5px;'>In Training</div>
            <div style='color: #ff4444; font-size: 32px; font-weight: bold;'>{in_training:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.metric(
            label="Active Drivers",
            value=f"{active_drivers:,}",
            delta=None
        )
    
    with col4:
        # Conversion Rate with threshold comparison
        threshold_met = conversion_rate >= threshold
        border_color = "#00cc96" if threshold_met else "#ff4444"
        status_text = "✅ Above" if threshold_met else "❌ Below"
        status_color = "#00cc96" if threshold_met else "#ff4444"
        
        st.markdown(f"""
        <div style='background-color: #1a1a1a; padding: 15px; border-radius: 8px; border: 2px solid {border_color};'>
            <div style='color: #cccccc; font-size: 14px; margin-bottom: 5px;'>Conversion Rate</div>
            <div style='color: {status_color}; font-size: 32px; font-weight: bold;'>{conversion_rate:.1f}%</div>
            <div style='color: #999999; font-size: 12px; margin-top: 5px;'>Threshold: {threshold}% {status_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.metric(
            label="#1 Friction Reason",
            value=top_friction.replace('_', ' '),
            delta=None
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Funnel Conversion Rate Analysis
    st.markdown("<h2 style='color: #ffffff; margin-top: 20px;'>📊 Funnel Conversion Analysis</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #cccccc; margin-bottom: 20px;'>Track conversion rates at each stage of the driver onboarding funnel</p>", unsafe_allow_html=True)
    
    # Calculate funnel metrics
    funnel_stages = {
        'Total Leads': len(df),
        'Contacted': len(df[df['Status'] == 'Contacted']),
        'Tea Station Visit': len(df[df['Status'] == 'Tea_Station_Visit']),
        'Docs Submitted': len(df[df['Status'] == 'Docs_Submitted']),
        'Training In Progress': len(df[df['Status'] == 'Training_In_Progress']),
        'Active': len(df[df['Status'] == 'Active'])
    }
    
    # Calculate conversion rates between stages
    # For funnel analysis, we use cumulative approach: each stage shows % of total leads that reached it
    funnel_data = []
    total_leads = funnel_stages['Total Leads']
    
    # Define the funnel progression order
    funnel_order = ['Total Leads', 'Contacted', 'Tea Station Visit', 'Docs Submitted', 'Training In Progress', 'Active']
    
    previous_stage_count = total_leads
    previous_stage_name = 'Total Leads'
    
    for stage in funnel_order:
        count = funnel_stages[stage]
        
        if stage == 'Total Leads':
            conversion_rate = 100.0  # Starting point
            stage_conversion_rate = 100.0  # 100% of leads are leads
            drop_off = 0.0
        else:
            # Cumulative conversion: what % of total leads reached this stage
            cumulative_conversion = (count / total_leads * 100) if total_leads > 0 else 0
            
            # Stage-to-stage conversion: of those who reached previous stage, what % reached this stage
            # Only calculate if previous stage has people (to avoid >100% issues)
            if previous_stage_count > 0 and count <= previous_stage_count:
                stage_conversion_rate = (count / previous_stage_count * 100)
            elif previous_stage_count == 0:
                stage_conversion_rate = 0.0
            else:
                # If count > previous_count, it means data doesn't follow strict funnel
                # Use cumulative instead
                stage_conversion_rate = cumulative_conversion
            
            conversion_rate = cumulative_conversion
            drop_off = ((previous_stage_count - count) / previous_stage_count * 100) if previous_stage_count > 0 else 0
        
        funnel_data.append({
            'Stage': stage,
            'Count': count,
            'Cumulative Conversion (%)': conversion_rate,
            'Stage Conversion (%)': stage_conversion_rate if stage != 'Total Leads' else 100.0,
            'Drop-off Rate (%)': drop_off
        })
        
        previous_stage_count = count
        previous_stage_name = stage
    
    funnel_df = pd.DataFrame(funnel_data)
    
    # Visual Funnel Chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create funnel visualization
        fig_funnel = go.Figure()
        
        stages = funnel_df['Stage'].tolist()
        counts = funnel_df['Count'].tolist()
        max_count = max(counts)
        
        # Create funnel shape
        for i, (stage, count) in enumerate(zip(stages, counts)):
            width = (count / max_count) * 100 if max_count > 0 else 0
            fig_funnel.add_trace(go.Bar(
                y=[stage],
                x=[count],
                orientation='h',
                marker=dict(
                    color=['#636EFA', '#EF553B', '#FFA15A', '#FF6B35', '#00CC96', '#00CC96'][i],
                    line=dict(color='#333333', width=1)
                ),
                cumulative_cr = funnel_df.iloc[i]['Cumulative Conversion (%)']
                text=[f"{count:,}<br>({cumulative_cr:.1f}% of total)"],
                textposition='inside',
                name=stage
            ))
        
        fig_funnel.update_layout(
            title="Funnel Visualization - Volume at Each Stage",
            xaxis_title="Number of Drivers",
            yaxis_title="Stage",
            plot_bgcolor='#1a1a1a',
            paper_bgcolor='#000000',
            font_color='#ffffff',
            title_font_color='#ffffff',
            xaxis=dict(gridcolor='#333333'),
            yaxis=dict(gridcolor='#333333'),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig_funnel, use_container_width=True)
    
    with col2:
        # Conversion rate metrics
        st.markdown("<h4 style='color: #ffffff; margin-bottom: 15px;'>Stage Conversion Rates</h4>", unsafe_allow_html=True)
        
        for i in range(1, len(funnel_df)):
            stage = funnel_df.iloc[i]['Stage']
            prev_stage = funnel_df.iloc[i-1]['Stage']
            cr = funnel_df.iloc[i]['Conversion Rate (%)']
            count = funnel_df.iloc[i]['Count']
            prev_count = funnel_df.iloc[i-1]['Count']
            
            # Color based on conversion rate (cap at 100% for display)
            display_cr = min(cr, 100.0)  # Cap at 100% for display
            if display_cr >= 80:
                color = "#00cc96"
            elif display_cr >= 60:
                color = "#ffa15a"
            else:
                color = "#ff4444"
            
            # Show warning if > 100%
            warning_text = " ⚠️" if cr > 100 else ""
            cr_text = f"{display_cr:.1f}%" if cr <= 100 else f"{cr:.1f}%*"
            
            st.markdown(f"""
            <div style='background-color: #1a1a1a; padding: 12px; border-radius: 6px; border-left: 4px solid {color}; margin-bottom: 10px;'>
                <div style='color: #ffffff; font-weight: bold; font-size: 14px;'>{prev_stage} → {stage}{warning_text}</div>
                <div style='color: {color}; font-size: 24px; font-weight: bold; margin-top: 5px;'>{cr_text}</div>
                <div style='color: #999999; font-size: 12px; margin-top: 5px;'>{count:,} / {prev_count:,}</div>
                {f"<div style='color: #ffa15a; font-size: 11px; margin-top: 5px;'>*Data snapshot - not sequential flow</div>" if cr > 100 else ""}
            </div>
            """, unsafe_allow_html=True)
    
    # Detailed Funnel Metrics Table
    st.markdown("<h3 style='color: #ffffff; margin-top: 30px;'>Detailed Funnel Metrics</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #999999; font-size: 12px; margin-bottom: 15px;'>Note: Stage conversion shows % of previous stage. Values >100% indicate data snapshot where more drivers are at later stages than earlier ones (not a sequential flow).</p>", unsafe_allow_html=True)
    
    # Create enhanced table with cumulative conversion
    detailed_funnel = []
    
    for i, row in funnel_df.iterrows():
        stage = row['Stage']
        count = row['Count']
        cumulative_cr = row['Cumulative Conversion (%)']
        stage_cr = row['Stage Conversion (%)']
        drop_off = row['Drop-off Rate (%)']
        
        # Flag if stage conversion is > 100%
        stage_cr_display = f"{stage_cr:.1f}%" if stage_cr <= 100 else f"{stage_cr:.1f}%*"
        
        detailed_funnel.append({
            'Stage': stage,
            'Volume': count,
            'Cumulative Conversion (%)': cumulative_cr,
            'Stage Conversion (%)': stage_cr_display,
            'Drop-off Rate (%)': drop_off
        })
    
    detailed_funnel_df = pd.DataFrame(detailed_funnel)
    detailed_funnel_df['Volume'] = detailed_funnel_df['Volume'].apply(lambda x: f"{x:,}")
    detailed_funnel_df['Cumulative Conversion (%)'] = detailed_funnel_df['Cumulative Conversion (%)'].round(1)
    detailed_funnel_df['Drop-off Rate (%)'] = detailed_funnel_df['Drop-off Rate (%)'].round(1)
    
    st.dataframe(detailed_funnel_df, use_container_width=True, hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chart 1: Funnel Volume by Station (colored by Status)
    st.markdown("<h2 style='color: #ffffff;'>Funnel Volume by Station</h2>", unsafe_allow_html=True)
    
    station_status_counts = df.groupby(['Station', 'Status']).size().reset_index(name='Count')
    
    fig1 = px.bar(
        station_status_counts,
        x='Station',
        y='Count',
        color='Status',
        color_discrete_map={
            'Contacted': '#636EFA',
            'Tea_Station_Visit': '#EF553B',
            'Docs_Submitted': '#FFA15A',
            'Training_In_Progress': '#FF6B35',  # Distinct Orange color
            'Active': '#00CC96'
        },
        title="Funnel Volume by Station (Colored by Status)",
        labels={'Count': 'Number of Drivers', 'Station': 'Station'}
    )
    fig1.update_layout(
        plot_bgcolor='#1a1a1a',
        paper_bgcolor='#000000',
        font_color='#ffffff',
        title_font_color='#ffffff',
        xaxis=dict(gridcolor='#333333'),
        yaxis=dict(gridcolor='#333333'),
        legend=dict(bgcolor='#1a1a1a', bordercolor='#333333')
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # Chart 2: Top Friction Reasons (horizontal bar, excluding 'None')
    st.markdown("<h2 style='color: #ffffff;'>Top Friction Reasons</h2>", unsafe_allow_html=True)
    
    friction_df = df[df['Friction_Reason'] != 'None']
    friction_counts = friction_df['Friction_Reason'].value_counts().reset_index()
    friction_counts.columns = ['Friction_Reason', 'Count']
    friction_counts['Friction_Reason'] = friction_counts['Friction_Reason'].str.replace('_', ' ')
    
    fig2 = px.bar(
        friction_counts,
        x='Count',
        y='Friction_Reason',
        orientation='h',
        title="Top Friction Reasons (Excluding None)",
        labels={'Count': 'Number of Drivers', 'Friction_Reason': 'Friction Reason'},
        color='Count',
        color_continuous_scale='Greys'
    )
    fig2.update_layout(
        plot_bgcolor='#1a1a1a',
        paper_bgcolor='#000000',
        font_color='#ffffff',
        title_font_color='#ffffff',
        xaxis=dict(gridcolor='#333333'),
        yaxis=dict(gridcolor='#333333'),
        showlegend=False
    )
    fig2.update_traces(marker_color='#666666')
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Chart 3: Lead Source Breakdown
    st.markdown("<h2 style='color: #ffffff;'>Lead Source Breakdown</h2>", unsafe_allow_html=True)
    
    # Check if Lead_Source column exists
    if 'Lead_Source' in df.columns:
        # Categorize lead sources
        def categorize_lead_source(source):
            if 'Performance_Marketing' in str(source):
                return 'Performance Marketing'
            elif source == 'Referral':
                return 'Referral'
            elif 'Physical' in str(source):
                return 'Physical (Tents/Hubs)'
            else:
                return 'Other'
        
        df['Lead_Category'] = df['Lead_Source'].apply(categorize_lead_source)
        lead_source_counts = df['Lead_Category'].value_counts().reset_index()
        lead_source_counts.columns = ['Lead_Category', 'Count']
        
        # Create pie chart for overall breakdown
        fig3 = px.pie(
            lead_source_counts,
            values='Count',
            names='Lead_Category',
            title="Lead Source Distribution",
            color_discrete_map={
                'Performance Marketing': '#636EFA',
                'Referral': '#00CC96',
                'Physical (Tents/Hubs)': '#FF6B35',
                'Other': '#999999'
            }
        )
        fig3.update_layout(
            plot_bgcolor='#1a1a1a',
            paper_bgcolor='#000000',
            font_color='#ffffff',
            title_font_color='#ffffff',
            legend=dict(bgcolor='#1a1a1a', bordercolor='#333333')
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig3, use_container_width=True)
        
        # Detailed breakdown by specific source
        detailed_source_counts = df['Lead_Source'].value_counts().reset_index()
        detailed_source_counts.columns = ['Lead_Source', 'Count']
        detailed_source_counts['Lead_Source'] = detailed_source_counts['Lead_Source'].str.replace('_', ' ')
        
        fig4 = px.bar(
            detailed_source_counts,
            x='Lead_Source',
            y='Count',
            title="Detailed Lead Source Breakdown",
            labels={'Count': 'Number of Leads', 'Lead_Source': 'Lead Source'},
            color='Count',
            color_continuous_scale='Blues'
        )
        fig4.update_layout(
            plot_bgcolor='#1a1a1a',
            paper_bgcolor='#000000',
            font_color='#ffffff',
            title_font_color='#ffffff',
            xaxis=dict(gridcolor='#333333'),
            yaxis=dict(gridcolor='#333333'),
            showlegend=False
        )
        fig4.update_traces(marker_color='#4A90E2')
        
        with col2:
            st.plotly_chart(fig4, use_container_width=True)
        
        # Conversion rate by lead source
        st.markdown("<h3 style='color: #ffffff; margin-top: 20px;'>Conversion Rate by Lead Source</h3>", unsafe_allow_html=True)
        
        conversion_by_source = []
        for source in df['Lead_Source'].unique():
            source_df = df[df['Lead_Source'] == source]
            source_total = len(source_df)
            source_active = len(source_df[source_df['Status'] == 'Active'])
            source_conversion = (source_active / source_total * 100) if source_total > 0 else 0
            conversion_by_source.append({
                'Lead_Source': source.replace('_', ' '),
                'Total_Leads': source_total,
                'Active_Drivers': source_active,
                'Conversion_Rate': source_conversion
            })
        
        conversion_df = pd.DataFrame(conversion_by_source).sort_values('Conversion_Rate', ascending=False)
        
        fig5 = px.bar(
            conversion_df,
            x='Lead_Source',
            y='Conversion_Rate',
            title="Conversion Rate by Lead Source (%)",
            labels={'Conversion_Rate': 'Conversion Rate (%)', 'Lead_Source': 'Lead Source'},
            color='Conversion_Rate',
            color_continuous_scale='RdYlGn'
        )
        fig5.add_hline(y=threshold, line_dash="dash", line_color="#ff4444", 
                      annotation_text=f"Threshold: {threshold}%", 
                      annotation_position="right")
        fig5.update_layout(
            plot_bgcolor='#1a1a1a',
            paper_bgcolor='#000000',
            font_color='#ffffff',
            title_font_color='#ffffff',
            xaxis=dict(gridcolor='#333333'),
            yaxis=dict(gridcolor='#333333'),
            showlegend=False
        )
        fig5.update_traces(marker_color='#00CC96')
        
        st.plotly_chart(fig5, use_container_width=True)
        
        # Table showing detailed conversion metrics
        st.markdown("<h4 style='color: #ffffff; margin-top: 20px;'>Detailed Conversion Metrics by Lead Source</h4>", unsafe_allow_html=True)
        conversion_df['Conversion_Rate'] = conversion_df['Conversion_Rate'].round(2)
        conversion_df['Above_Threshold'] = conversion_df['Conversion_Rate'] >= threshold
        conversion_df.columns = ['Lead Source', 'Total Leads', 'Active Drivers', 'Conversion Rate (%)', 'Above Threshold']
        conversion_df['Above Threshold'] = conversion_df['Above Threshold'].map({True: '✅ Yes', False: '❌ No'})
        st.dataframe(conversion_df, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Lead_Source column not found in data. Please upload a CSV with Lead_Source column.")
    
    # Action List: Drivers in Training_In_Progress
    st.markdown("<h2 style='color: #ffffff;'>Action List: Drivers In Training</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #cccccc; margin-bottom: 15px;'>Drivers currently in training who need ambassador support to complete the tutorial</p>", unsafe_allow_html=True)
    
    training_df = df[df['Status'] == 'Training_In_Progress'].copy()
    training_df = training_df[['Station', 'Status', 'Friction_Reason']].reset_index(drop=True)
    training_df['Friction_Reason'] = training_df['Friction_Reason'].str.replace('_', ' ')
    
    if len(training_df) > 0:
        st.dataframe(
            training_df,
            use_container_width=True,
            hide_index=True
        )
        st.caption(f"Total drivers in training requiring action: {len(training_df)}")
    else:
        st.info("No drivers currently in training.")
    
    # Download Report Button
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: #333333;'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Report (CSV)",
            data=csv,
            file_name="marrakesh_friction_report.csv",
            mime="text/csv",
            use_container_width=True
        )
