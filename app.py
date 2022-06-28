import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title="Survey Results")
st.header("Survey Results 2021")
st.subheader("This Survey Result Analysis consists of Age, Department, Rating and others")

### -- Load DATAFRAME 

excel_file = "Survey_Results.xlsx"
sheet_name = "DATA"

df = pd.read_excel(excel_file, sheet_name=sheet_name, usecols="B:D", header=3)

df_participants = pd.read_excel(excel_file, sheet_name=sheet_name, usecols="F:G", header=3)

df_participants.dropna(inplace=True)

# ---- STREAMLIT SELECTION

department = df["Department"].unique().tolist()

ages = df["Age"].unique().tolist()


age_selection = st.slider("Age: ", min_value=min(ages), max_value=max(ages), value=(min(ages), max(ages)))


department_selection = st.multiselect("Department: ", department, default=department)


# ---- FILTER DATAFRAME BASED ON USER SELECTION

mask = (df["Age"].between(*age_selection)) & (df["Department"].isin(department_selection))

number_of_result = df[mask].shape[0]

st.markdown(f"Available Results {number_of_result}")


# --- GROUP DATAFRAME AFTER SELECTION

df_grouped = df[mask].groupby(by=["Rating"]).count()[["Age"]]

df_grouped = df_grouped.rename(columns={"Age" : "Votes"})

df_grouped = df_grouped.reset_index()


# --- PLOT BAR CHART
bar_chart = px.bar(df_grouped,x ="Rating", y="Votes", text="Votes", color_discrete_sequence=["#F63366"] * len(df_grouped), template="plotly_white")

st.plotly_chart(bar_chart)

# --- DISPLAY IMAGE & DATAFRAME

col1, col2 = st.columns(2)


image = Image.open("images/survey.jpg")

col1.image(image, caption="Analysis by Davis", use_column_width=True)

col2.dataframe(df[mask])

st.dataframe(df_participants)


#PLot PIE CHART
pie_chart = px.pie(df_participants, title="Total No. of Participants", values="Participants", names="Departments")

st.plotly_chart(pie_chart)


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

