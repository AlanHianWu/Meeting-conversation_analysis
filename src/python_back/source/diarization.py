# from pyannote.core import Segment, notebook
# import torch, wave
# import numpy as np
# from matplotlib import pyplot as plt

def first():
    pipeline = torch.hub.load('pyannote/pyannote-audio', 'dia')

    audio_file = "./output.wav"

    diarization = pipeline({'audio': audio_file})

    # print(diarization)
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
    return None

# from pyannote.audio import Pipeline
# pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")
# diarization = pipeline("./output.wav")
# print(diarization)



def second():
    
    from pyannote.audio import Pipeline
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")
    AUDIO_FILE = "./example.wav"
    dia = pipeline(AUDIO_FILE)
    for speech_turn, track, speaker in dia.itertracks(yield_label=True):
        print(f"{speech_turn.start:4.1f} {speech_turn.end:4.1f} {speaker}")

    return None


def tird():
    from resemblyzer import preprocess_wav, VoiceEncoder
    from pathlib import Path
    
    
    audio_file_path = 'output.wav'
    wav_fpath = Path(audio_file_path)
    
    wav = preprocess_wav(wav_fpath)
    encoder = VoiceEncoder("cpu")
    _, cont_embeds, wav_splits = encoder.embed_utterance(wav, return_partials=True, rate=16)
    print(cont_embeds.shape)
    
    return None

if __name__ == "__main__":
    # second()
    pass
 