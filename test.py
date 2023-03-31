import gradio_client as grc

client = grc.Client("aliabd/whisper")
job = client.predict("hello-world.wav", api_name="transcribe")  

print(job.result())
