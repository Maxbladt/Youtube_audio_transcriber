import yt_dlp
import pandas as pd
import os
import openai


def scrape_channel_info(channel_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }

    video_list = []
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(channel_url, download=False)
            
            if 'entries' in result:
                for entry in result['entries']:
                    video_list.append({
                        'title': entry.get('title'),
                        'url': f"https://www.youtube.com/watch?v={entry.get('id')}",
                        'view_count': entry.get('view_count'),
                        'mp3_path': f"audio/{entry.get('title')}.mp3"
                    })
            print("Scraping channel info succeeded")
                    
        return pd.DataFrame(video_list)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def download_audio(video_url, save_dir):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(save_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp3',
        }],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("Audio download complete.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

def download_all_audios(df, save_dir):
    for index, row in df.iterrows():
        try:
            video_url = row['url']
            print(f"Downloading audio for video: {row['title']}")
            download_audio(video_url, save_dir)
        except Exception as e:
            print(f"Error occurred while downloading audio for video: {row['title']}. Continuing...")


def transcribe_audio(mp3_path, title, views):
    with open(mp3_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file, response_format="text")

    
    
    result = f"\nTitle: {title}\nYouTube views: {views}\n{transcript}"

    return result
def transcribe_videos(df,title_transcriptions, start=0, end=None, ):
    save_path=f"text/{title_transcriptions}.txt"
    if end is None:
        end = len(df)

    with open(save_path, "w") as file:  # Open the file for writing
        for index, row in df.iloc[start:end].iterrows():
            try:
                title = row['title']
                views = row['view_count']
                mp3_path = row['mp3_path']

                transcription = transcribe_audio(mp3_path, title, views)
                file.write(transcription + "\n\n")  # Write transcription to the file  

                # Feedback to the user
                print(f"Successfully transcribed: {title}")

            except Exception as e:
                print(f"An error occurred with video {title}: {e}")
def get_filename():
    while True:  # This loop will keep asking until a valid filename is provided
        title_transcriptions = input("Title of transcriptions: ")
        filename = f"{title_transcriptions}.txt"

        # Check if the file already exists
        full_path = f"text/{filename}"
        if os.path.exists(full_path):
            print("A file with this name already exists. Please enter a different title.")
        else:
            return title_transcriptions

def clear_audio_directory(directory="audio"):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)  # delete file
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

if __name__ == "__main__":
    #Magic variables
    print("This program automates the process of scraping video information from a given YouTube channel, downloading their audio, and transcribing the content into text. By converting YouTube episodes into textual data, users can perform comprehensive AI analyses, gaining insights into content trends, keyword usage, sentiment, and much more.\nYou need an OPEN-AI API key using an paid account, and the requirements.txt installed for this to work\n\n")
    channel_url = input("Channel URL: ")
    title_transcriptions = get_filename()
    print(f"Your selected filename is: {title_transcriptions}")
    openai.api_key = input("Enter your OPENAI-API key: ")


    #starting process

    #Scraping channel info
    print("Scraping channel info")
    df = scrape_channel_info(channel_url)
    df = df.sort_values(by='view_count', ascending=False)

    #Downloading audio files of youtube videos channel
    print("Downloading all audio files of youtube videos and converting them to MP3")
    save_directory = 'audio'
    download_all_audios(df, save_directory)
    print("Succesfully download all audio files of the youtube videos and converted them to MP3")


    #Transcribing using Openai API
    print("Transcribing the videos")
    transcribe_videos(df,title_transcriptions, 0) 
    clear_audio_directory()
    print("Cleared audio files.")
    print(f"Succesfully transcribed and saved to {title_transcriptions}.txt")






