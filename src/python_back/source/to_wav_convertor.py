import os
import ffmpy

'''simple mp4 tp wav at 16000hz convertor'''

inputdir = ''
outputdir = ''
for filename in os.listdir(inputdir):
    actual_filename = filename[:-4]
    if(filename.endswith(".mp4")):
        os.system('ffmpeg -i {}/{} -acodec pcm_s16le -ar 16000 {}/{}.wav'.format(inputdir, filename, outputdir, actual_filename))
    else:
        continue