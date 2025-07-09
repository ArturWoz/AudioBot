## Description


This is a simple Discord bot for playing music. Sources are added by plugin system. Every plugin has to provide playing a song, playing a list and a search function. The bot is designed for small-scale private usage, but is capable of serving multiple servers at once.


## Commands


* join - Join a voice channel
* leave - Join a voice channel
* shutdown - Shutdown the bot if the user is bot admin (listed in config file)
* play <plugin> <url> - Play a song
* list <plugin> <url> - Play a playlist
* search <plugin> <url> - Search for a song
* select <no> - Select from search command
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


Plugins are stored in plugins folder. They are loaded automatically.

