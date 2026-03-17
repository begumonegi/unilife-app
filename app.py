import streamlit as st
import datetime
from database import create_table, add_task, get_tasks, update_task_status, delete_task

# -------------------------
# Page config
# -------------------------
st.set_page_config(
    page_title="UniLife App",
    page_icon="🎓",
    layout="centered"
)

# -------------------------
# Database init
# -------------------------
create_table()

# -------------------------
# Custom CSS
# -------------------------
st.markdown("""
<style>
    .block-container {
        max-width: 860px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .main-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .sub-title {
        text-align: center;
        color: #9aa0a6;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    .section-title {
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .metric-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 16px;
        padding: 1.2rem 1rem;
        text-align: center;
    }

    .metric-number {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .metric-label {
        color: #b0b0b0;
        font-size: 0.95rem;
    }

    .task-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 0.9rem;
    }

    .meta-text {
        color: #b0b0b0;
        font-size: 0.92rem;
        margin-top: 0.2rem;
    }

    div.stButton > button {
        border-radius: 12px;
        font-weight: 600;
        height: 44px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Helper functions
# -------------------------
def category_icon(category):
    icons = {
        "Study": "📚",
        "Exam": "📝",
        "Project": "💻",
        "Personal": "🌿"
    }
    return icons.get(category, "📌")


def priority_badge(priority):
    badges = {
        "High": "🔴 High",
        "Medium": "🟠 Medium",
        "Low": "🟢 Low"
    }
    return badges.get(priority, "⚪ Unknown")


# -------------------------
# Header
# -------------------------
st.markdown('<div class="main-title">🎓 UniLife</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Professional student productivity dashboard</div>', unsafe_allow_html=True)

# -------------------------
# Add new task
# -------------------------
st.markdown('<div class="section-title">➕ Add New Task</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    task_name = st.text_input("Task Name", placeholder="Enter your task name")

with col2:
    deadline = st.date_input(
        "Deadline",
        min_value=datetime.date.today()
    )

col3, col4 = st.columns(2)

with col3:
    category = st.selectbox(
        "Category",
        ["Study", "Exam", "Project", "Personal"]
    )

with col4:
    priority = st.selectbox(
        "Priority",
        ["High", "Medium", "Low"]
    )

if st.button("Add Task", use_container_width=True):
    if task_name.strip():
        add_task(
            task_name.strip(),
            str(deadline),
            category,
            priority
        )
        st.success("Task added successfully.")
        st.rerun()
    else:
        st.warning("Please enter a task name.")

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------
# Search, filter, sort
# -------------------------
st.markdown('<div class="section-title">🔎 Search & Filter</div>', unsafe_allow_html=True)

search = st.text_input("Search task", placeholder="Search by task name...")

f1, f2, f3 = st.columns(3)

with f1:
    filter_category = st.selectbox(
        "Filter by Category",
        ["All", "Study", "Exam", "Project", "Personal"]
    )

with f2:
    filter_priority = st.selectbox(
        "Filter by Priority",
        ["All", "High", "Medium", "Low"]
    )

with f3:
    sort_option = st.selectbox(
        "Sort by",
        ["Nearest Deadline", "Furthest Deadline"]
    )

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------
# Load and filter tasks
# -------------------------
tasks = get_tasks()

filtered_tasks = []

for task in tasks:
    task_id, name, task_deadline, task_category, task_priority, task_completed = task

    if search.strip() and search.lower() not in name.lower():
        continue

    if filter_category != "All" and task_category != filter_category:
        continue

    if filter_priority != "All" and task_priority != filter_priority:
        continue

    filtered_tasks.append(task)

if sort_option == "Nearest Deadline":
    filtered_tasks = sorted(filtered_tasks, key=lambda x: x[2])
else:
    filtered_tasks = sorted(filtered_tasks, key=lambda x: x[2], reverse=True)

# -------------------------
# Progress overview
# -------------------------
total_tasks = len(tasks)
completed_tasks = sum(task[5] for task in tasks)
pending_tasks = total_tasks - completed_tasks
progress_value = completed_tasks / total_tasks if total_tasks > 0 else 0

st.markdown('<div class="section-title">📊 Progress Overview</div>', unsafe_allow_html=True)
st.progress(progress_value)

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{total_tasks}</div>
            <div class="metric-label">Total Tasks</div>
        </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{completed_tasks}</div>
            <div class="metric-label">Completed</div>
        </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{pending_tasks}</div>
            <div class="metric-label">Pending</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------
# Task list
# -------------------------
st.markdown('<div class="section-title">📋 Your Tasks</div>', unsafe_allow_html=True)

if filtered_tasks:
    for task in filtered_tasks:
        task_id, name, task_deadline, task_category, task_priority, task_completed = task
        task_completed = bool(task_completed)

        st.markdown('<div class="task-card">', unsafe_allow_html=True)

        c1, c2, c3 = st.columns([5, 2, 1])

        with c1:
            checked = st.checkbox(
                name,
                value=task_completed,
                key=f"task_{task_id}"
            )

            if checked != task_completed:
                update_task_status(task_id, int(checked))
                st.rerun()

            st.markdown(
                f"<div class='meta-text'>{category_icon(task_category)} {task_category} • {priority_badge(task_priority)} • 📅 {task_deadline}</div>",
                unsafe_allow_html=True
            )

        with c2:
            today = datetime.date.today()
            deadline_date = datetime.datetime.strptime(task_deadline, "%Y-%m-%d").date()

            if task_completed:
                st.success("Completed")
            elif deadline_date < today:
                st.error("Overdue")
            else:
                st.info("Pending")

        with c3:
            if st.button("❌", key=f"delete_{task_id}"):
                delete_task(task_id)
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("No tasks match your current search/filter.")