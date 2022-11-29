#!/usr/bin/env python3

import datetime
import requests
import subprocess
import sys

CUR_DATE = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
APT_MIRROR_LOG_FILE = f"/opt/apt-mirror/var/{CUR_DATE}.log"
SOFTFREEZE_REMOTE_REPO_API_URL = "{{ softfreeze_remote_repo_api_url }}"
{# it's no longer needed, since we are using just remote repo instead of snapshots
SOFTFREEZE_DISTRIBUTION_LIST = {{ apt_mirrors_deb | map(attribute="dists") | list | flatten | map("regex_replace", "^([\w-]+)\s+.*$", "\\1") | list }}
SOFTFREEZE_VIRTUAL_REPO_API_URL = "{{ softfreeze_virtual_repo_api_url }}"
#}

SLACK_CHANNEL = "#infra_alerts"
SLACK_NAME = "Softfreeze status"
SLACK_WEBHOOK = "{{ slack_webhook_url }}"

def slack_request(status, message):
    json_body = {
        "channel": SLACK_CHANNEL,
        "username": SLACK_NAME,
        "attachments": [
            {
                "color": status,
                "text": message
            }
        ]
    }
    requests.post(SLACK_WEBHOOK, json=json_body)

def main():
    slack_request("good", "Updating remote repo's cache")

    # Disabling offline mode, before updating repo's cache
    _headers = {"Authorization": f"Bearer {{ svc_softfreeze_token }}"}
    _payload = {"offline": False}
    try:
        requests.post(SOFTFREEZE_REMOTE_REPO_API_URL, json=_payload, headers=_headers)
    except requests.exceptions.RequestException as e:
        slack_request("danger", f"Error while disabling offline mode for remote repo: `{e}`")
        raise SystemExit(e)

    # Update remote's repo cache. Running apt-mirror
    with open(APT_MIRROR_LOG_FILE, "w+") as log:
        proc = subprocess.Popen(["/usr/bin/apt-mirror"], stdout=log, stderr=log)
    ret_code = proc.wait()
    if ret_code != 0:
        slack_request("danger", f"apt-mirror exited with `{ret_code}`. See `{APT_MIRROR_LOG_FILE}`")
        sys.exit(ret_code)

{# it's no longer needed, since we are using just remote repo instead of snapshots
    # Make a snapshot via Artifactory API
    _headers = {"Authorization": f"Bearer {{ svc_softfreeze_token }}"}
    _snapshot_name = f"{datetime.datetime.now():%Y%m%d}"
    _payload = {"tag": _snapshot_name,
                "targetRepo": "{{ softfreeze_snapshots_repo }}"}
    for _distribution in SOFTFREEZE_DISTRIBUTION_LIST:
        _payload["distribution"] = _distribution
        try:
            requests.post(SOFTFREEZE_SNAPSHOTS_API_URL, json=_payload, headers=_headers)
        except requests.exceptions.RequestException as e:
            slack_request("danger", f"Error while making a snapshot for distribution {_distribution}: {e}")
            raise SystemExit(e)
#}
    # Enabling offline mode, after updating repo's cache
    _payload = {"offline": True}
    try:
        requests.post(SOFTFREEZE_REMOTE_REPO_API_URL, json=_payload, headers=_headers)
    except requests.exceptions.RequestException as e:
        slack_request("danger", f"Error while enabling offline mode for remote repo: `{e}`")
        raise SystemExit(e)

    slack_request("good", "Done")

if __name__ == "__main__":
    main()
