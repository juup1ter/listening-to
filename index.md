## listening-to
A simple discord rpc lastfm integration using pypresence
You should host your own instance because centralization is bad


### Installation
1. Clone and cd into this github repository with
    ```bash
    git clone https://github.com/youoralovedone/listening-to/ && cd listening-to
    ```
1. Go to the [discord dev portal](https://discord.com/developers/) and create a new application. You will replace client_id in config.json with your application id
2. Find your discord user token, there are plenty of guides on how to do so I will no go into details here. You will replace discord_token in config.json with your token
    > Be warned as this is in the grey area of discord TOS
    
    
    > DO NOT SHARE YOUR TOKEN ANYWHERE AND DO NOT COMMIT IT TO GITHUB
3. Go to the [lastfm api page](https://www.last.fm/api) and register for an account. You will replace lastfm_api_key in config.json with your api key
4. Finally, replace lastfm_name with your lastfm name in config.json



### Usage
To run, simply execute
```
python3 server.py
```
in whatever directory you cloned into
> discord takes a while to cache the album art so you might have to wait a little before the album art will show up

### Credits
Created by null, null#3333
Logo created by aveen, chill_alcoholic#2199

Thanks to qwertyquerty for [pypresence](https://github.com/qwertyquerty/pypresence)
