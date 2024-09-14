from moviepy.editor import VideoFileClip

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
video_path = "video.mkv"
audio_output_path = "output_audio.wav"  # Can also use .wav, .ogg, etc.
video_to_audio(video_path, audio_output_path)
