import gradio_client as grc

def transcribe(filepath):
    """
    Converts audio from filepath to text using gradio API and whisper space
    Parameters: 
        filepath (str): path to audio file
    """

    client = grc.Client("aliabd/whisper")
    job = client.predict(filepath)
    transcription = job.result()
    return transcription
