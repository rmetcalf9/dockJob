# Manual utility app


def list_files_in_folder(google_client):
    project_folder = google_client.drive().find_folder_from_path(path="/Projects/Property/Business Cards")
    print(project_folder)
    (files, request) = google_client.drive().get_all_items_in_folder(folder_id=project_folder["id"])
    while request is not None:
        result = request.execute()
        for file in result["files"]:
            print("FFF", file)
        request = files.list_next(request, result)

def add_watch_notification(google_client):
    folder_id_to_watch = "1LhOLAK3AC3XYGm3mr2MpZ1uM0BJPcDwJ"

    trigger_url = APIAPP_TRIGGERAPIURL + "/trigger/" + DOCKJOB_APICLIENT_URLPASSCODE
    print("Setting up trigger", trigger_url)

    watch_response = google_client.drive().setup_watch_on_files(
        file_id=folder_id_to_watch,
        trigger_url=APIAPP_TRIGGERAPIURL + "/trigger/" + DOCKJOB_APICLIENT_URLPASSCODE,
        channel_id=DOCKJOB_APICLIENT_NONURLPASSCODE,
        token=DOCKJOB_APICLIENT_JOBREF
    )

    print("Watch response", watch_response)
