
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from wordcloud import WordCloud
import streamlit as st

# Load and preprocess data
df = pd.read_csv("all_zen.csv")
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

# Ticket Volume Over Time
st.subheader("Ticket Volume Over Time")
ticket_volume_fig, ax = plt.subplots(figsize=(12, 6))
df['ID'].resample('D').count().plot(title='Ticket Volume Over Time', ax=ax)
st.pyplot(ticket_volume_fig)

# Top 15 Most Frequently Repeated Issues
st.subheader("Top 15 Most Frequently Repeated Issues")
top_15 = df['Subject'].value_counts().head(15)
top_15_fig, ax = plt.subplots(figsize=(12, 6))
top_15.plot(kind='bar', title='Top 15 Most Frequently Repeated Issues', ax=ax)
st.pyplot(top_15_fig)

# Issue Categories Distribution
st.subheader("Issue Categories Distribution")
category_counts = df['Category'].value_counts()
category_counts_fig, ax = plt.subplots(figsize=(12, 6))
category_counts.plot(kind='pie', autopct='%1.1f%%', title='Issue Categories Distribution', ax=ax)
plt.ylabel('')
st.pyplot(category_counts_fig)

# Ticket Resolution by Assignee
st.subheader("Ticket Resolution by Assignee")
ticket_resolution_fig, ax = plt.subplots(figsize=(12, 6))
df['Assignee'].value_counts().plot(kind='bar', title='Ticket Resolution by Assignee', ax=ax)
st.pyplot(ticket_resolution_fig)

# Heatmap of Ticket Volume by Day and Hour
st.subheader("Heatmap of Ticket Volume by Day and Hour")
df['DayOfWeek'] = df.index.dayofweek
df['Hour'] = df.index.hour
heatmap_data = df.groupby(['DayOfWeek', 'Hour']).size().unstack()
heatmap_fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='.0f', ax=ax)
st.pyplot(heatmap_fig)

# Word Cloud of Issue Subjects
st.subheader("Word Cloud of Issue Subjects")
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df['Subject']))
wordcloud_fig, ax = plt.subplots(figsize=(12, 6))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(wordcloud_fig)

# Advanced Insights
st.subheader("Advanced Insights")

# Ticket Volume by Weekday and Hour
st.subheader("Ticket Volume by Weekday and Hour")
weekday_hour_heatmap_data = df.groupby(['DayOfWeek', 'Hour']).size().unstack()
weekday_hour_heatmap_fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(weekday_hour_heatmap_data, cmap='YlGnBu', annot=True, fmt='.0f', ax=ax)
st.pyplot(weekday_hour_heatmap_fig)

# Escalation Patterns by Assignee
df['Escalated'] = df['Status'].apply(lambda x: 'Escalated' if 'Escalated' in x else 'Not Escalated')
escalation_by_assignee = df[df['Escalated'] == 'Escalated']['Assignee'].value_counts()
if not escalation_by_assignee.empty:
    st.subheader("Escalation Patterns by Assignee")
    escalation_by_assignee_fig, ax = plt.subplots(figsize=(12, 6))
    escalation_by_assignee.plot(kind='bar', title='Escalation Patterns by Assignee', ax=ax)
    st.pyplot(escalation_by_assignee_fig)

# Requester-Assignee Interaction Frequency
st.subheader("Requester-Assignee Interaction Frequency")
interaction_matrix = pd.crosstab(df['Requester'], df['Assignee'])
interaction_matrix_fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(interaction_matrix, cmap='YlGnBu', annot=True, fmt='.0f', ax=ax)
st.pyplot(interaction_matrix_fig)

# Issue Lifecycle Stages
st.subheader("Issue Lifecycle Stages")
status_counts = df['Status'].value_counts()
status_counts_fig, ax = plt.subplots(figsize=(12, 6))
status_counts.plot(kind='bar', title='Issue Lifecycle Stages', ax=ax)
st.pyplot(status_counts_fig)
