from APIClients import GoogleClient
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import json

print("Start of trigger creator")

DOCKJOB_APICLIENT_GOOGLE_CLIENT_SECRET_FILE = "./client_secret.json"
APIAPP_TRIGGERAPIURL = "https://api.metcarob.com/memset_dockjob_triggerapi"

DOCKJOB_APICLIENT_URLPASSCODE = os.environ["DOCKJOB_APICLIENT_URLPASSCODE"]
DOCKJOB_APICLIENT_NONURLPASSCODE = os.environ["DOCKJOB_APICLIENT_NONURLPASSCODE"]
DOCKJOB_APICLIENT_JOBREF = os.environ["DOCKJOB_APICLIENT_JOBREF"]

SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]

private_login_file = "./private_login_file.json"


google_client = GoogleClient(
    client_Secret_file=DOCKJOB_APICLIENT_GOOGLE_CLIENT_SECRET_FILE
)

refresh_token = None
client_id = None
client_secret = None

if os.path.exists(private_login_file):
    with open(private_login_file, 'r') as private_login:
        contents = json.load(private_login)
    refresh_token = contents["refresh_token"]
else:
    flow = InstalledAppFlow.from_client_secrets_file(
        DOCKJOB_APICLIENT_GOOGLE_CLIENT_SECRET_FILE,
        SCOPES
    )
    creds = flow.run_local_server(port=0)
    cred_json = json.loads(creds.to_json())
    refresh_token = cred_json["refresh_token"]
    with open(private_login_file, 'w') as token:
        token.write(json.dumps({"refresh_token": refresh_token}))

google_client.setup_auth(
    refresh_token=refresh_token
)

# project_folder = google_client.drive().find_folder_from_path(path="/Projects/Property/Business Cards")
# print(project_folder)
# (files, request) = google_client.drive().get_all_items_in_folder(folder_id=project_folder["id"])
# while request is not None:
#     result = request.execute()
#     for file in result["files"]:
#         print("FFF", file)
#     request = files.list_next(request, result)

folder_id_to_watch = "1LhOLAK3AC3XYGm3mr2MpZ1uM0BJPcDwJ"

trigger_url = APIAPP_TRIGGERAPIURL + "/trigger/" + DOCKJOB_APICLIENT_URLPASSCODE
print("Setting up trigger", trigger_url)

watch_response = google_client.drive().setup_watch_on_files(
    file_id = folder_id_to_watch,
    trigger_url = APIAPP_TRIGGERAPIURL + "/trigger/" + DOCKJOB_APICLIENT_URLPASSCODE,
    channel_id = DOCKJOB_APICLIENT_NONURLPASSCODE,
    token = DOCKJOB_APICLIENT_JOBREF
)

print("Watch response", watch_response)

print("End of trigger creator")
