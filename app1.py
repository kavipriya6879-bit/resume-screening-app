import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="JK Smart Hiring", page_icon="🎯", layout="wide")

# 2. Stylish UI with JK Logo (Fixed Error Version)
st.markdown("""
    <div style="background-color:#003366; color:white; border-radius:15px; padding:30px; text-align:center; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
        <h1 style="margin:0; font-size:50px; font-family:'Arial Black';">JK</h1>
        <p style="margin:0; font-size:18px; font-weight:lighter; letter-spacing: 2px;">SMART CANDIDATE SCREENER</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

# 3. Loading Data
try:
    # CSV file-ah read pannudhu. sep=None potta automatic-ah comma/semicolon detect pannum
    df = pd.read_csv('Candidates_Resume_Data.csv', sep=None, engine='python')
    
    # Sidebar Setup
    st.sidebar.markdown("<h2 style='text-align: center; color: #003366;'>🔍 Filter Panel</h2>", unsafe_allow_html=True)
    
    # Filter 1: Name Search
    search = st.sidebar.text_input("Name vechu search panna:")
    
    # Filter 2: Skills Filter (Automatic Scan)
    if 'Skills' in df.columns:
        all_skills = set()
        for s in df['Skills'].dropna():
            for skill in str(s).split(','):
                all_skills.add(skill.strip())
        selected_skill = st.sidebar.selectbox("Skill match panna:", ["All"] + sorted(list(all_skills)))
    else:
        selected_skill = "All"

    # Filter 3: Experience Slider
    if 'Experience_Years' in df.columns:
        min_exp = st.sidebar.slider("Min Experience (Years):", 0, int(df['Experience_Years'].max()), 0)
    else:
        min_exp = 0

    # --- Filtering Logic ---
    filtered_df = df.copy()
    
    if search:
        filtered_df = filtered_df[filtered_df['Name'].str.contains(search, case=False, na=False)]
    
    if selected_skill != "All":
        filtered_df = filtered_df[filtered_df['Skills'].str.contains(selected_skill, case=False, na=False)]
        
    if min_exp > 0:
        filtered_df = filtered_df[filtered_df['Experience_Years'] >= min_exp]

    # --- Display Results ---
    st.subheader(f"✅ Found {len(filtered_df)} Matching Candidates")
    
    # Data-va professional-ah kaata
    st.dataframe(filtered_df, use_container_width=True)

    # Optional: Download Button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered List",
        data=csv,
        file_name="JK_Filtered_Candidates.csv",
        mime="text/csv",
    )

except Exception as e:
    st.error(f"Error: {e}")
    st.info("Kabi, GitHub-la 'Candidates_Resume_Data.csv' file-ah correct-ah upload panniteengala-nu check pannunga.")

# Footer
st.markdown("<br><hr><center>Developed for JK Professional Hiring Team</center>", unsafe_allow_html=True)
