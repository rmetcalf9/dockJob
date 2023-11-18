from google.oauth2.credentials import Credentials
import json
from .drive import DriveApiHelpers, NotFoundException
from googleapiclient.discovery import build

class GoogleClient():
    client_Secret_file = None
    client_id = None
    client_secret = None
    creds = None

    drive_service = None

    def __init__(self, client_Secret_file):
        self.client_Secret_file = client_Secret_file
        with open(self.client_Secret_file, 'r') as secret_file:
            secrets = json.load(secret_file)
        self.client_id = secrets["installed"]["client_id"]
        self.client_secret = secrets["installed"]["client_secret"]
        self.drive_service = None

    def get_current_refresh_token(self):
        return json.loads(self.creds.to_json())["refresh_token"]

    def setup_auth(self, refresh_token, scopes=None):
        info = {
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        self.creds = Credentials.from_authorized_user_info(info, scopes)

    def drive(self):
        if self.drive_service is None:
            self.drive_service = build('drive', 'v3', credentials=self.creds)
        return DriveApiHelpers(drive_service=self.drive_service)
