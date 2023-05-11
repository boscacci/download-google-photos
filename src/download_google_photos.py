import os
import requests
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

LOCAL_FOLDER_DESTINATION = "~/Desktop/google_photos/"

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/photoslibrary.readonly"]


def download_photos(album_id, output_folder):
    """Shows basic usage of the Photos v1 API.
    Prints the names and ids of the first 10 albums the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

        # Save the bearer token to a file
        with open("bearer_token.txt", "w") as file:
            file.write(creds.token)

    service = build(
        "photoslibrary", "v1", credentials=creds, static_discovery=False
    )

    # Call the Photos API
    results = (
        service.mediaItems()
        .search(body={"albumId": album_id, "pageSize": 100})
        .execute()
    )
    items = results.get("mediaItems", [])
    nextPageToken = results.get("nextPageToken", None)

    while nextPageToken:
        results = (
            service.mediaItems()
            .search(
                body={
                    "albumId": album_id,
                    "pageSize": 100,
                    "pageToken": nextPageToken,
                }
            )
            .execute()
        )
        items.extend(results.get("mediaItems", []))
        nextPageToken = results.get("nextPageToken", None)

    for item in items:
        url = item["baseUrl"] + "=d"
        file_name = item["filename"]
        response = requests.get(url)
        file_path = os.path.join(output_folder, file_name)

        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {file_name} to {file_path}")


def main():
    album_id = input("Enter the shared Google Photos album ID: ")
    output_folder = os.path.expanduser(LOCAL_FOLDER_DESTINATION)
    download_photos(album_id, output_folder)


if __name__ == "__main__":
    main()
