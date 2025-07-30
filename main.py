import streamlit as st
from layout_registry import get_layout
from style_presets import get_css

# Sample callback logic for testing
def fetch_repos(org): return ["repo1", "repo2"]
def validate_org(org): return org.startswith("gh-")
def update_env_callback(var, value): st.session_state[var] = value
def process_callback(files): print("Processing", files)

st.set_page_config(layout="wide")
st.markdown(get_css(), unsafe_allow_html=True)

tabs = ["Repository", "Settings", "Upload", "Jobs"]
selected = st.sidebar.radio("Navigate", tabs)

config = {
    "orgs": st.session_state.get("orgs", []),
    "repos": st.session_state.get("repos", []),
    "fetch_repos": fetch_repos,
    "validate_org": validate_org,
    "env_vars": ["API_KEY", "GITHUB_TOKEN"],
    "update_env": update_env_callback,
    "convert_mp4_to_mp3": process_callback,
    "job_list": [{"name": "Convert batch 1", "progress": 0.7, "status": "In Progress"}]
}

layout = get_layout(selected, config)
layout()