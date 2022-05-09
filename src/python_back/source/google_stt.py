from google.cloud import speech_v1p1beta1 as speech
from google.cloud import storage
import wavSplit, webrtcvad
import numpy as np
import math

def cloud_upload(blob_name, path_to_file, bucket_name):

    storage_client = storage.Client.from_service_account_json(
        'C:/Users/wuala/Documents/Google_key/pragmatic-cat-345714-2221156cd8c7.json')

    #print(buckets = list(storage_client.list_buckets())

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(path_to_file)

    #returns a public url
    return blob.public_url

def cloud_delete():
    from google.cloud import storage

    my_storage = storage.Client()
    bucket = my_storage.get_bucket('meeting_stt_temp')
    blobs = bucket.list_blobs()
    for blob in blobs:
        blob.delete()


def convert_size(size_bytes):
    if size_bytes == 0:
       return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def vad_segment_generator(wavFile, aggressiveness):
    audio, sample_rate, audio_length = wavSplit.read_wave(wavFile)
    assert sample_rate == 16000
    vad = webrtcvad.Vad(int(aggressiveness))
    frames = wavSplit.frame_generator(30, audio, sample_rate)
    frames = list(frames)
    segments = wavSplit.vad_collector(sample_rate, 30, 100, vad, frames)

    return segments, sample_rate, audio_length
     

def transcribe_file(speech_file, fs, full_audio, audio):
    audio_length = len(audio) * (1 / fs)
    print("audio_length ==> ", audio_length)
    time = full_audio - audio_length    

    client = speech.SpeechClient()

    content = speech_file

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-IE",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result()

    re = []
    con = []
    for result in response.results:
        re.append(result.alternatives[0].transcript)
        con.append(result.alternatives[0].confidence)
    
    if len(con) == 0:
        con.append(0)
    return re, float(con[0]), time


def transcribe_gcs(gcs_uri, fs, full_audio, a):

    audio_length = len(a) * (1 / fs)
    print("audio_length ==> ", audio_length)
    time = full_audio - audio_length   

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code="en-IE",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result()

    re = []
    con = []
    for result in response.results:
        re.append(result.alternatives[0].transcript)
        con.append(result.alternatives[0].confidence)
    
    if len(con) == 0:
        con.append(0)
    
    return re, float(con[0]), time
    
def main(audioFile=None, name=None):
    if audioFile == None:
        speech_file = "./audiofiles/downsampled_wav02.wav"
    else:
        speech_file = audioFile


    segments, rate, audio_length = vad_segment_generator(speech_file, 2)
    
    full_audio_lenght = audio_length
    temp = audio_length 

    if name == None:
        f = open("google_transcript_file_03.txt", 'a')
    else:
        f = open(name, 'a')
    
    for i, segment in enumerate(segments):
        audio = np.frombuffer(segment, dtype=np.int16)
        a_size = convert_size(len(segment))
        a_length = len(audio) * (1 / rate)
        print("Audio :", a_size, a_length)
        
        if a_length <= 60:
        
            output = transcribe_file(segment, rate, full_audio_lenght, audio)
            full_audio_lenght = output[2]
    
            print("Time ==> ", "|{:02d}:{:02d}| Confidence |{:05f}|".format(int((temp - full_audio_lenght) // 60), int((temp - full_audio_lenght) % 60), output[1]))
            print("===> ", output[0], "\n")
            f.write("Time |{:02d}:{:02d}| Confidence |{:05f}|".format(int((temp - full_audio_lenght) // 60), int((temp - full_audio_lenght) % 60), output[1]) + " ".join(output[0]) + "\n")

        else:
            # use long file format
            print("\nLARGE FILE\n")
            gcs_uri = cloud_upload("audio", 'gs://meeting_stt_temp/audio', 'meeting_stt_temp')
            
            output = transcribe_gcs('gs://meeting_stt_temp/audio', rate, full_audio_lenght, audio)
            full_audio_lenght = output[2]
    
            print("Time ==> ", "|{:02d}:{:02d}| Confidence |{:05f}|".format(int((temp - full_audio_lenght) // 60), int((temp - full_audio_lenght) % 60), output[1]))
            print("===> ", output[0], "\n")
            f.write("Time |{:02d}:{:02d}| Confidence |{:05f}|".format(int((temp - full_audio_lenght) // 60), int((temp - full_audio_lenght) % 60), output[1]) + " ".join(output[0]) + "\n")
            cloud_delete()


    f.close()



if __name__ == "__main__":
    main()
    # transcribe_gcs('gs://meeting_stt_temp/audio', 10, 10, 'test')