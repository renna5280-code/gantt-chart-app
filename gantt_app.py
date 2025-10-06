import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Gantt Chart Project Manager", layout="wide")

# Title of the app
st.title("📊 Gantt Chart Project Management Tool")

# Initialize session state to store tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Sidebar form to add a new task
with st.sidebar.form("task_form"):
    st.header("➕ Add New Task")
    task_name = st.text_input("Task Name")
    team_member = st.text_input("Assigned To")
    start_date = st.date_input("Start Date", value=datetime.today())
    end_date = st.date_input("End Date", value=datetime.today())
    submitted = st.form_submit_button("Add Task")

    # Add task to session state
    if submitted:
        if task_name and team_member and start_date and end_date:
            st.session_state.tasks.append({
                "Task": task_name,
                "Team Member": team_member,
                "Start": pd.to_datetime(start_date),
                "Finish": pd.to_datetime(end_date)
            })
        else:
            st.warning("Please fill in all fields.")

# Display current tasks
st.subheader("📋 Current Tasks")
if st.session_state.tasks:
    tasks_df = pd.DataFrame(st.session_state.tasks)
    st.dataframe(tasks_df)

    # Generate Gantt chart
    fig = px.timeline(
        tasks_df,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color="Team Member",
        title="📅 Project Timeline - Gantt Chart"
    )
    fig.update_yaxes(autorange="reversed")  # Show tasks from top to bottom
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No tasks added yet. Use the form in the sidebar to add tasks.")
