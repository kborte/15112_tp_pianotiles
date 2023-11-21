import librosa
import json

uploadFile = open("songBeats.json", "r+")
data = json.load(uploadFile)["songs"]
currentSongBeats = dict()

for song in data.keys():
    currentSongBeats[song] = data[song]

newSong = "test"
url = songUrl
y, sr = librosa.load(f"{url}")

hop_length = 512

oenv = librosa.onset.onset_strength(y = y, sr = sr, hop_length = hop_length)

tempo, beats = librosa.beat.beat_track(y = y, sr = sr)

beat_times = librosa.frames_to_time(beats, sr = sr).tolist()

print(beat_times)

currentSongBeats[newSong] = beat_times