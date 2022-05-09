print('importing . . .')
import audio, speech_to_text, summarisation, google_stt, dbp_spotlight
import sys
def main():
    # start audio
    try:
        time = input('enter recording time in seconds ')
        print(int(time))

        audio.run(time)
        
        method = input('Select method of transcribe local[1] or server[2]')
        if method == 1:
            details = input('please enter audio file path and desired transcibe file name, format path_to_audio_file,name')
        
            # transcribe
            speech_to_text.main(details[0], details[1])
        elif method == 2:
            details = input('please enter audio file path and desired transcibe file name, format path_to_audio_file,name')
            
            google_stt.main(details[0], details[1])
        else:
            print('invalid input')
            return None
        
        # summarize with bart
        print('summarising lastest file in transcripts')
        summarisation.main()
        
        print('populate database')
        neo4j = input('enter neo4j info, format url, user, pass : ')
        name = input('enter meeting name : ')
        
        try:
            neo4j = neo4j.strip().split()

            # popluate neo4j
            dbp_spotlight.main(name, neo4j)
            
            print('database populated!')
            
        except Exception as e:
            print(e)
        
    except Exception as e:
        print(e)

  
if __name__ == "__main__":
    main()
    