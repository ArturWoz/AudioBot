## Description


This is a simple Discord bot for playing music. Sources are added by plugin system. Every plugin has to provide playing a song, playing a list and a search function. The bot is designed for small-scale private usage, but is capable of serving multiple servers at once.


## Commands


* join - Join a voice channel
* leave - Join a voice channel
* shutdown - Shutdown the bot if the user is bot admin (listed in config file)
* play (plugin) (url) - Play a song
* list (plugin) (url) - Play a playlist
* search (plugin) (url) - Search for a song
* select (no) - Select from search command
* queue - Show the song queue
* shuffle - Shuffle the song queue
* repeat - Toggle repeat mode
* skip - Skips a song
* pause - Pause playing
* resume - Resume playing
* stop - Stop playing


## Setup


Bot is run as a regular Python project. File requirements.txt provides Python dependencies for the bot itself, but you need to remember about dependencies for your own plugins. FFmpeg executable is needed inside the bot directory or in PATH. File config\_examle.json defines a structure of a real config.json file that is needed.


## Plugin design


Plugins are stored in plugins folder. They are loaded automatically. Downloading files is recommended, as direct links to files on a server can expire before playing, if the song is in queue. Each plugin implements the following structure:

    class Plugin(plugins.Base):

        def play(self, path: str) -) str:
            #Argument is a url/path. Returns path to downloaded file.
    
        def playlist(self, path: str) -) list[str]:
            #Argument is a playlist url/path. Returns list of song urls/paths.
    
        def search(self, query: str) -) list[dict[str, str]]:
            #Argument is a search query. Returns list of dicts containing urls/paths and names in the following format: {"url": url, "title": title}
