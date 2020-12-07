import time
import json
import base64
import pickle
import requests
import pypresence

LASTFM_API_URL = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={user}&api_key={key}&format=json"
DISCORD_API_POST_URL = "https://discord.com/api/v8/oauth2/applications/{client_id}/assets"


def main():
    try:
        with open("album_cache.p", "rb") as f:
            album_cache = pickle.load(f)
    except FileNotFoundError:
        album_cache = []
        with open("album_cache.p", "wb") as f:
            pickle.dump(album_cache, f)
    with open("config.json") as f:
        config = json.load(f)

    rpc = pypresence.Presence(config["client_id"], pipe=0)
    rpc.connect()

    while True:
        trackinfo = requests.get(LASTFM_API_URL.format(user=config["lastfm_name"],
                                                       key=config["lastfm_api_key"])).json()
        trackinfo = trackinfo["recenttracks"]["track"][0]

        album_name = trackinfo['album']['#text'].replace(" ", "_").lower()

        if album_name not in album_cache:
            print(f"caching album {album_name}...")
            cover_img = requests.get(trackinfo["image"][1]["#text"]).content
            cover_img = "data:image/jpeg;base64," + str(base64.b64encode(cover_img), "utf-8")
            requests.post(DISCORD_API_POST_URL.format(client_id=config["client_id"]),
                          json={"name": album_name,
                                "image": cover_img,
                                "type": 1},
                          headers={"Authorization": config["discord_token"],
                                   "content-type": "application/json"})
            album_cache.append(album_name)
            with open("album_cache.p", "wb") as f:
                pickle.dump(album_cache, f)

        rpc.update(details=trackinfo["album"]["#text"],
                   state=f"{trackinfo['artist']['#text']} - {trackinfo['name']}",
                   large_image=album_name)

        print(f"updating rpc with current track {trackinfo['name']}...")
        time.sleep(1)


if __name__ == '__main__':
    print("starting listening-to...")
    main()
