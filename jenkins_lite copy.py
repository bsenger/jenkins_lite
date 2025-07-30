import streamlit as st
import yaml

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Jenkins-lite Dashboard", layout="wide")

# ---------------- JOBS LOAD ----------------
def load_jobs():
    with open("jobs_config.yaml", "r") as f:
        return yaml.safe_load(f)

# ---------------- BUILD SIMULATOR ----------------
def build_job(job):
    logs = []
    logs.append(f"🚀 Starting build: {job['name']}")

    for plugin in job.get("plugins", []):
        logs.append(f"🔌 Running plugin: {plugin['name']}")
        # Simulate plugin work
        logs.append(f"✅ {plugin['name']} completed")

    # Store logs in session
    st.session_state[f"logs_{job['name']}"] = "\n".join(logs)

# ---------------- UI BLOCK ----------------
def render_job_card(job):
    col1, col2, col3 = st.columns([2, 3, 1])

    with col1:
        st.markdown(f"### {job['name']}")
        st.caption(f"Group: `{job.get('group', 'default')}`")

    with col2:
        st.button(
            f"🚀 Run {job['name']}",
            on_click=build_job,
            args=(job,),
            key=f"run_{job['name']}"
        )

    with col3:
        st.toggle(
            "🔔 Email Notify",
            value=True,
            key=f"{job['name']}_notify"
        )

    with st.expander("🔌 Plugin Config", expanded=False):
        for plugin in job.get("plugins", []):
            st.markdown(f"**{plugin['name']}**")
            config = plugin.get("config", {})
            for key, value in config.items():
                st.text_input(f"{key}", value, key=f"{job['name']}_{plugin['name']}_{key}")

    with st.expander("📜 Build Logs", expanded=False):
        log_text = st.session_state.get(f"logs_{job['name']}", "(No logs yet)")
        st.text_area("Logs", log_text, height=140, key=f"logs_{job['name']}_view")

    st.divider()

# ---------------- MAIN APP ----------------
st.sidebar.title("🧭 Jenkins-lite Controls")
st.sidebar.toggle("🌙 Dark Mode", value=True, key="theme_toggle")

jobs = load_jobs()
grouped = {}
for job in jobs:
    grouped.setdefault(job.get("group", "default"), []).append(job)

for group, job_list in grouped.items():
    st.header(f"🔹 {group.upper()} Jobs")
    for job in job_list:
        render_job_card(job)