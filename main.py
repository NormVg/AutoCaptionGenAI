from pydub import AudioSegment
import math
import os
import speech_recognition as sr
from googletrans import Translator
from tqdm import tqdm
from datetime import timedelta
from moviepy.editor import VideoFileClip
import sys

translator = Translator()


def seconds_to_srt_time(seconds):
    """Convert seconds to SRT time format (hh:mm:ss,ms)."""

    delta = timedelta(seconds=seconds)
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = delta.microseconds // 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def append_to_srt(file_path, subtitle_number, text, start_time_sec, end_time_sec):
    """Append a new subtitle entry to the SRT file."""

    start_time = seconds_to_srt_time(start_time_sec)
    end_time = seconds_to_srt_time(end_time_sec)

    with open(file_path, 'a', encoding='utf-8') as srt_file:
        srt_file.write(f"{subtitle_number}\n")
        srt_file.write(f"{start_time} --> {end_time}\n")
        srt_file.write(f"{text}\n\n")

# Example usage
# append_to_srt("example.srt", 1, "Hello, world!", 0, 4)  # Appends the first subtitle from 0 to 4 seconds



def translate2SubLang(text,distLang:str = "en",src="hi"):
    resp = translator.translate(text, dest=distLang,src=src)
    return resp.text

def split_audio(file_path, output_dir):
    isFirstClip = True
    
    for i in os.listdir("output_directory/"):
    
        os.remove("output_directory/"+i)
    
    os.rmdir("output_directory/")
    
    
    audio = AudioSegment.from_file(file_path)
    
    # Chunk parameters
    chunk_duration_ms = 8000  # 8 seconds in milliseconds
    overlap_duration_ms = 2000  # 1 second in milliseconds
    step_duration_ms = chunk_duration_ms - overlap_duration_ms
    
    total_duration_ms = len(audio)
    
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Split audio into chunks
    for i in range(0, total_duration_ms, step_duration_ms):
        start_time_ms = i
        end_time_ms = min(i + chunk_duration_ms, total_duration_ms)
        
        # Extract chunk without overlap
        chunk = audio[start_time_ms:end_time_ms]
        
        # Timestamp for filename
        if isFirstClip:
            start_sec = math.floor(start_time_ms / 1000)
            isFirstClip = False
        else:
            start_sec = math.floor(start_time_ms / 1000)+2
        end_sec = math.floor(end_time_ms / 1000)
        timestamp = f"{start_sec}s_to_{end_sec}s"
        
        # Save chunk
        chunk.export(os.path.join(output_dir, f"{timestamp}.wav"), format="wav")

    print("Audio split and saved successfully!")

# Usage example
#split_audio("output_audio.wav", "output_directory")



def recognize_speech_from_wav(file_path,lang='en-IN'):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.record(source)
        
        try:
            recognized_text = recognizer.recognize_google(audio_data,language=lang)
            return recognized_text

        except sr.UnknownValueError:
            return None

        except sr.RequestError as e:
            return None

# Example usage:
# recognized_text = recognize_speech_from_wav('path_to_your_wav_file.wav')


def Audio2SrtFile(audiofile,srcLang="hi",distLang= "en",srtFile = "caption.srt"):
    
    split_audio(audiofile, "output_directory")

    FilesList = os.listdir("output_directory/")

    with tqdm(total=len(FilesList), desc="Processing chunks") as pbar:
    
        for index , i in enumerate(FilesList,start=1) :
            
            strartTime = int(i.split("_to_")[0].replace('s',""))
            endTime = int(i.split("_to_")[1].replace(".wav","").replace('s',""))
            print(index, strartTime,endTime,sep="---")
            

            recoText = recognize_speech_from_wav("output_directory/" + i,srcLang) 
            
            if not recoText:
                recoText = "---"

            print(recoText)

            transText  = translate2SubLang(recoText,distLang=distLang,src=srcLang).lower()
            print(transText)

            append_to_srt(srtFile, index , transText, strartTime, endTime)

            pbar.update(1)



def video_to_audio(video_path, audio_output_path):
    # Load the video file
    video_clip = VideoFileClip(video_path)
    
    # Extract the audio
    audio_clip = video_clip.audio
    
    # Write the audio file in the desired format (e.g., mp3 or wav)
    audio_clip.write_audiofile(audio_output_path)

    # Close the clips
    video_clip.close()
    audio_clip.close()

# Example usage
# video_to_audio(video_path, audio_output_path)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        video_to_audio(sys.argv[1] , "output_audio.wav")
        Audio2SrtFile("output_audio.wav",srcLang="hi",distLang="en")
        
    else:
        print("No arguments passed. please provide a video file")