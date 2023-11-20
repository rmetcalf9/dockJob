# Manual utility app
import time
import uuid

def list_files_in_folder(google_client, context):
    project_folder = google_client.drive().find_folder_from_path(path="/Projects/Property/Business Cards")
    print(project_folder)
    (files, request) = google_client.drive().get_all_items_in_folder(folder_id=project_folder["id"])
    while request is not None:
        result = request.execute()
        for file in result["files"]:
            print("FFF", file)
        request = files.list_next(request, result)

def add_watch_notification(google_client, context):
    folder_id_to_watch = "1LhOLAK3AC3XYGm3mr2MpZ1uM0BJPcDwJ"

    trigger_url = context["APIAPP_TRIGGERAPIURL"] + "/trigger/" + context["DOCKJOB_APICLIENT_URLPASSCODE"]
    print("Setting up trigger", trigger_url)

    context["watch_setup"] = {
        #"channel_id": context["DOCKJOB_APICLIENT_NONURLPASSCODE"] No longer want to use constant
        "channel_id": str(uuid.uuid4())
    }

    watch_response = google_client.drive().setup_watch_on_files(
        file_id=folder_id_to_watch,
        trigger_url=context["APIAPP_TRIGGERAPIURL"] + "/trigger/" + context["DOCKJOB_APICLIENT_URLPASSCODE"],
        channel_id=context["watch_setup"]["channel_id"],
        token=context["DOCKJOB_APICLIENT_JOBREF"]
    )

    context["watch_setup"]["resource_id"] = watch_response["resourceId"]

    print("Watch response", watch_response)

def clear_watch_notification(google_client, context):
    folder_id_to_watch = "1LhOLAK3AC3XYGm3mr2MpZ1uM0BJPcDwJ"
    print("Clearing watch")
    if "watch_setup" not in context:
        print("You must add a watch first")

    clear_Response = google_client.drive().clear_watch_on_files(
        channel_id=context["watch_setup"]["channel_id"],
        resource_id=context["watch_setup"]["resource_id"]
    )
    print(clear_Response)

    del context["watch_setup"]

def monitor_folder_for_new_files(google_client, context):
    folder_id_to_watch = "1LhOLAK3AC3XYGm3mr2MpZ1uM0BJPcDwJ"

    (_, file_id_list) = google_client.drive().get_list_of_new_files(folder_id_to_watch, None)

    while True:
        time.sleep(1)
        (new_files, file_id_list) = google_client.drive().get_list_of_new_files(folder_id_to_watch, file_id_list)
        for file in new_files:
            print("Saw new file", file)


