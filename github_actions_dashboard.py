import streamlit as st
import requests

GITHUB_API = "https://api.github.com"

def get_headers(token):
    return {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}

def list_repos(token, user):
    url = f"{GITHUB_API}/users/{user}/repos"
    r = requests.get(url, headers=get_headers(token))
    if r.status_code == 200:
        return [repo["name"] for repo in r.json()]
    return []

def list_workflows(token, user, repo):
    url = f"{GITHUB_API}/repos/{user}/{repo}/actions/workflows"
    r = requests.get(url, headers=get_headers(token))
    if r.status_code == 200:
        return r.json().get("workflows", [])
    return []

def list_runs(token, user, repo, workflow_id):
    url = f"{GITHUB_API}/repos/{user}/{repo}/actions/workflows/{workflow_id}/runs"
    r = requests.get(url, headers=get_headers(token))
    if r.status_code == 200:
        return r.json().get("workflow_runs", [])
    return []

def trigger_workflow(token, user, repo, workflow_id, ref="main"):
    url = f"{GITHUB_API}/repos/{user}/{repo}/actions/workflows/{workflow_id}/dispatches"
    data = {"ref": ref}
    r = requests.post(url, headers=get_headers(token), json=data)
    return r.status_code == 204

def get_run_logs(token, user, repo, run_id):
    url = f"{GITHUB_API}/repos/{user}/{repo}/actions/runs/{run_id}/logs"
    r = requests.get(url, headers=get_headers(token))
    if r.status_code == 200:
        return r.content
    return b""

def main():
    st.title("GitHub Actions Jenkins-like Dashboard")

    token = st.text_input("GitHub Personal Access Token", type="password")
    user = st.text_input("GitHub Username or Org")

    if not token or not user:
        st.info("Enter your GitHub token and username/org to continue.")
        return

    # Views (simple grouping by repo or workflow name)
    st.sidebar.header("Views")
    custom_views = st.sidebar.text_area("Define views (comma-separated workflow names)", "")
    views = [v.strip() for v in custom_views.split(",") if v.strip()]

    repos = list_repos(token, user)
    repo = st.selectbox("Select Repository", repos)

    if repo:
        workflows = list_workflows(token, user, repo)
        if not workflows:
            st.warning("No workflows found in this repository.")
            return

        # Filter workflows by views
        if views:
            workflows = [wf for wf in workflows if wf["name"] in views]

        workflow_names = [wf["name"] for wf in workflows]
        workflow = st.selectbox("Select Workflow", workflow_names)

        if workflow:
            workflow_obj = next((wf for wf in workflows if wf["name"] == workflow), None)
            if workflow_obj:
                st.write(f"**Workflow ID:** {workflow_obj['id']}")
                st.write(f"**Path:** {workflow_obj['path']}")
                st.write(f"**State:** {workflow_obj['state']}")

                if st.button("Trigger Workflow"):
                    success = trigger_workflow(token, user, repo, workflow_obj["id"])
                    if success:
                        st.success("Workflow triggered successfully.")
                    else:
                        st.error("Failed to trigger workflow.")

                runs = list_runs(token, user, repo, workflow_obj["id"])
                st.subheader("Workflow Runs")
                for run in runs:
                    with st.expander(f"Run #{run['run_number']} - {run['status']} ({run['conclusion']})"):
                        st.write(f"Started: {run['created_at']}")
                        st.write(f"Branch: {run['head_branch']}")
                        st.write(f"Commit: {run['head_sha']}")
                        if st.button(f"Show Logs for Run {run['id']}", key=f"log_{run['id']}"):
                            logs = get_run_logs(token, user, repo, run["id"])
                            st.download_button("Download Logs", logs, file_name=f"run_{run['id']}_logs.zip")

if __name__ == "__main__":
    main()