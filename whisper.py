import gradio_client as grc
import mimetypes
import requests
import base64

def get_mimetype(filename):
    mimetype = mimetypes.guess_type(filename)[0]
    if mimetype is not None:
        mimetype = mimetype.replace("x-wav", "wav").replace("x-flac", "flac")
    return mimetype


def encode_file_to_base64(f):
    with open(f, "rb") as file:
        encoded_string = base64.b64encode(file.read())
        base64_str = str(encoded_string, "utf-8")
        mimetype = get_mimetype(f)
        return (
            "data:"
            + (mimetype if mimetype is not None else "")
            + ";base64,"
            + base64_str
        )

def transcribe(filepath):
    """
    Converts audio from filepath to text using gradio API and whisper space
    Parameters: 
        filepath (str): path to audio file
    """

    # client = grc.Client("aliabd/whisper")
    # job = client.predict(filepath)
    # job.result()
    ### currently erroring out with gradio_client.utils.InvalidAPIEndpointError

    b64_audio = encode_file_to_base64(filepath)
    response = requests.post("https://aliabd-whisper.hf.space/run/transcribe", json={
        "data": [
            {"name":"audio.wav","data":b64_audio},
        ]
    }).json()

    transcription = response["data"][0]
    return transcription
