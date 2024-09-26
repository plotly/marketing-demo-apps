import os

import numpy
import requests
from PIL import Image

from constants import PATH_TO_DATA


def DEV_download_google_sample_data():
    """
    Download sample project images to data/ folder, this only happens once,
    after that the download is skipped if the data exists.
    """

    def download_file(url, destination):
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(destination, "wb") as file:
            for chunk in response.iter_content(chunk_size=32768):
                if chunk:
                    file.write(chunk)

    def downsample_tiff(input_path, output_path, scale_factor):
        img = Image.open(input_path)
        new_width = int(img.width * scale_factor)
        new_height = int(img.height * scale_factor)
        resized_img = img.resize((new_width, new_height), resample=Image.BILINEAR)
        resized_img.save(output_path)

    sample_data_links = {
        "spiral": [
            "https://drive.google.com/uc?export=download&id=1EHFOWmieLBfzednlcwAXMSmyv418u5Oj",
            "https://drive.google.com/uc?export=download&id=19Gu0y-VsAGwf9d8y57QwEj96x9JbrJRj",
            "https://drive.google.com/uc?export=download&id=135M2GHMuMo_ObHmfqqrDesp0eqvsQ-5t",
            "https://drive.google.com/uc?export=download&id=1C6tfVwjhYukIi2ZqHK5jYwphDXYODp7M",
            "https://drive.google.com/uc?export=download&id=1bU7umIIUJWQrP1vvSCjzbi1WAXptF91e",
            "https://drive.google.com/uc?export=download&id=1DsEGE1ECyN848SnYhdftYpLqG8kcZ-6D",
            "https://drive.google.com/uc?export=download&id=1L99iHiTUGWoeUQh3WLjOQki6NRvr9wEc",
            "https://drive.google.com/uc?export=download&id=1XJwwFsiPgJD4Rb1OjthhEILo6_JW9zst",
            "https://drive.google.com/uc?export=download&id=13Xldntc34OW6q9NShFF098gkXojDZ2wk",
            "https://drive.google.com/uc?export=download&id=1PNphlCDcXDlH_Sq5jHx0tU7TRMFyCE1M",
        ],
        "toothpick": [
            "https://drive.google.com/uc?export=download&id=1krqJpNwFFY6Vd7HmWRdFIEn4807KYuAv",
            "https://drive.google.com/uc?export=download&id=1FhfDBVhH5eW2bMoZPw0YrG-EXDYgse4C",
            "https://drive.google.com/uc?export=download&id=1vLZkjbD3x9116iBvushXSJ10-s4ngjZv",
            "https://drive.google.com/uc?export=download&id=1OuXO_VTHBFJfbhKHuwq1tyYUmjw4R3HF",
            "https://drive.google.com/uc?export=download&id=1CvMz9NF0D4oGHOVPSPtDJhZ7KZTG9wqs",
            "https://drive.google.com/uc?export=download&id=1Al0HlKEC3olDGv2rM2PnRU5Y9I6DBmhn",
            "https://drive.google.com/uc?export=download&id=1scnCNFWDVsp2uLBCiTnJ2FXldn1oT3QH",
            "https://drive.google.com/uc?export=download&id=1oLrDRC2By3NZ9JfSlnOeBWIdvrDTc8fi",
            "https://drive.google.com/uc?export=download&id=1xn03w2NaOYX0ijRxxgUibc-BmflV281h",
            "https://drive.google.com/uc?export=download&id=1Q2KX2EBl8gJcW0VwhsZP5YZLCWWXyNgj",
            "https://drive.google.com/uc?export=download&id=1gup8H3Y5m8hwOOH20ov9-6dUDWMk5wN6",
            "https://drive.google.com/uc?export=download&id=1wR0snAkxWPBhnPHHZWz4kHMWhT5WZo4I",
            "https://drive.google.com/uc?export=download&id=1iTVFigWEDmhFUIaWA64wmf6fmVhCwgnF",
        ],
        "check_handedness": [
            "https://drive.google.com/uc?export=download&id=1yJqGQdttkdUuxDzcSNnUfNjFS0It4l_d",
            "https://drive.google.com/uc?export=download&id=1woKTlWEkYB4nB__Bk8ioKvpTxjcEZ2lz",
            "https://drive.google.com/uc?export=download&id=1k4yot122LXzfFKaBmRY9n1HTu_Cc8OvO",
            "https://drive.google.com/uc?export=download&id=1VT-cv3y_tci3bHyMdIHYXXJhfOZRqykH",
            "https://drive.google.com/uc?export=download&id=1jVYFoN91tv7s2EwKf1FtlUDp62DTJK53",
            "https://drive.google.com/uc?export=download&id=1TMdnG9Uu3n_nDPyQGrNUgwCrA1HVJSmj",
            "https://drive.google.com/uc?export=download&id=1dSuEMBSq0uMgRGmavVsoaO1cVSPjh8Dt",
            "https://drive.google.com/uc?export=download&id=15xUp0etuEdCVxFSBz4JLZpUP5GyWUeNd",
            "https://drive.google.com/uc?export=download&id=1ptRo4JVjehgp478OGWnfTTxhvGDNO98v",
            "https://drive.google.com/uc?export=download&id=1W3DftX6nbc9qLVrEzO8aa8HQNAWwu1bn",
            "https://drive.google.com/uc?export=download&id=19af8U1Jm0wEmYZXneilHYw7mm771nzBm",
            "https://drive.google.com/uc?export=download&id=1IV3vCHsY98S5rfOEQ-bFgl0lCI6UryQ2",
            "https://drive.google.com/uc?export=download&id=12Erf8H4TdA6bs0Z1AMDq1cGc5I_SeP9p",
            "https://drive.google.com/uc?export=download&id=1BzIfZw7PfcncvacZ0EzFm6uZrqCTULiY",
            "https://drive.google.com/uc?export=download&id=17KYY-Iwid0PxSxki5FT6VQH1d5XNWMMD",
            "https://drive.google.com/uc?export=download&id=1XsynOCCqFpz6CZIAiryKIlgsIrjCMWE2",
            "https://drive.google.com/uc?export=download&id=1Gdf8aI9bb5H7eYNEcj2-Dbb5uAeisuLV",
        ],
    }
    base_directory = PATH_TO_DATA

    print("Downloading sample data...")
    print(PATH_TO_DATA)
    if PATH_TO_DATA == "data":
        if not os.path.exists(base_directory):
            os.makedirs(base_directory)

    for project, urls in sample_data_links.items():
        project_directory = os.path.join(base_directory, project)
        if not os.path.exists(project_directory):
            os.makedirs(project_directory)

        for i, url in enumerate(urls):
            destination = os.path.join(project_directory, f"{i}.tiff")

            if os.path.exists(destination):
                print(f"File {destination} already exists. Skipping download. ")
                continue

            download_file(url, destination)
            downsample_tiff(destination, destination, 0.5)
            print(f"Downloaded {destination}")

    print("All files downloaded successfully.")


def get_data_project_names():
    """
    Get available project names from the main Tiled container,
    filtered by types that can be processed (Container and ArrayClient)
    """
    project_names = os.listdir(PATH_TO_DATA)
    return project_names


def get_data_sequence_by_name(project_name):
    """
    Data sequences may be given directly inside the main client container,
    but can also be additionally encapsulated in a folder.
    """
    # get a dictionnary of all files in directory, where the key starts at 0 and the value is the file
    # name

    path = os.path.join(PATH_TO_DATA, project_name)
    data = os.listdir(path)
    project = {}
    for i, file in enumerate(data):
        im = Image.open(os.path.join(path, file))
        im = numpy.array(im)
        project[i] = im
    return project


def get_data_shape_by_name(project_name):
    """
    Retrieve shape of the data
    """
    path = os.path.join(PATH_TO_DATA, project_name)
    if os.path.exists(path):
        number_slices = len(os.listdir(path))
        return number_slices
    return 0
