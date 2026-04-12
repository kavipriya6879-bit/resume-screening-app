import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Candidate Screening App", layout="wide")
st.title("🎯 Smart Candidate Screening App")

try:
    # Unga Excel file name-ah inga correct-ah kuduthuruken
    df = pd.read_excel('candidates_resume_data_100.xlsx', engine='openpyxl')
    
    st.sidebar.header("Filter Candidates")
    
    # 1. Name search
    search = st.sidebar.text_input("Candidate Name search panna:")
    
    # 2. Qualification filter (Excel-la irukura column name 'Degree' nu iruka-nu check pannunga)
    if 'Degree' in df.columns:
        qual_options = ["All"] + list(df['Degree'].unique())
        selected_qual = st.sidebar.selectbox("Qualification select pannunga:", qual_options)
        
        filtered_df = df.copy()
        if search:
            filtered_df = filtered_df[filtered_df['Name'].str.contains(search, case=False, na=False)]
        if selected_qual != "All":
            filtered_df = filtered_df[filtered_df['Degree'] == selected_qual]
            
        st.subheader(f"Results: {len(filtered_df)} candidates found")
        st.dataframe(filtered_df, use_container_width=True)
    else:
        # Oru velai 'Degree' nu column illana, ellathaiyum kaatum
        st.warning("Note: 'Degree' nu column illa, so filtering apply aagala.")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")
    st.info("Kabi, GitHub-la file name 'candidates_resume_data_100.xlsx' nu correct-ah iruka-nu check pannunga.")
