#internal
import functions as func
import hmm


# Testing with temp files
def main():
    #path = "Data/P!nk_-_Raise_Your_Glass_(Official_Video).wav"      # 287 frames/ 6 seconds
    path = "Data/Lorde_-_Team.wav"
    #path = "Data/Rolling_in_the_deep.wav"                           # 282 frames / 6 seconds
    #func.songHandler(path)
    hmm.chordHandler(path)


if __name__ == "__main__":
    main()
