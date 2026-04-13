import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Page Configuration & Custom Styling ---
st.set_page_config(page_title="JK Smart Hiring", page_icon="🎯", layout="wide")

# Custom CSS for UI Enhancement
st.markdown("""
    <style>
    /* Styling for the entire app */
    .main {
        background-color: #f0f2f6; /* Subtle grey background */
    }
    
    /* Title styling */
    .stTitle {
        color: #003366; /* Deep blue for titles */
        font-family: 'Montserrat', 'Open Sans', Helvetica, Arial, sans-serif;
        font-weight: 700;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Subheader styling */
    .stSubheader {
        color: #1E90FF; /* Dodger blue for subheaders */
        font-weight: 600;
    }
    
    /* Sidebar header styling */
    .stSidebar .stSidebarHeader {
        background-color: #003366;
        color: #FFFFFF;
        padding: 10px;
        font-size: 20px;
        text-align: center;
        border-radius: 5px;
    }
    
    /* DataFrame styling */
    .stDataFrame {
        border: 2px solid #DDDDDD;
        border-radius: 10px;
        background-color: #FFFFFF;
    }
    
    /* Custom button styling */
    .stButton > button {
        background-color: #008CBA;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>
    """, unsafe_safe_origin=True)

# --- 2. Logo and Header Section ---
with st.container():
    # Style JK elegantly
    logo_col, title_col = st.columns([1, 4])
    
    with logo_col:
        st.markdown(
            """
            <div style="background-color:#003366; color:white; border-radius:10px; padding:20px; text-align:center;">
                <h1 style="margin:0; font-size:40px; font-family:'Playfair Display', serif;">JK</h1>
                <p style="margin:0; font-size:12px; font-weight:lighter;">Smart Hiring</p>
            </div>
            """, 
            unsafe_safe_origin=True
        )
    
    with title_col:
        st.title("🎯 Smart Candidate Screening Dashboard")
        st.write("Unga Excel file-la irukura candidates-ah inga filter panni paakalam.")

# --- 3. File Loading and Sidebar ---
try:
    # Read the data file
    df = pd.read_excel('candidates_resume_data_100.xlsx', engine='openpyxl')
    
    # Sidebar - Screening Filters
    st.sidebar.markdown("<div class='stSidebarHeader'>🔍 Screening Panel</div>", unsafe_safe_origin=True)
    
    # 1. Name Search
    search = st.sidebar.text_input("Name search:")
    
    # 2. Skill Filter
    if 'Skills' in df.columns:
        all_skills = set()
        for s in df['Skills'].dropna():
            for skill in str(s).split(','):
                all_skills.add(skill.strip())
        selected_skill = st.sidebar.selectbox("Skill match:", ["All"] + sorted(list(all_skills)))
    else:
        selected_skill = "All"

    # 3. Experience Slider (Selecting the BEST ones)
    if 'Experience_Years' in df.columns:
        # Top 10 experience-ah highlgiht pannuvom
        top_exp_score = df['Experience_Years'].nlargest(10).min()
        st.sidebar.info(f"Top 10 candidates have {top_exp_score}+ years of experience.")
        
        # Best Candidates Slider
        min_exp = st.sidebar.slider("Show Best Candidates with Minimum Experience (Years):", 0, int(df['Experience_Years'].max()), 0)
    else:
        min_exp = 0

    # --- 4. Advanced Visualization (Optional - Sir-ku impress panna) ---
    st.divider()
    
    if 'Location' in df.columns:
        st.subheader("🌐 Global Talent Pool")
        # Sample location data if not present, but better to check
        location_counts = df['Location'].value_counts().reset_index()
        location_counts.columns = ['Location', 'Candidate Count']
        
        # Create a simple bubble map (assuming Locations are city names)
        # For a true map, we'd need lat/long, but city names will work partially
        # In a real app, we'd add geocoding, but let's stick to simple counts for now
        fig = px.scatter_geo(location_counts, locations="Location", locationmode="country names",
                            hover_name="Location", size="Candidate Count",
                            projection="natural earth", title="Candidate Locations Distribution")
        st.plotly_chart(fig, use_container_width=True)
        st.write("*(Note: For city locations to appear accurately on the map, geocoding would be required. Here we just plot based on country names.)*")

    # --- 5. Filtering Logic ---
    filtered_df = df.copy()
    if search:
        filtered_df = filtered_df[filtered_df['Name'].str.contains(search, case=False, na=False)]
    if selected_skill != "All":
        filtered_df = filtered_df[filtered_df['Skills'].str.contains(selected_skill, case=False, na=False)]
    if min_exp > 0:
        filtered_df = filtered_df[filtered_df['Experience_Years'] >= min_exp]

    # --- 6. Results Display (Professional Dataframe) ---
    st.divider()
    
    st.subheader(f"✅ Found {len(filtered_df)} Best Candidates")
    
    # Highlight the top candidates row style
    def highlight_experience(s):
        if s.Experience_Years >= top_exp_score:
            return ['background-color: #E6F3FF'] * len(s)
        else:
            return [''] * len(s)

    # st.dataframe(filtered_df, use_container_width=True)
    st.dataframe(filtered_df.style.apply(highlight_experience, axis=1), use_container_width=True)
    
    # Optional - Download Filtered List
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Candidate List (CSV)",
        data=csv,
        file_name="filtered_candidates.csv",
        mime="text/csv",
    )

except Exception as e:
    st.error(f"Error loading the data: {e}. GitHub-la file name correct-ah iruka-nu check pannunga.")



