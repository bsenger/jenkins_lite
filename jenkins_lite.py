import streamlit as st
import json
import os
import pandas as pd
import asyncio
from datetime import datetime

# ----------- Config and Setup ----------
st.set_page_config(page_title="Jenkins-Lite", layout="wide")
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
DATA_PATH = os.path.join(DATA_DIR, "jobs.json")
LOG_PATH = os.path.join(DATA_DIR, "build_logs.csv")

# ----------- Plugin Interface ----------
class PostBuildPlugin:
    def run(self, job_name, job_data):
        pass

class TTSPlugin(PostBuildPlugin):
    def run(self, job_name, job_data):
        if "Speak" in job_name:
            st.info(f"🗣️ Speaking summary for job: {job_name}")
            # Integrate TTS logic here

class FileMovePlugin(PostBuildPlugin):
    def run(self, job_name, job_data):
        if "Transfer" in job_name:
            st.info(f"📤 Transferring files for job: {job_name}")
            # File moving logic goes here

class MediaConvertPlugin(PostBuildPlugin):
    def run(self, job_name, job_data):
        if "Convert" in job_name:
            st.info(f"🎬 Converting media for: {job_name}")
            # Replace with convert_all(folder_path)

# Register plugins
plugins = [
    TTSPlugin(),
    FileMovePlugin(),
    MediaConvertPlugin()
]

def run_post_build_plugins(job_name, job_data):
    for plugin in plugins:
        plugin.run(job_name, job_data)

# ----------- File Operations ----------
def load_jobs():
    if os.path.exists(DATA_PATH):
        try:
            if os.path.getsize(DATA_PATH) == 0:
                st.warning("⚠️ jobs.json is empty. Reinitializing...")
                return {}

            with open(DATA_PATH, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            st.warning("⚠️ jobs.json is corrupted. Starting fresh.")
            return {}
    return {}

def save_jobs(jobs):
    try:
        with open(DATA_PATH, "w") as f:
            json.dump(jobs, f, indent=2)
    except Exception as e:
        st.error(f"❌ Failed to save jobs: {e}")

def log_build(job_name, status):
    try:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_df = pd.DataFrame([[job_name, status, time]], columns=["Job", "Status", "Timestamp"])
        if os.path.exists(LOG_PATH):
            log_df.to_csv(LOG_PATH, mode="a", header=False, index=False)
        else:
            log_df.to_csv(LOG_PATH, index=False)
    except Exception as e:
        st.error(f"❌ Failed to log build: {e}")

# ----------- Build Simulator ----------
async def run_build(job_name, jobs, plugin_active):
    jobs[job_name]["status"] = "Running"
    save_jobs(jobs)
    await asyncio.sleep(3)
    status = "Success" if "Test" not in job_name else "Failed"
    jobs[job_name]["status"] = status
    jobs[job_name]["last_build"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_jobs(jobs)
    log_build(job_name, status)

    if status == "Success":
        run_post_build_plugins(job_name, jobs[job_name])
        if plugin_active:
            st.toast(f"📧 Email sent: Build succeeded for {job_name}")

# ----------- UI and State ----------
jobs = load_jobs()

st.sidebar.title("🔧 Manage Jenkins-Lite")
plugin_active = st.sidebar.checkbox("🔔 Email Notify Plugin (demo)", value=True)
st.sidebar.button("🛠️ Configure System")
st.sidebar.button("📦 Plugin Manager")

st.title("🧩 Jenkins-Lite Dashboard")
st.caption("Real-time simulation • Plugin-ready • Extensible automation")

# Create new job
st.subheader("📁 Create New Job")
new_job = st.text_input("Enter job name")
if st.button("Create Job") and new_job:
    if new_job not in jobs:
        jobs[new_job] = {"status": "Idle", "last_build": "Never"}
        save_jobs(jobs)
        st.success(f"✅ Job '{new_job}' added!")
    else:
        st.warning("⚠️ Job already exists!")

# Display existing jobs
st.subheader("📂 Job Status")
for name, data in jobs.items():
    with st.expander(f"💼 {name}"):
        st.markdown(f"**Status**: `{data['status']}`")
        st.markdown(f"**Last Build**: {data['last_build']}")
        if st.button(f"Run Build: {name}"):
            asyncio.run(run_build(name, jobs, plugin_active))
            st.rerun()
        if data["status"] == "Success":
            st.success("✅ Build succeeded.")
        elif data["status"] == "Failed":
            st.error("❌ Build failed.")
        elif data["status"] == "Running":
            st.info("🚀 Build in progress...")
        else:
            st.warning("🟡 Idle")

# Display build history
st.subheader("📜 Build History")
if os.path.exists(LOG_PATH):
    try:
        log_df = pd.read_csv(LOG_PATH)
        if log_df.empty or log_df.columns.size == 0:
            st.info("📄 Build log is empty — no builds yet.")
        else:
            st.dataframe(log_df, use_container_width=True)
        st.dataframe(log_df, use_container_width=True)
    except Exception as e:
        st.warning(f"⚠️ Couldn't load build log: {e}")
else:
    st.info("No builds logged yet.")

if plugin_active:
    st.markdown("---")
    st.subheader("🔌 Plugins")
    st.info("📧 Email Notify Plugin is active (placeholder for future feature)")

st.markdown("---")
st.caption("Built by Bhuvnesh & Copilot • Modular & Scalable Jenkins-Lite")