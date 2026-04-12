import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="APP", layout="wide")
st.title("APP")

try:
    # Excel file-ah read pannudhu
    df = pd.read_excel('candidates_resume_data_100.xlsx', engine='openpyxl')
    
    st.sidebar.header("🔍 Advanced Filters")
    
    # 1. Search by Name
    search = st.sidebar.text_input("Name vechu search panna:")
    
    # 2. Filter by Skills (Pudhu Option!)
    # Unga Excel-la 'Skills' nu column irukanum
    if 'Skills' in df.columns:
        # Mothamulla skills-ah list edukka
        all_skills = set()
        for s in df['Skills'].dropna():
            for skill in s.split(','): # Comma vechu skills-ah pirikkurom
                all_skills.add(skill.strip())
        
        selected_skill = st.sidebar.selectbox("Skill select pannunga:", ["All"] + sorted(list(all_skills)))
    else:
        st.sidebar.warning("Note: Excel-la 'Skills' nu column illa.")
        selected_skill = "All"

    # 3. Filter by Degree
    if 'Degree' in df.columns:
        degree_options = ["All"] + list(df['Degree'].unique())
        selected_degree = st.sidebar.selectbox("Degree select pannunga:", degree_options)
    else:
        selected_degree = "All"

    # Filtering Logic
    filtered_df = df.copy()
    
    if search:
        filtered_df = filtered_df[filtered_df['Name'].str.contains(search, case=False, na=False)]
    
    if selected_skill != "All":
        filtered_df = filtered_df[filtered_df['Skills'].str.contains(selected_skill, case=False, na=False)]
        
    if selected_degree != "All":
        filtered_df = filtered_df[filtered_df['Degree'] == selected_degree]

    # Results Display
    st.subheader(f"Found {len(filtered_df)} Matching Candidates")
    st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")

