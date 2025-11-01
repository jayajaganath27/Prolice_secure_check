import pandas as pd
import streamlit as st
import pymysql
from datetime import datetime
import plotly.express as px


# 🧩 DATABASE CONNECTION
def create_connection():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Dhruv@2212',
            database='securecheck',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as error:
        st.error(f"Database connection error: {error}")
        return None
    
# 📥 FETCH DATA FUNCTION
def fetch_data(query):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                df = pd.DataFrame.from_records(result)
                return df
        finally:
            connection.close()
    else:
        return pd.DataFrame()


# 🔧 PAGE CONFIGURATION IN STREAMLIT 
st.set_page_config(
    page_title="Securecheck_Police_Dashboard",
    page_icon="🚓",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 🧾 DASHBOARD TITLE
st.markdown("<h1 style='text-align:center; color:#FF4B4B;'>🚨 SecureCheck: Police Checkpost Digital Ledger</h1>", unsafe_allow_html=True)
st.header("Police Logs Overview")

# 📊 FETCH DATA EXAMPLE
query = "SELECT * FROM police_log"
df = fetch_data(query)

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data found in 'securecheck.police_log' table")

# Quick metrices
st.header("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4) 

with col1:
     total_stops = df.shape[0]
     st.metric("Total Police Stops",total_stops)

with col2:
     arrests = df[df["stop_outcome"].str.contains("arrest",case=False,na=False)].shape[0]
     st.metric("Total Arrests", arrests)

with col3:
     warnings = df[df["stop_outcome"].str.contains("warning",case=False,na=False)].shape[0]
     st.metric("Total_warnings",warnings)

with col4:
     drug_related = df[df["drugs_related_stop"] == 1].shape[0]
     st.metric("drugs_related_stop",drug_related)


st.markdown("---")
# Medium level queries
st.header("🧠 Medium Level Insights")

select_query = st.selectbox("select a query to run",[
    "What are the top 10 vehicle_Number involved in drug-related stops?",
    "Which vehicles were most frequently searched?",
    "Which driver age group had the highest arrest rate?",
    "What is the gender distribution of drivers stopped in each country?",
    "Which race and gender combination has the highest search rate?",
    "What time of day sees the most traffic stops?",
    "What is the average stop duration for different violations?",
    "Are stops during the night more likely to lead to arrests?",
    "Which violations are most associated with searches or arrests?",
    "Which violations are most common among younger drivers (<25)?",
    "Is there a violation that rarely results in search or arrest?",
    "Which countries report the highest rate of drug-related stops?",
    "What is the arrest rate by country and violation?",
    "Which country has the most stops with search conducted?"
])

# 🧩 SQL queries mapped to selections
query_map =  {
     "What are the top 10 vehicle_Number involved in drug-related stops?" :
        "SELECT vehicle_number, COUNT(*) AS drug_stop_count FROM police_log WHERE drugs_related_stop=1 GROUP BY vehicle_number ORDER BY drug_stop_count DESC LIMIT 10",
   
     "Which vehicles were most frequently searched?" :
        "SELECT vehicle_number, COUNT(*) AS search_count FROM police_log WHERE search_conducted = 1 GROUP BY vehicle_number ORDER BY search_count DESC LIMIT 10",
   
    "Which driver age group had the highest arrest rate?": 
        "SELECT driver_age, ROUND(SUM(CASE WHEN stop_outcome LIKE '%arrest%' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS arrest_rate FROM police_log GROUP BY driver_age ORDER BY arrest_rate DESC;",
    
    "What is the gender distribution of drivers stopped in each country?": 
        "SELECT country_name, driver_gender, COUNT(*) AS total_stops FROM police_log GROUP BY country_name, driver_gender;",
    
    "Which race and gender combination has the highest search rate?": 
        "SELECT driver_race, driver_gender, ROUND(SUM(CASE WHEN search_conducted = 1 THEN 1 ELSE 0 END)/COUNT(*)*100,2) AS search_rate FROM police_log GROUP BY driver_race, driver_gender ORDER BY search_rate DESC;",

    "What time of day sees the most traffic stops?": 
        "SELECT HOUR(stop_time) AS hour_of_day, COUNT(*) AS total_stops FROM police_log GROUP BY hour_of_day ORDER BY total_stops DESC;",
  
    "What is the average stop duration for different violations?": 
        "SELECT violation, ROUND(AVG(stop_duration), 2) AS avg_stop_duration FROM police_log GROUP BY violation ORDER BY avg_stop_duration DESC;",

    "Are stops during the night more likely to lead to arrests?":
        "SELECT  CASE WHEN HOUR(stop_time) BETWEEN 20 AND 23 OR HOUR(stop_time) BETWEEN 0 AND 5 THEN 'Night' ELSE 'Day' END AS time_period, ROUND(SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS arrest_rate FROM police_log GROUP BY time_period;",
            
    "Which violations are most associated with searches or arrests?": 
        "SELECT violation, SUM(CASE WHEN search_conducted='1' THEN 1 ELSE 0 END) AS total_searches, SUM(CASE WHEN is_arrested=1 THEN 1 ELSE 0 END) AS total_arrests FROM police_log GROUP BY violation ORDER BY total_searches+total_arrests DESC LIMIT 5;",
    
    "Which violations are most common among younger drivers (<25)?": 
        "SELECT violation, COUNT(*) AS total_stops FROM police_log WHERE driver_age < 25 GROUP BY violation ORDER BY total_stops DESC;",

    "Is there a violation that rarely results in search or arrest?":
        "SELECT violation, ROUND(SUM(CASE WHEN search_conducted='1' THEN 1 ELSE 0 END)*100.0/COUNT(*),2) AS search_rate, ROUND(SUM(CASE WHEN is_arrested=1 THEN 1 ELSE 0 END)*100.0/COUNT(*),2) AS arrest_rate FROM police_log GROUP BY violation HAVING search_rate<1 AND arrest_rate<1;",
    
    "Which countries report the highest rate of drug-related stops?":
        "SELECT  country_name, ROUND(SUM(CASE WHEN drugs_related_stop = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS drug_stop_rate FROM police_log GROUP BY country_name ORDER BY drug_stop_rate DESC LIMIT 5;",
        
    "What is the arrest rate by country and violation?":
        "SELECT country_name, violation, ROUND(SUM(CASE WHEN stop_outcome LIKE '%arrest%' THEN 1 ELSE 0 END)/COUNT(*)*100,2) AS arrest_rate FROM police_log GROUP BY country_name, violation ORDER BY arrest_rate DESC;",

    "Which country has the most stops with search conducted?": 
        "SELECT country_name, COUNT(*) AS total_searches FROM police_log WHERE search_conducted = 1 GROUP BY country_name ORDER BY total_searches DESC;",
    }

# 🧩 Run the selected query

if st.button("Run Query"):
    result = fetch_data(query_map[select_query])
    if not result.empty:
        st.success(f"✅ Results for: {select_query}")
        st.dataframe(result, use_container_width=True)
    else:
        st.warning("⚠️ No results found for the selected query.")

st.markdown("---")
# complex level queries
st.header("🧠 Complex Level Insights")

select_query = st.selectbox("select a query to run",[
    "Yearly Breakdown of Stops and Arrests by Country",
    "Driver Violation Trends Based on Age and Race",
    "Time Period Analysis of Stops (Joining with Date Functions), Number of Stops by Year,Month, Hour of the Day",
    "Violations with High Search and Arrest Rates",
    "Driver Demographics by Country (Age, Gender, and Race)",
    "Top 5 Violations with Highest Arrest Rates"
])

query_map =  {
    "Yearly Breakdown of Stops and Arrests by Country": #(Using Subquery and Window Functions)
        "SELECT  country_name,  year,  total_stops,  total_arrests, ROUND((total_arrests * 100.0 / total_stops), 2) AS arrest_rate,  RANK() OVER (PARTITION BY year ORDER BY total_arrests DESC) AS rank_by_arrests FROM (SELECT country_name, YEAR(stop_date) AS year, COUNT(*) AS total_stops, SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) AS total_arrests FROM police_log GROUP BY country_name, YEAR(stop_date)) AS yearly_summary ORDER BY year DESC, total_arrests DESC;",
    
    "Driver Violation Trends Based on Age and Race": #(Join with Subquery)
        "SELECT driver_age, driver_race, COUNT(*) AS total_violations FROM police_log WHERE violation IS NOT NULL GROUP BY driver_age, driver_race ORDER BY total_violations DESC;",

    "Time Period Analysis of Stops (Joining with Date Functions), Number of Stops by Year,Month, Hour of the Day":
        "SELECT YEAR(stop_date) AS year, MONTH(stop_date) AS month, HOUR(stop_time) AS hour, COUNT(*) AS total_stops FROM police_log GROUP BY year, month, hour ORDER BY year, month, hour;",

    "Violations with High Search and Arrest Rates": # (Window Function)
        "SELECT violation, ROUND(SUM(CASE WHEN search_conducted = 1 THEN 1 ELSE 0 END)/COUNT(*)*100,2) AS search_rate, ROUND(SUM(CASE WHEN stop_outcome LIKE '%arrest%' THEN 1 ELSE 0 END)/COUNT(*)*100,2) AS arrest_rate, RANK() OVER (ORDER BY SUM(CASE WHEN search_conducted = 1 THEN 1 ELSE 0 END) DESC) AS search_rank FROM police_log GROUP BY violation ORDER BY search_rate DESC, arrest_rate DESC;",

    "Driver Demographics by Country (Age, Gender, and Race)": 
        "SELECT country_name, driver_gender, driver_race, ROUND(AVG(driver_age),2) AS avg_age, COUNT(*) AS total_stops FROM police_log GROUP BY country_name, driver_gender, driver_race ORDER BY country_name, total_stops DESC;",

    "Top 5 Violations with Highest Arrest Rates":
        "SELECT violation, ROUND(SUM(CASE WHEN stop_outcome LIKE '%arrest%' THEN 1 ELSE 0 END)/COUNT(*)*100,2) AS arrest_rate, COUNT(*) AS total_stops FROM police_log GROUP BY violation ORDER BY arrest_rate DESC LIMIT 5;"
}

if st.button("Run Complex Query"):
    result = fetch_data(query_map[select_query])
    if not result.empty:
        st.success(f"✅ Results for: {select_query}")
        st.dataframe(result, use_container_width=True)
    else:
        st.warning("⚠️ No results found for the selected query.")

st.markdown("---")

st.header("🚔 Add a New Police Log & Predict Outcome and Violation")

with st.form("new_log_form"):
    stop_date = st.date_input("stop date")
    stop_time = st.time_input("Stop Time")
    country_name = st.text_input("Country Name")
    driver_gender = st.selectbox("Driver Gender", ["Male", "Female"])
    driver_age = st.number_input("Driver Age", min_value=16, max_value=100, value=27)
    driver_race = st.text_input("Driver Race")
    violation = st.text_input("Violation Description")
    search_conducted = st.selectbox("Was a search conducted?", ["1", "0"])
    search_type = st.text_input("search type")
    drugs_related_stop = st.selectbox("Was it Drugs Related Stop?", ["1", "0"])
    stop_duration = st.number_input("Stop Duration (in minutes)", min_value=0.0, step=0.1)
    vehicle_number = st.text_input("vehicle number")
    timestamp = pd.Timestamp.now()

    submitted = st.form_submit_button("Predict Stop Outcome and Violation")


    if submitted:
        filtered_data = df[
            (df["driver_gender"]==driver_gender) &
            (df["driver_age"]==driver_age) &
            (df["search_conducted"]==int(search_conducted)) &
            (df["stop_duration"]==stop_duration) &
            (df["drugs_related_stop"]==int(drugs_related_stop))
        ]

        if not filtered_data.empty:
            predicted_outcome = filtered_data["stop_outcome"].mode()[0]
            predicted_violation = filtered_data["violation"].mode()[0]
        else:
            predicted_outcome = "Warning"
            predicted_violation = "Speeding"


        search_text = "A search was conducted" if int(search_conducted) else "No search was conducted"
        drug_text = "was drug related" if int(drugs_related_stop) else "was not drug related"

st.markdown(f"""
**prediction summary**
            
- **predicted violation:** {predicted_violation}
- **predicted stop outcome:** {predicted_outcome}

A {driver_age} year old{driver_gender} driver in {country_name} was stopped at{stop_time}. 
{search_text}, and the stop {drug_text}. 
stop duration: {stop_duration}
vehicle number: {vehicle_number}
""")

import streamlit as st
import base64

# Function to set background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
