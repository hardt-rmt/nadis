import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime, timedelta
import inference
import alerts


disaster_tweets = inference.getDisasterTweets()
disaster_locations = inference.getDisasterLocations()
disaster_coordinates = inference.getDisasterCoordinates()
tweets_sentiment = inference.getSentiment()
tweets_severity = inference.detectSeverity()

# Get data for visualization
def getVisualData():    
    data = []
    for _ in range(disaster_locations):
        data.append({
            'Tweet': disaster_tweets,
            'Location': disaster_locations,
            'Severity': tweets_severity,
            'Coordinates': disaster_coordinates,
            'Sentiment': tweets_sentiment
        })
    return pd.DataFrame(data)

# Page configuration
st.set_page_config(page_title="Disaster Detection Dashboard", layout="wide")

# Dashboard Title
st.title("Real-Time Natural Disaster Detection Dashboard")

# Sidebar for filtering
st.sidebar.header("Filter Data")
selected_severity = st.sidebar.multiselect("Select Disaster Type", tweets_severity)

# Load or generate sample data
df = getVisualData()

# Filter data based on user selection
if selected_severity:
    df = df[df['Severity'].isin(selected_severity)]

# Visualization 1: Disaster Type Distribution
st.subheader("Disaster Type Distribution")
fig1 = px.pie(df, names='Severity', title='Distribution of Disaster Types')
st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: Geographic Distribution (Mock Example)
st.subheader("Geographic Distribution")
location_counts = df['Location'].value_counts().reset_index()
location_counts.columns = ['Location', 'Count']
fig3 = px.bar(location_counts, x='Location', y='Count', color='Location',
              title='Number of Events by Location')
st.plotly_chart(fig3, use_container_width=True)

# Alert Section
st.subheader("Alert Notifications")
latest_event = df.iloc[0]
st.warning(f"Latest Alert: {latest_event['Severity']} detected in {latest_event['Location']} "
           f"with severity '{latest_event['Severity']}'")

alerts.send_sms_alert('+1234567890', 'Alert: A severe earthquake has been detected in ' + latest_event['Location'] + '!')
alerts.send_email_alert('recipient@example.com', 'Disaster Alert', 'Alert: A severe flood has been detected in ' + latest_event['Location'] + '!')

# Footer
st.write("---")
st.write("Real-time monitoring of natural disasters from social media posts.")
