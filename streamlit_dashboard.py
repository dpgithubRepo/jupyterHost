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

elif graph == "Top 15 Most Frequently Repeated Issues":
    st.subheader("Top 15 Most Frequently Repeated Issues")
    top_15 = df['Subject'].value_counts().head(15)
    top_15.plot(kind='bar', figsize=(12, 6), title='Top 15 Most Frequently Repeated Issues')
    st.pyplot(plt)
    plt.close()

elif graph == "Issue Categories Distribution":
    st.subheader("Issue Categories Distribution")
    category_counts = df['Category'].value_counts()
    category_counts.plot(kind='pie', autopct='%1.1f%%', title='Issue Categories Distribution')
    plt.ylabel('')
    st.pyplot(plt)
    plt.close()

elif graph == "Ticket Resolution by Assignee":
    st.subheader("Ticket Resolution by Assignee")
    df['Assignee'].value_counts().plot(kind='bar', figsize=(12, 6), title='Ticket Resolution by Assignee')
    st.pyplot(plt)
    plt.close()

elif graph == "Heatmap of Ticket Volume":
    st.subheader("Heatmap of Ticket Volume")
    df['DayOfWeek'] = df.index.dayofweek
    df['Hour'] = df.index.hour
    heatmap_data = df.groupby(['DayOfWeek', 'Hour']).size().unstack()
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='.0f')
    st.pyplot(plt)
    plt.close()

elif graph == "Word Cloud of Issue Subjects":
    st.subheader("Word Cloud of Issue Subjects")
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df['Subject']))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)
    plt.close()

elif graph == "Ticket Volume by Weekday and Hour":
    st.subheader("Ticket Volume by Weekday and Hour")
    weekday_hour_heatmap_data = df.groupby(['DayOfWeek', 'Hour']).size().unstack()
    sns.heatmap(weekday_hour_heatmap_data, cmap='YlGnBu', annot=True, fmt='.0f')
    st.pyplot(plt)
    plt.close()

elif graph == "Requester-Assignee Interaction Frequency":
    st.subheader("Requester-Assignee Interaction Frequency")
    interaction_matrix = pd.crosstab(df['Requester'], df['Assignee'])
    sns.heatmap(interaction_matrix, cmap='YlGnBu', annot=True, fmt='.0f')
    st.pyplot(plt)
    plt.close()

elif graph == "Issue Lifecycle Stages":
    st.subheader("Issue Lifecycle Stages")
    status_counts = df['Status'].value_counts()
    status_counts.plot(kind='bar', figsize=(12, 6), title='Issue Lifecycle Stages')
    st.pyplot(plt)
    plt.close()

elif graph == "Escalation Patterns by Assignee":
    st.subheader("Escalation Patterns by Assignee")
    df['Escalated'] = df['Status'].apply(lambda x: 'Escalated' if 'Escalated' in x else 'Not Escalated')
    escalation_by_assignee = df[df['Escalated'] == 'Escalated']['Assignee'].value_counts()
    if not escalation_by_assignee.empty:
        escalation_by_assignee.plot(kind='bar', figsize=(12, 6), title='Escalation Patterns by Assignee')
        st.pyplot(plt)
        plt.close()
