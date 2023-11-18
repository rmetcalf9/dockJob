
class NotFoundException(Exception):
    pass

class DriveApiHelpers():
    drive_service = None
    def __init__(self, drive_service):
        self.drive_service = drive_service

    def get_root_folder_id(self):
        return self.drive_service.files().get(fileId='root').execute()['id']

    def get_item_id(self, parent, name):
        files = self.drive_service.files()
        request = files.list(pageSize=100, q=f"name='{name}' and '{parent}' in parents and trashed=false", fields="nextPageToken, files(id, name, parents)")
        res = []
        while request is not None:
            result = request.execute()
            for file in result["files"]:
                res.append(file)
            request = files.list_next(request, result)
        if len(res) == 0:
            raise Exception(f"Error folder with {name} not found with parent {parent}")
        if len(res) != 1:
            raise Exception("Found too many")
        return res[0]["id"]

    def get_folder_id(self, path):
        if path[0] != "/":
            raise Exception("Path must start with /")
        if path=="/":
            return self.get_root_folder_id()
        path_components = path[1:].split("/")
        if len(path_components) == 1:
            print(path[1:])
            return self.get_item_id(parent=self.get_root_folder_id(), name=path[1:])
        else:
            cur_root = self.get_root_folder_id()
            for path in path_components:
                cur_root = self.get_item_id(parent=cur_root, name=path)
            return cur_root

    def get_all_items_in_folder(self, folder_id, restrict_mimetype=None):
        files = self.drive_service.files()
        query_string = f"'{folder_id}' in parents and trashed=false"
        if restrict_mimetype is not None:
            for mt in restrict_mimetype:
                query_string += f" and mimeType='{mt}'"

        return (files, files.list(pageSize=100, q=query_string, fields="nextPageToken, files(id, name, parents, mimeType)"))
        #Exmpale usage:
        # (files, request) = google_client.drive().get_all_items_in_folder(folder_id="1uTSyL7-DZ3PwHYAxv2OQsQvq81lXGX4F")
        # while request is not None:
        #     result = request.execute()
        #     for file in result["files"]:
        #         print("FFF", file)
        #     request = files.list_next(request, result)

    def find_folder_from_path(self, path, start_folder_id=None):
        if start_folder_id is None:
            if path[0] != "/":
                raise Exception("Specified root but path is not root")
            return self.find_folder_from_path(path=path[1:], start_folder_id=self.get_root_folder_id())

        path_elements = path.split("/")

        (files, request) = self.get_all_items_in_folder(folder_id=start_folder_id)
        while request is not None:
            result = request.execute()
            for file in result["files"]:
                if file["name"] == path_elements[0]:
                    if len(path_elements) == 1:
                        return file
                    return self.find_folder_from_path(path="/".join(path_elements[1:]), start_folder_id=file["id"])
            request = files.list_next(request, result)
        raise NotFoundException("Not found")

    def setup_watch_on_files(self, file_id, trigger_url, channel_id, token):
        # https://googleapis.github.io/google-api-python-client/docs/dyn/drive_v3.files.html#watch
        files = self.drive_service.files()

        body = {
            "id": channel_id,  # A UUID or similar unique string that identifies this channel.
            "type": "web_hook",  # The type of delivery mechanism used for this channel.
            "address": trigger_url,
            "token": token, # An arbitrary string delivered to the target address with each notification delivered over this channel. Optional.
            "expiration": None, # Date and time of notification channel expiration, expressed as a Unix timestamp, in milliseconds. Optional.
            "kind": "api#channel", # Identifies this as a notification channel used to watch for changes to a resource, which is `api#channel`.
            "params": None,
            "payload": None, #True or False,  # A Boolean value to indicate whether payload is wanted. Optional.
            "resourceId": None, # An opaque ID that identifies the resource being watched on this channel. Stable across different API versions.
            "resourceUri": None  # A version-specific identifier for the watched resource.
        }

        request = files.watch(
            fileId = file_id,
            body = body
        )
        result = request.execute()
        return result

    # REturns ([new files], current_list_of_ids)
    def get_list_of_new_files(self, folder_id, previous_list_of_files_ids):
        if previous_list_of_files_ids is None:
            previous_list_of_files_ids = []
        (files, request) = self.get_all_items_in_folder(folder_id=folder_id)

        new_files = []
        seen_file_ids = []
        while request is not None:
            result = request.execute()
            for file in result["files"]:
                seen_file_ids.append(file["id"])
                if file["id"] not in previous_list_of_files_ids:
                    new_files.append(file)
            request = files.list_next(request, result)

        return (new_files, seen_file_ids)

