
# AutoCaptionGenAI

This project extracts audio from video files, transcribes the speech using Google's Speech Recognition API, translates it into a target language (default: English), and generates subtitles in SRT format. The project processes audio chunks with a slight overlap to improve transcription accuracy, then translates and writes each chunk's transcription into an SRT file with timestamps.

## Features
- **Audio extraction from video files**.
- **Speech-to-text transcription** using the `speech_recognition` library.
- **Translation** of transcribed text into a target language using `googletrans`.
- **SRT subtitle file generation** with proper timing.
- **Progress tracking** using `tqdm` while processing audio chunks.
- Configurable source and destination languages for transcription and translation.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [Customization](#customization)
- [License](#license)

## Installation

To run this project, you need to have Python 3 installed along with some required libraries.

1. Clone the repository:
   ```bash
   git clone https://github.com/NormVg/AutoCaptionGenAI
   cd AutoCaptionGenAI
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Required libraries include:
   - `pydub`
   - `speech_recognition`
   - `googletrans`
   - `tqdm`
   - `moviepy`

   You can install them manually if needed:
   ```bash
   pip install pydub speechrecognition googletrans==4.0.0-rc1 tqdm moviepy
   ```

### Additional Dependencies
Ensure that `ffmpeg` or `libav` is installed in your system to enable audio and video processing via `moviepy`. You can install it using:

- On **Ubuntu**:
   ```bash
   sudo apt update && sudo apt install ffmpeg
   ```

- On **MacOS** using Homebrew:
   ```bash
   brew install ffmpeg
   ```

## Usage

### Command-Line

1. **Run the program** by passing a video file path as an argument:

   ```bash
   python main.py path_to_video.mp4
   ```

   This will extract the audio, process it, generate transcriptions, translate the text, and output an SRT file (`caption.srt` by default).

### SRT Output
By default, the SRT file is saved as `caption.srt`. The file will contain timestamps and translated subtitles for the audio extracted from the video.

## Example

Here is an example of how to run the script:

```bash
python main.py my_video.mp4
```

### Expected Output
1. **Audio** will be extracted from `my_video.mp4` into `output_audio.wav`.
2. **SRT file** (`caption.srt`) will be generated containing the transcriptions and translations.

The structure of an SRT file:
```srt
1
00:00:00,000 --> 00:00:08,000
hello, welcome to this demo

2
00:00:08,000 --> 00:00:16,000
how are you today?
```

## Customization

### 1. Change the Chunk Duration
You can adjust the length of each audio chunk being processed by modifying the `chunk_duration_ms` and `overlap_duration_ms` in the `split_audio` function. 
```python
chunk_duration_ms = 15000  # 15 seconds in milliseconds
overlap_duration_ms = 2000  # 2 seconds of overlap
```

### 2. Modify Source and Target Language
By default, the source language is set to Hindi (`hi`) and the target language to English (`en`). You can change these in the `Audio2SrtFile` function call:
```bash
Audio2SrtFile("output_audio.wav", srcLang="fr", distLang="es")
```
This example will transcribe French audio and translate it into Spanish.

### 3. Change the Output SRT File Name
You can change the name of the output SRT file by passing a different `srtFile` parameter:
```bash
Audio2SrtFile("output_audio.wav", srcLang="hi", distLang="en", srtFile="my_custom_caption.srt")
```

### 4. Tweak Speech Recognition Language
The speech recognition language can be modified in the `recognize_speech_from_wav` function by changing the `lang` argument:
```python
recognize_speech_from_wav("output_directory/some_audio.wav", lang='fr-FR')  # Recognize French
```

## Project Structure

```bash
.
├── main.py                # Main script for extracting audio, recognizing speech, translating, and generating SRT
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── output_directory/      # Directory for storing intermediate audio chunks
```

## To-Do / Future Enhancements
- **Parallel processing** of audio chunks to improve performance.
- **Error handling** for cases when speech recognition or translation fails.
- Add more translation services for greater flexibility.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

### Key Sections:
- **Installation**: Explains how to install the project dependencies.
- **Usage**: Guides how to run the script via the command line.
- **Example**: Demonstrates the expected output.
- **Customization**: Allows users to tweak audio chunking, language, and output file configurations.
- **Future Enhancements**: Provides ideas for contributors.

Feel free to modify any section as per your specific requirements!