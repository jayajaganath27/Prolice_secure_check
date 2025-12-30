🚓 SecureCheck – Police Checkpost Digital Ledger
📌 Project Overview
SecureCheck is a data analytics and visualization project that digitizes police checkpost records and provides actionable insights through an interactive dashboard.The project analyzes traffic stop data to understand patterns related to searches, arrests, violations, driver demographics, time-based trends, and drug-related stops.
It integrates Python, MySQL, SQL analytics, and Streamlit to build an end-to-end data pipeline and dashboard.

🎯 Objectives
Digitize police checkpost records using a structured database
Analyze traffic stop patterns across time, location, and driver demographics
Identify high-risk violations and drug-related stops
Provide interactive insights using SQL queries
Predict likely stop outcomes and violations based on historical data

🛠️ Technologies Used
Python
Pandas – Data cleaning & preprocessing
MySQL – Database storage
SQL (Advanced Queries) – Analytics & insights
Streamlit – Interactive dashboard
Plotly Express – Visualizations
PyMySQL / MySQL Connector – Database connectivity

🔄 Project Workflow
1.Load CSV data using Pandas
2.Clean and preprocess data (handle nulls, data types, duplicates)
3.Convert date & time fields to proper formats
4.Create MySQL database and table
5.Insert cleaned data into MySQL
6.Run SQL queries for insights (basic, medium, complex)
7.Build Streamlit dashboard for:
  1-Data viewing
  2-Metrics
  3-Query-based insights
  4-Prediction of stop outcome & violation

📈 Key Features
📊 Dashboard Highlights
-> Total police stops, arrests, warnings, drug-related stops
-> Interactive SQL-based insights (Medium & Complex level)
-> Time-based analysis (day vs night, hourly trends)
-> Demographic analysis (age, gender, race)
-> Country-wise and violation-wise arrest rates
🧠 SQL Insights
-> Top vehicles involved in drug-related stops
-> Most frequently searched vehicles
-> Arrest rates by age group
-> Search rate by race & gender
-> Night vs day arrest comparison
-> Violations with high search/arrest probability
-> Countries with highest drug-related stops

🖥️ Streamlit Dashboard
Dashboard Sections:
~ Police Logs Overview (raw data)
~ Key Metrics (KPIs)
~ Medium-Level SQL Insights
~ Complex-Level SQL Insights
~ New Log Egntry & Prediction
