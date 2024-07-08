````markdown
# VAD Pipeline

This project provides a pipeline to download a YouTube video, extract its audio, resample the audio, detect voice activity, and save both audio and video segments based on detected speech.

## Requirements

- Python 3.x
- Required Python packages:
  - pytube
  - moviepy
  - pydub
  - torch
  - torchaudio
  - soundfile
  - pip-system-certs

## Installation

1. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the required packages:
   ```sh
   pip install pytube moviepy pydub torch torchaudio
   ```

## Usage

1. Run the script:
   ```sh
   python VADpl.py
   ```

2. Enter the YouTube video URL and a base name for the files when prompted.

## Functionality

- Downloads the highest resolution of the provided YouTube video using `pytube`.
- Extracts and saves audio from the video as a WAV file using `moviepy`.
- Resamples the audio to 16 kHz using `pydub`.
- Detects speech segments in the resampled audio using the `silero-vad` model.
- Saves detected speech segments as separate audio and video files.

## Example

```sh
python VADpl.py
```

Enter:
- YouTube video URL: `https://www.youtube.com/watch?v=example`
- Base name for the files: `my_video`

The script will create directories `my_video_audios` and `my_video_videos` with the extracted segments.

## Notes

- Ensure `ffmpeg` is installed and accessible in your system's PATH for `moviepy` to function correctly.

