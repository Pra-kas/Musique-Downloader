# Musique-Downloader

# Spotify Playlist Downloader

Download your favorite Spotify playlists with ease!

## Features

- Downloads Spotify playlists from given links.
- Converts downloaded tracks to MP3 format.
- Supports resuming interrupted downloads.

## Requirements

- Python 3.x
- spotipy library
- pytube library

## How to Use

- Clone the repository.

    ```
      git clone https://github.com/Pra-kas/Musique-Downloader.git
    ```

- Install dependencies with
  
    ```
      pip3 install -r requirements.txt
    ```
- Run the script with
 
    ```
      python3 spoyou.py -p <playlist_link>
    ```
- Run the script with
  
    ```
      python3 spoyou.py -s <song_link>
    ```
## Error 

Incase of network issues or internal error 
    
- Create resume.txt in the same directory
   ``` 
      touch resume.txt
   ```
  - Write the count of downloaded songs in  resume.txt
  - After run the script again
  - This will resume the download instead os downloading songs from the beggining
        
## Configuration

Ensure your `.env` file includes the following:
