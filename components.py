import streamlit as st

def repo_org_panel(orgs, repos, fetch_repos, validate_org):
    @st.fragment
    def layout():
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader("🏢 Organization")

        org_cols = st.columns([4, 1])
        with org_cols[0]:
            new_org = st.text_input("", placeholder="Add new GitHub org...", key="repo_new_org_input")
        with org_cols[1]:
            if st.button("➕", key="repo_btn_add_org"):
                if validate_org(new_org):
                    if new_org not in st.session_state.orgs:
                        st.session_state.orgs.append(new_org)
                    st.session_state.repo_new_org_input = ""
                    st.experimental_rerun()
                else:
                    st.error("❌ Invalid GitHub organization")

        org_cols2 = st.columns([4, 1])
        with org_cols2[0]:
            org = st.selectbox("", orgs, key="repo_org_select", label_visibility="collapsed")
        with org_cols2[1]:
            if st.button("🗑️", key="repo_btn_del_org"):
                if org in st.session_state.orgs:
                    st.session_state.orgs.remove(org)
                    st.experimental_rerun()

        st.divider()
        st.subheader("📦 Repository")

        repo_cols = st.columns([4, 1])
        with repo_cols[0]:
            repo_select = st.selectbox("", repos, key="repo_repo_select", label_visibility="collapsed")
        with repo_cols[1]:
            if st.button("🔄", key="repo_btn_reload_repos"):
                st.session_state.repos = fetch_repos(org)
                st.success("Repos refreshed!")

        repo_cols2 = st.columns([4, 1])
        with repo_cols2[0]:
            repo_input = st.text_input(
                                        label="Repository input",
                                        placeholder="Or enter repo name manually",
                                        key="repo_repo_input",
                                        label_visibility="collapsed"
                                    )
        with repo_cols2[1]:
            if st.button("💾", key="repo_btn_save_repo"):
                st.session_state.selected_repo = repo_input or repo_select
                st.success(f"Repo saved: `{st.session_state.selected_repo}`")

        st.markdown("</div>", unsafe_allow_html=True)
    return layout

def settings_panel(env_vars, update_env_callback):
    @st.fragment
    def layout():
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader("⚙️ Environment Settings")
        for var in env_vars:
            value = st.text_input(f"{var}", value=st.session_state.get(var, ""), key=f"settings_{var}_input")
            if st.button(f"💾 Save {var}", key=f"settings_save_{var}"):
                update_env_callback(var, value)
                st.success(f"{var} updated!")
        st.markdown("</div>", unsafe_allow_html=True)
    return layout

def upload_panel(process_callback):
    @st.fragment
    def layout():
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader("📤 Upload & Convert")
        uploaded_files = st.file_uploader("Choose MP4 files", type=["mp4"], accept_multiple_files=True, key="upload_mp4_files")
        if st.button("🎬 Convert to MP3", key="upload_convert_button"):
            process_callback(uploaded_files)
            st.success("Conversion started!")
        st.markdown("</div>", unsafe_allow_html=True)
    return layout

def job_tracker_panel(job_list):
    @st.fragment
    def layout():
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader("📊 Job Status")
        for idx, job in enumerate(job_list):
            st.caption(f"🔄 {job['name']}")
            st.progress(job['progress'])
            st.text(job['status'])
        st.markdown("</div>", unsafe_allow_html=True)
    return layout