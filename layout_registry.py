from components import repo_org_panel, settings_panel, upload_panel, job_tracker_panel

def get_layout(tab_name, config):
    if tab_name == "Repository":
        return repo_org_panel(
            orgs=config["orgs"],
            repos=config["repos"],
            fetch_repos=config["fetch_repos"],
            validate_org=config["validate_org"]
        )
    elif tab_name == "Settings":
        return settings_panel(
            env_vars=config["env_vars"],
            update_env_callback=config["update_env"]
        )
    elif tab_name == "Upload":
        return upload_panel(process_callback=config["convert_mp4_to_mp3"])
    elif tab_name == "Jobs":
        return job_tracker_panel(config["job_list"])