
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

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

# Add DayOfWeek and Hour columns for heatmaps
df['DayOfWeek'] = df.index.dayofweek
df['Hour'] = df.index.hour

# Streamlit app
st.title("Zendesk Ticket Analytics & Dashboard")

# Date range picker
start_date = st.date_input("Start date", df.index.min().date())
end_date = st.date_input("End date", df.index.max().date())
mask = (df.index.date >= start_date) & (df.index.date <= end_date)
filtered_df = df.loc[mask]

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
    "Escalation Patterns by Assignee",
    "Show All Graphs and Tables"
])

# Function to display graphs and tables
def display_graph_and_table(graph, filtered_df):
    if graph == "Ticket Volume Over Time":
        st.subheader("Ticket Volume Over Time")
        filtered_df['ID'].resample('D').count().plot(figsize=(12, 6))
        plt.title('Ticket Volume Over Time')
        st.pyplot(plt)
        plt.close()
        st.dataframe(filtered_df[['ID']].resample('D').count().rename(columns={'ID': 'Count'}))

    elif graph == "Top 15 Most Frequently Repeated Issues":
        st.subheader("Top 15 Most Frequently Repeated Issues")
        top_15 = filtered_df['Subject'].value_counts().head(15)
        top_15.plot(kind='bar', figsize=(12, 6))
        plt.title('Top 15 Most Frequently Repeated Issues')
        st.pyplot(plt)
        plt.close()
        st.dataframe(filtered_df[filtered_df['Subject'].isin(top_15.index)].groupby('Subject').size().reset_index(name='Count'))

    elif graph == "Issue Categories Distribution":
        st.subheader("Issue Categories Distribution")
        category_counts = filtered_df['Category'].value_counts()
        category_counts.plot(kind='pie', autopct='%1.1f%%')
        plt.title('Issue Categories Distribution')
        plt.ylabel('')
        st.pyplot(plt)
        plt.close()
        st.dataframe(filtered_df.groupby('Category').size().reset_index(name='Count'))

    elif graph == "Ticket Resolution by Assignee":
        st.subheader("Ticket Resolution by Assignee")
        filtered_df['Assignee'].value_counts().plot(kind='bar', figsize=(12, 6))
        plt.title('Ticket Resolution by Assignee')
        st.pyplot(plt)
        plt.close()
        st.dataframe(filtered_df.groupby('Assignee').size().reset_index(name='Count'))

    elif graph == "Heatmap of Ticket Volume":
        st.subheader("Heatmap of Ticket Volume")
        heatmap_data = filtered_df.groupby(['DayOfWeek', 'Hour']).size().unstack()
        sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='.0f')
        plt.title('Heatmap of Ticket Volume')
        st.pyplot(plt)
        plt.close()
        st.dataframe(filtered_df.groupby(['DayOfWeek', 'Hour']).size().reset_index(name='Count'))

    elif graph == "Word Cloud of Issue Subjects":
        st.subheader("Word Cloud of Issue Subjects")
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(filtered_df['Subject']))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)
        plt.close()
        st.dataframe(filtered_df.groupby('Subject').size().reset_index(name='Count'))

    elif graph == "Ticket Volume by Weekday and Hour":
        st.subheader("Ticket Volume by Weekday and Hour")
        weekday_hour_heatmap_data = filtered_df.groupby(['DayOfWeek', 'Hour']).size().unstack()
        sns.heatmap(weekday_hour_heatmap_data, cmap='YlGnBu', annot=True, fmt='.0f')
        plt.title('Ticket Volume by Weekday and Hour')
        st.pyplot(plt)
        plt.close()
        st.dataframe(filtered_df.groupby(['DayOfWeek', 'Hour']).size().reset_index(name='Count'))

    elif graph == "Requester-Assignee Interaction Frequency":
        st.subheader("Requester-Assignee Interaction Frequency")
        interaction_matrix = pd.crosstab(filtered_df['Requester'], filtered_df['Assignee'])
        sns.heatmap(interaction_matrix, cmap='YlGnBu', annot=True, fmt='.0f')
        plt.title('Requester-Assignee Interaction Frequency')
        st.pyplot(plt)
        plt.close()
        st.dataframe(filtered_df.groupby(['Requester', 'Assignee']).size().reset_index(name='Count'))

    elif graph == "Issue Lifecycle Stages":
        st.subheader("Issue Lifecycle Stages")
        status_counts = filtered_df['Status'].value_counts()
        status_counts.plot(kind='bar', figsize=(12, 6))
        plt.title('Issue Lifecycle Stages')
        st.pyplot(plt)
        plt.close()
        st.dataframe(filtered_df.groupby('Status').size().reset_index(name='Count'))

    elif graph == "Escalation Patterns by Assignee":
        st.subheader("Escalation Patterns by Assignee")
        filtered_df['Escalated'] = filtered_df['Status'].apply(lambda x: 'Escalated' if 'Escalated' in x else 'Not Escalated')
        escalation_by_assignee = filtered_df[filtered_df['Escalated'] == 'Escalated']['Assignee'].value_counts()
        if not escalation_by_assignee.empty:
            escalation_by_assignee.plot(kind='bar', figsize=(12, 6))
            plt.title('Escalation Patterns by Assignee')
            st.pyplot(plt)
            plt.close()
            st.dataframe(filtered_df[filtered_df['Escalated'] == 'Escalated'].groupby('Assignee').size().reset_index(name='Count'))

# Display selected graph and table
if graph == "Show All Graphs and Tables":
    for g in [
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
    ]:
        display_graph_and_table(g, filtered_df)
else:
    display_graph_and_table(graph, filtered_df)
