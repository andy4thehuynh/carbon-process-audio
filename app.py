import time
import os
import boto3

from chalice import Chalice

app = Chalice(app_name='carbon-process-audio')
app.debug = True

# Set the value of APP_BUCKET_NAME in the .chalice/config.json file.
S3_BUCKET = os.environ.get('APP_BUCKET_NAME', '')
client = boto3.client('transcribe')


@app.on_s3_event(bucket=S3_BUCKET, events=['s3:ObjectCreated:*'])
def s3_handler(event):
    app.log.debug("-------------------------------")
    media_file_uri = "".join(["s3://", S3_BUCKET, "/", event.key])
    app.log.debug('media_file_uri: {}'.format(media_file_uri))
    transcription_job_name = 'AudioToTextJob-{}'.format(int(time.time()))
    app.log.debug('transcription_job_name: {}'.format(transcription_job_name))

    response = client.start_transcription_job(
        TranscriptionJobName=transcription_job_name,
        LanguageCode='en-US',
        Media={
            'MediaFileUri': media_file_uri
        },
    )

    app.log.debug('transcription response: {}'.format(response))
    app.log.debug("-------------------------------")
