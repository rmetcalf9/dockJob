from APIClients import GoogleClient
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import json
import inquirer
import Manapp

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

options = []
options.append(("List files in folder", Manapp.list_files_in_folder))
options.append(("Add watch notification", Manapp.add_watch_notification))
options.append(("Manually watch for new files", Manapp.monitor_folder_for_new_files))
options.append(("Quit", None))
questions = [
    inquirer.List('action',
                  message="What do you want to do?",
                  choices=options,
                  ),
]
while True:
    answers = inquirer.prompt(questions)
    if answers["action"] is None:
        print("Quitting")
        exit(0)
    answers["action"](google_client)

print("End of trigger creator")
