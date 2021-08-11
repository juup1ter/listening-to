import time
import json
import base64
import pickle
import requests
import pypresence
import re
import discord
from discord.ext import commands
from pypresence import presence

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
    with open('replace.json') as content:
        special_characters = json.load(content)

    lfm = "lfm"
    lfmimg = config['lfmimg']
        
    if lfm in album_cache and lfm:
        print("small image found! skipping first cache process...\n")
    else:
        print("small image not found! caching...")
        requests.post(DISCORD_API_POST_URL.format(client_id=config["client_id"]),
                      json={"name": "lfm",
                            "image": lfmimg,
                            "type": 1},
                      headers={"Authorization": config["discord_token"],
                               "content-type": "application/json"})
        album_cache.append("lfm")
        with open("album_cache.p", "wb") as f:
            pickle.dump(album_cache, f)
        print("cached successfully!\n")

    rpc = pypresence.Presence(config["client_id"], pipe=0)
    rpc.connect()

    old_trackname = "" 

    while True:
        try:
            trackinfo = requests.get(LASTFM_API_URL.format(user=config["lastfm_name"],
                                                           key=config["lastfm_api_key"])).json()
            trackinfo = trackinfo["recenttracks"]["track"][0]

            album_text = trackinfo["album"]["#text"]
            album_display = trackinfo["album"]["#text"] + "​​"
            track_display = trackinfo["name"] + "​​"
            replace = special_characters
            album_name = album_text.translate(str.maketrans(replace)).lower()[:32]            
            album_discord = ''.join([str(ord(x) - 96) for x in album_name])[:32]
            
            if album_discord not in album_cache and album_discord:
                print(f"{album_text} not found in album cache, caching...")
                cover_img = requests.get(
                    trackinfo["image"][1]["#text"]).content
                cover_img = "data:image/jpeg;base64," + \
                    str(base64.b64encode(cover_img), "utf-8")
                requests.post(DISCORD_API_POST_URL.format(client_id=config["client_id"]),
                              json={"name": album_discord,
                                    "image": cover_img,
                                    "type": 1},
                              headers={"Authorization": config["discord_token"],
                                       "content-type": "application/json"})
                print(f"converted {album_text} to {album_discord} successfully!")
                print(f"{album_text} sent to discord correctly!")
                album_cache.append(album_discord)
                with open("album_cache.p", "wb") as f:
                    pickle.dump(album_cache, f)
                print("cached succesfully!\n")

            rpc.update(details=f"{track_display}",
                       state=f"by {trackinfo['artist']['#text']}",
                       large_image=album_discord if album_discord else None,
                       small_image="lfm",
                       small_text=f"scrobbling on account {config['lastfm_name']}",
                       large_text=album_display if album_display else None)
            
            if old_trackname != trackinfo["name"]:
                print(f"updating rpc with current track {trackinfo['name']}...")
                old_trackname = trackinfo["name"]
                print("successfully set rpc!\n")

            time.sleep(0.3)

        except Exception as e:
            print("exception occurred:", e)
            print("skipping generic lastfm error: 'recenttracks', you can ignore this\n")

if __name__ == '__main__':
    print("welcome to listening-to!\n")
    main()
