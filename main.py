from datetime import timedelta
import whisper
from moviepy import VideoFileClip
import typer
import warnings
from googletrans import Translator

import asyncio

from tqdm import tqdm

translator = Translator()
app = typer.Typer()

warnings.simplefilter("ignore",UserWarning)

async  def translate2SubLang(text,distLang:str="en"):

    resp = await translator.translate(text, dest=distLang)

    return resp.text


def seconds_to_srt_time(seconds):
    """Convert seconds to SRT time format (hh:mm:ss,ms)."""

    delta = timedelta(seconds=seconds)
    hours, remainder = divmod(delta.seconds, 3600)

    minutes, seconds = divmod(remainder, 60)\

    milliseconds = delta.microseconds // 1000

    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def append_to_srt(file_path, subtitle_number, text, start_time_sec, end_time_sec):
    """Append a new subtitle entry to the SRT file."""

    start_time = seconds_to_srt_time(int(start_time_sec))

    end_time = seconds_to_srt_time(int(end_time_sec))

    with open(file_path, 'a', encoding='utf-8') as srt_file:
        srt_file.write(f"{subtitle_number}\n")
        srt_file.write(f"{start_time} --> {end_time}\n")
        srt_file.write(f"{text}\n\n")

def wisper_speech_to_text(file_path, model_name='base'):
    print('Loading model...')
    model = whisper.load_model(model_name)
    print('Transcribing...')
    result = model.transcribe(file_path,verbose=False)
    # print('Saving result...')
    filtered_result = [ [x['text'],x['start'],x['end'] ] for x in result['segments']]
    return filtered_result

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


async def ProcessAudio(audio: str, output: str, model: str = 'base',translate: str = "none"):
    res = wisper_speech_to_text(audio,model)

    for i,r in tqdm(enumerate(res,start=1)):

      if translate != "none":
        r[0] = await translate2SubLang(r[0],translate)
      append_to_srt(output, i, r[0], r[1], r[2])


@app.command()
def audio2srt(audio: str, output: str, model: str = 'base',translate: str = "none"):
    # print(f"Hello {name}")
    asyncio.run( ProcessAudio(audio,output,model,translate))

@app.command()
def video2srt(video: str, output: str, model: str = 'base',translate: str = "none"):
    video_to_audio(video, 'temp_audio.mp3')
    ProcessAudio('temp_audio.mp3',output,model,translate)


if __name__ == "__main__":
    app()
