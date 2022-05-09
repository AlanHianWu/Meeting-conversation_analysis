import deepspeech
import numpy as np
import os
import wave
import webrtcvad
import wavSplit

def down_sample(p):
    import librosa
    import soundfile as sf
    
    y, sr = librosa.load(p)
    data = librosa.resample(y, sr, 16000)
    sf.write("downsampled_wav02.wav", data, 16000)


def load_model(model, scorer):
    beam_width = 10000
    alpha = 0.93
    beta = 1.18

    ds = deepspeech.Model(model)
    ds.enableExternalScorer(scorer) 
    ds.setScorerAlphaBeta(alpha, beta)
    ds.setBeamWidth(beam_width)

    return ds


def main_stt(full_audio, ds, audio, fs):
    audio_length = len(audio) * (1 / fs)
    time = full_audio - audio_length

    #Run deepspeech
    output = ds.stt(audio)
    
    return output, time


def vad_segment_generator(wavFile, aggressiveness):
    audio, sample_rate, audio_length = wavSplit.read_wave(wavFile)
    assert sample_rate == 16000
    vad = webrtcvad.Vad(int(aggressiveness))
    frames = wavSplit.frame_generator(30, audio, sample_rate)
    frames = list(frames)
    segments = wavSplit.vad_collector(sample_rate, 30, 225, vad, frames)

    return segments, sample_rate, audio_length


def main(audioFile=None, outFile=None):
    model_path = os.path.join(os.getcwd(), "models\deepspeech-0.9.3-models.pbmm")
    score = os.path.join(os.getcwd(), "models\deepspeech-0.9.3-models.scorer")
    
    if audioFile == None:
        audio_file = os.path.join(os.getcwd(), "downsampled_wav02.wav")
    else:
        audio_file = os.path.join(os.getcwd(), "audioFile.wav")
    
    model = load_model(model_path, score)
    
    
    segments, sample_rate, audio_length = vad_segment_generator(audio_file, 1.25)
    
    print("full audio lenght: ",audio_length // 60)
    
    full_audio_lenght = audio_length
    temp = audio_length 
    
    if outFile == None:
        f = open("transcript_file01.txt", 'a')
    else:
        f = open(audioFile, 'a')
  
    for i, segment in enumerate(segments):
        # Run deepspeech on the chunk that just completed VAD
        audio = np.frombuffer(segment, dtype=np.int16)
        output = main_stt(full_audio_lenght, model, audio, sample_rate)
        full_audio_lenght = output[1]
    
        print(" Time ==> ", "|{:02d}:{:02d}|".format( int((temp - full_audio_lenght) // 60), int((temp - full_audio_lenght) % 60)))
        print(" ==> ", output[0], "\n")        
        f.write("Time |{:02d}:{:02d}| ".format(int((temp - full_audio_lenght) // 60), int((temp - full_audio_lenght) % 60)) + output[0] + "\n")
    
    f.close()
 

if __name__ == "__main__":
    main()

    # down_sample(os.path.join(os.getcwd(), "Recording02.wav"))