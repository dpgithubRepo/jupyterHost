import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load and preprocess data
df = pd.read_csv("all_zen 5.csv")
df['Requested'] = pd.to_datetime(df['Requested'])
df.set_index('Requested', inplace=True)

# Categorize issues
def categorize_issue(subject):
    subject = subject.lower()
    if 'level' in subject:
        return 'Level'
    elif 'avail' in subject:
        return 'Availability'
    elif 'platform' in subject:
        return 'Platform'
    else:
        return 'Other'

df['Category'] = df['Subject'].apply(categorize_issue)

# Streamlit app
st.title("Ticket Analysis Dashboard")

# Dropdown menu for selecting a graph
graph = st.selectbox("Select a graph to display:", [
    "Ticket Volume Over Time",
    "Top 15 Most Frequently Repeated Issues",
    "Issue Categories Distribution",
    "Ticket Resolution by Assignee",
    "Heatmap of Ticket Volume",
    "Word Cloud of Issue Subjects",
    "Ticket Volume by Weekday and Hour",
    "Requester-Assignee Interaction Frequency",
    "Issue Lifecycle Stages",
    "Escalation Patterns by Assignee"
])

# Display the selected graph
if graph == "Ticket Volume Over Time":
    st.subheader("Ticket Volume Over Time")
    df['ID'].resample('D').count().plot(title='Ticket Volume Over Time', figsize=(12, 6))
    st.pyplot(plt)
    plt.close()

elif graph == "Top 15 Most Frequently Re
