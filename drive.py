from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

import credential_handler


creds = credential_handler.get_creds()


def edit_file(file_id):
    """
    Edits the contents of a file with specified id.
    """
    try:
        service = build('drive', 'v3', credentials=creds)
        media = MediaFileUpload(
            "test_file_2.txt", mimetype="text/plain", resumable=True
        )
        service.files().update(fileId=file_id, media_body=media).execute()

    except HttpError as e:
        print(e)


def delete_object(object_id):
    """
    Trashes an object or a file. (you may still see it in the file's list)
    """
    try:
        service = build('drive', 'v3', credentials=creds)
        body_value = {"trashed": True}
        service.files().update(fileId=object_id, body=body_value).execute()

    except HttpError as e:
        print(e)


def move_file(file_id, folder_id):
    """
    Moves file to folder with their specified ids.
    """
    try:
        service = build('drive', 'v3', credentials=creds)
        file = service.files().get(fileId=file_id, fields="parents").execute()
        previous_parents = ",".join(file.get("parents"))
        file = (
            service.files()
            .update(
                fileId=file_id,
                addParents=folder_id,
                removeParents=previous_parents,
                fields="id, parents",
            )
            .execute()
        )
        return file.get("parents")

    except HttpError as e:
        print(e)


def upload_file_to_folder(file_name, folder_id):
    """
    Adds a file to a folder with a specified name.
    """
    try:
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            "name": file_name,
            "parents": [folder_id]
        }
        media = MediaFileUpload(
            "test_file.txt", mimetype="text/plain", resumable=True
        )

        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        return file.get("id")
    except HttpError as e:
        print(e)


def create_folder(name):
    """
    Creates folder with a specified name.
    """
    try:
        service = build('drive', 'v3', credentials=creds)
        file_metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        file = service.files().create(body=file_metadata, fields="id").execute()
        print(f'Folder ID: "{file.get("id")}".')
        return file.get("id")

    except HttpError as e:
        print(e)


def search_files():
    """
    Shows all user files and folders.
    """
    try:
        service = build('drive', 'v3', credentials=creds)
        results = service.files().list(q="").execute()
        items = results.get('files', [])
        return items

    except HttpError as e:
        print(e)
        return None
