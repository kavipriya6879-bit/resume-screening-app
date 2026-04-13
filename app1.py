



import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Smart Resume Scanner", layout="wide")
st.title("🎯 Automated Resume Screening APP")

# 1. File Upload Option (Inga dhaan file-ah scan panna start pannudhu)
uploaded_file = st.file_uploader("upload your resume ", type=['xlsx', 'csv'])

if uploaded_file is not None:
    try:
        # File type-ah paathu read pannudhu
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        
        st.success("File Successfully Scanned!")
        
        # Sidebar - Advanced Filters
        st.sidebar.header("🔍 Best Candidate Filters")
        
        # 1. Search by Name
        search = st.sidebar.text_input("Name Search(optional):")
        
        # 2. Skill-based Screening
        if 'Skills' in df.columns:
            all_skills = set()
            for s in df['Skills'].dropna():
                for skill in str(s).split(','):
                    all_skills.add(skill.strip())
            selected_skill = st.sidebar.selectbox("Skill :", ["All"] + sorted(list(all_skills)))
        else:
            selected_skill = "All"

        # 3. Experience Screening (Automatic Best Candidate Logic)
        if 'Experience_Years' in df.columns:
            min_exp = st.sidebar.slider("Minimum Experience (Years):", 0, int(df['Experience_Years'].max()), 0)
        else:
            min_exp = 0

        # --- Filtering Logic ---
        filtered_df = df.copy()
        
        # Filter 1: Name
        if search:
            filtered_df = filtered_df[filtered_df['Name'].str.contains(search, case=False, na=False)]
        
        # Filter 2: Skills
        if selected_skill != "All":
            filtered_df = filtered_df[filtered_df['Skills'].str.contains(selected_skill, case=False, na=False)]
            
        # Filter 3: Experience (Selecting the BEST candidates)
        if min_exp > 0:
            filtered_df = filtered_df[filtered_df['Experience_Years'] >= min_exp]

        # Results Display
        st.subheader(f"Found {len(filtered_df)} Matching Candidates")
        
        # Highlight top candidates (Optional - Best ones mela varum)
        if 'Experience_Years' in filtered_df.columns:
            filtered_df = filtered_df.sort_values(by='Experience_Years', ascending=False)

        st.dataframe(filtered_df, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}. File columns names (Name, Skills, Experience_Years) correct-ah irukanu check pannunga.")

else:
    st.info("Mela irukura button-ah click panni candidate data-voda Excel file-ah upload pannunga.")
    st.image("https://img.icons8.com/clouds/200/upload.png") # Oru chinna icon for look
