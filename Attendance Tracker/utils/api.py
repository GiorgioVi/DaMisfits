import requests, os, sqlite3, json

creds = "creds.json"
if __name__ == "__main__":
    creds = "../creds.json"

if not os.path.isfile(creds):
    print("Missing credentials file.")
    exit(1)

source = open(creds)
data = source.read()
data = json.loads(data)
api_base = "http://api.musixmatch.com/ws/1.1/{}"#formatting string for the command
musix_key = data["musix_match"]["key"]
ibm_user = data['text_to_speech']['username']
ibm_pwd = data['text_to_speech']['password']
source.close()

def get_song_id(track, artist=""):
    args = {"q_track":track, "q_artist":artist, "page_size":"5", "page":"1","s_track_rating":"desc","apikey":musix_key}
    msg = requests.get(api_base.format("track.search"), params=args)
    search_dict = msg.json()
    if search_dict["message"]["body"]["track_list"] == []:
        return 0
    return search_dict["message"]["body"]["track_list"][0]["track"]["track_id"]

def get_track(track_id):
    args = {"track_id":track_id, "apikey":musix_key}
    msg = requests.get(api_base.format("track.get"), params=args)
    search_dict = msg.json()
    return search_dict["message"]["body"]["track"]

def get_lyrics(track_id):
    args = {"track_id":track_id, "apikey":musix_key}
    msg = requests.get(api_base.format("track.lyrics.get"), params=args)
    search_dict = msg.json()
    if search_dict["message"]["body"] == []:
        return 0
    return search_dict["message"]["body"]["lyrics"]["lyrics_body"]

def get_artistid(artist):
    args = {"q_artist":artist, "apikey":musix_key}
    msg = requests.get(api_base.format("artist.search"), params=args)
    search_dict = msg.json()
    if search_dict["message"]["body"]["artist_list"] == []:
        return 0
    return search_dict["message"]["body"]["artist_list"][0]["artist"]["artist_id"]

def get_albums(artistid):
    args = {"artist_id":artistid, "apikey":musix_key}
    msg = requests.get(api_base.format("artist.albums.get"), params=args)
    search_dict = msg.json()
    return search_dict["message"]["body"]["album_list"]

def get_album_tracks(albumid):
    args = {"album_id":albumid, "apikey":musix_key}
    msg = requests.get(api_base.format("album.tracks.get"), params=args)
    search_dict = msg.json()
    return search_dict["message"]["body"]["track_list"]

def get_top_songs():
    args = {"page":"1", "page_size":"10", "country":"us", "f_has_lyrics":"1", "apikey":musix_key}
    msg = requests.get(api_base.format("chart.tracks.get"), params=args)
    search_dict = msg.json()
    return search_dict["message"]["body"]["track_list"]

def get_wav(text, filename, voice = "en-US_AllisonVoice"):
        apiurl = "https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize"
        headers = {"content-type": "application/json", "Accept": "audio/wav", "Content-Disposition": "attachment;filename=audio.wav"}
        dictionary = {"text": text, "voice": voice}
        try:
            r = requests.get(apiurl, auth=(ibm_user, ibm_pwd), stream=True, params=dictionary)
        except Exception as e:
            print e
            return False
        with open(filename, 'wb+') as f:
            f.write(r.content)
            return True

if __name__ == "__main__":
    get_wav("Testing text to speech API", "../static/test.wav")
