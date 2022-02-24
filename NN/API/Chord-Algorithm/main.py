#internal
import functions as func
import hmm
import match_templates as temp
import chordACA

# Testing with temp files
def main():
    #path = "Data/P!nk_-_Raise_Your_Glass_(Official_Video).wav"      # 287 frames/ 6 seconds
    path = "Data/Lorde_-_Team.wav"
    #path = "Data/Rolling_in_the_deep.wav"                           # 282 frames / 6 seconds

    #  aubio.slice_source_at_stamps(path, [0,48000], output_dir=newpath,) # Absolutely terrible quality for some reason
    #func.songHandler(path)         # No chord detection yet
    #temp.templateMatch(path)        # Seems really bad
    #chordACA.getChords(path)   

if __name__ == "__main__":
    main()
