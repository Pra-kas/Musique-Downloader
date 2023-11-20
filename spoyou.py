import argparse
import csv
from spotipy.oauth2 import SpotifyClientCredentials
import pytube
from youtubesearchpython import VideosSearch
from moviepy.editor import AudioFileClip
import os
import spotipy
import re
from dotenv import load_dotenv

uname = os.getlogin()

def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Process some input data.')

    # Add the input option (e.g., file) argument
    parser.add_argument('-p', '--playlist', type=str, help='playlist link')
    parser.add_argument('-s', '--song', type=str, help='song name')
    # Add other options or arguments as needed

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the input option value
    if args.playlist:
        playlist = args.playlist
        env_path = "/home/" + uname  + "/Musique-Downloader/spos.env"
        load_dotenv(dotenv_path=env_path)

        CLIENT_ID = os.getenv("CLIENT_ID", "")
        CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
        OUTPUT_FILE_NAME = "track_info.csv"

        PLAYLIST_LINK = playlist

        client_credentials_manager = SpotifyClientCredentials(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )  

        session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", PLAYLIST_LINK):
            playlist_uri = match.groups()[0]
        else:
            raise ValueError("Expected format: https://open.spotify.com/playlist/...") 

        #getting playlist name 
        playlist_details = session.playlist(playlist_uri)
        playlist_name = playlist_details["name"]

        #making a new directory to store songs 
        parent_path = "/home/" + uname + "/Music/"
        path = os.path.join(parent_path,playlist_name)
        if os.path.exists(path):
            print("Directory already exists! Making it the download path...")
        else:
            os.mkdir(path)

        # Initialize variables for pagination
        offset = 0
        limit = 100  # The maximum limit per request
        all_tracks = []

        while True:
            # Retrieve tracks in batches with pagination
            tracks = session.playlist_tracks(playlist_uri, offset=offset, limit=limit)["items"]

            if not tracks:
                break

            all_tracks.extend(tracks)
            offset += limit

        with open(OUTPUT_FILE_NAME, "w", encoding="utf-8") as file:
            writer = csv.writer(file)

            # write header column names
            writer.writerow(["track", "artist"])

            # extract name and artist
            for track in all_tracks:
                name = track["track"]["name"]
                artists = ", ".join(
                [artist["name"] for artist in track["track"]["artists"]]
            )

                # write to csv
                writer.writerow([name, artists])

        count = 1

        #import the csv file with songs and artists name 
        with open('/home/'+uname+'/Musique-Downloader/track_info.csv',newline='') as f:
            reader = csv.reader(f)
            data = list(reader)


        def get_download(video_url):
            # Get the YouTube video
            yt = pytube.YouTube(video_url)

            # Get the highest quality audio stream
            audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()

            if audio_stream:
                # Download the audio
                audio_path = audio_stream.download(output_path = path + "/")

                # Convert the audio from MP4 to MP3
                audio_path_mp3 = audio_path.replace(".mp4", ".mp3")
                audio_clip = AudioFileClip(audio_path)
                audio_clip.write_audiofile(audio_path_mp3)
                audio_clip.close()

                # Clean up the downloaded files
                os.remove(audio_path)

                print("Audio downloaded in MP3 format with the highest quality.")
            else:
                print("No MP3 audio streams available for download.")
    
        def resume_search(data, count):
            try:
                with open('resume.txt', 'r') as pos:
                    position_str = pos.read().strip()
                    if position_str:
                        position = int(position_str)
                        os.remove('resume.txt')
                        return position,data[position][0] + ' by ' + data[position][1]
            except FileNotFoundError:
                return count,data[count][0] + ' by ' + data[count][1]


        def get_url(search):
            results = search.result()
            for video in results["result"]:
                video_title = video["title"]
                video_id = video["id"]
                video_url = "https://www.youtube.com/watch?v=" + video_id
                print(f"Title: {video_title}")
                return video_url


        while count < len(data):
            count, search_query = resume_search(data, count)
            

            # Create a VideosSearch object
            videos_search = VideosSearch(search_query, limit=1)

            # Get the search results
            url = get_url(videos_search)

            try:
                print(count)
                get_download(url)
                count += 1

            except KeyboardInterrupt:
                with open('resume.txt', 'w') as last:
                    last.write(str(count))
                break
    
            except Exception as e:
                print(e)
                search = VideosSearch(search_query,limit=5)
                get_url(search)
    elif args.song:
        song = args.song
        # Define your search query
        search_query = song
        # Create a VideosSearch object
        videos_search = VideosSearch(search_query, limit=1)
        # Get the search results
        results = videos_search.result()
        for video in results["result"]:
            video_title = video["title"]
            video_id = video["id"]
            video_url = "https://www.youtube.com/watch?v=" + video_id
            print(f"Title: {video_title}")
            print(f"Video URL: {video_url}")

        try:
        # Get the YouTube video
            yt = pytube.YouTube(video_url)

        # Get the highest quality audio stream
            audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()

            if audio_stream:
            # Download the audio
                audio_path = audio_stream.download(output_path="/home/" + uname + "/Music/")

            # Convert the audio from MP4 to MP3
                audio_path_mp3 = audio_path.replace(".mp4", ".mp3")
                audio_clip = AudioFileClip(audio_path)
                audio_clip.write_audiofile(audio_path_mp3)
                audio_clip.close()

            # Clean up the downloaded files
                os.remove(audio_path)

                print("Audio downloaded in MP3 format with the highest quality.")
            else:
                print("No MP3 audio streams available for download.")

        except pytube.exceptions.RegexMatchError as e:
            print("Regex match error:", e)
        except Exception as e:
            print("An error occurred:", e)

if __name__ == "__main__":
    main()
