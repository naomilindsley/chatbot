import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page configuration
st.set_page_config(
    page_title="Airline Passenger Satisfaction Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load the dataset
@st.cache_data
def load_data():
    data = pd.read_csv('airline_satisfaction.csv')
    return data

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")
customer_type = st.sidebar.multiselect(
    "Customer Type",
    options=df["Customer Type"].unique(),
    default=df["Customer Type"].unique()
)
travel_class = st.sidebar.multiselect(
    "Class",
    options=df["Class"].unique(),
    default=df["Class"].unique()
)
age_range = st.sidebar.slider(
    "Age Range",
    int(df["Age"].min()),
    int(df["Age"].max()),
    (int(df["Age"].min()), int(df["Age"].max()))
)

# Apply filters
filtered_df = df[
    (df["Customer Type"].isin(customer_type)) &
    (df["Class"].isin(travel_class)) &
    (df["Age"] >= age_range[0]) &
    (df["Age"] <= age_range[1])
]

# Main dashboard
st.title("Airline Passenger Satisfaction Analysis")

# Display filtered data
st.subheader("Filtered Data")
st.write(f"Total Records: {filtered_df.shape[0]}")
st.dataframe(filtered_df)

# Satisfaction distribution
st.subheader("Satisfaction Distribution")
fig, ax = plt.subplots()
sns.countplot(data=filtered_df, x="satisfaction", palette="viridis", ax=ax)
st.pyplot(fig)

# Satisfaction by Travel Class
st.subheader("Satisfaction by Travel Class")
fig, ax = plt.subplots()
sns.countplot(data=filtered_df, x="Class", hue="satisfaction", palette="viridis", ax=ax)
st.pyplot(fig)

# Age Distribution
st.subheader("Age Distribution")
fig, ax = plt.subplots()
sns.histplot(filtered_df["Age"], bins=30, kde=True, color="skyblue", ax=ax)
st.pyplot(fig)

# Correlation Heatmap
st.subheader("Correlation Heatmap")
corr = filtered_df.corr()
fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
st.pyplot(fig)
