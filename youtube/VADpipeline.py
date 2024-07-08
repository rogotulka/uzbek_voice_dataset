from pytube import YouTube
import ssl
from moviepy.editor import VideoFileClip
import wave
import contextlib
from pydub import AudioSegment
import os
import torch
import torchaudio
from pprint import pprint

# Set up SSL context
ssl._create_default_https_context = ssl._create_unverified_context


# Function to download YouTube video
def download_youtube_video(url, output_path='.'):
    try:
        yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
        stream = yt.streams.get_highest_resolution()
        downloaded_file = stream.download(output_path)
        print(f"Downloaded '{yt.title}' successfully!")
        return downloaded_file
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Function to convert video to audio (WAV)
def video_to_audio(input_file, output_file):
    video_clip = VideoFileClip(input_file)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_file)
    audio_clip.close()
    video_clip.close()
    print(f"Converted {input_file} to {output_file}")


# Function to get sampling rate of a WAV file
def get_sampling_rate(wav_file):
    with contextlib.closing(wave.open(wav_file, 'r')) as f:
        framerate = f.getframerate()
        return framerate


# Function to resample audio
def resample_audio(input_file, output_file, target_sample_rate):
    audio = AudioSegment.from_wav(input_file)
    audio = audio.set_frame_rate(target_sample_rate)
    audio.export(output_file, format='wav')
    print(f"Resampled {input_file} from {audio.frame_rate} Hz to {target_sample_rate} Hz and saved as {output_file}")


# Function to save audio segments
def save_audio_segments(wav, timestamps, sampling_rate, output_dir):
    if len(wav.shape) == 1:
        wav = wav.unsqueeze(0)
    for i, segment in enumerate(timestamps):
        start_frame = segment['start']
        end_frame = segment['end']
        audio_segment = wav[:, start_frame:end_frame]
        output_path = os.path.join(output_dir, f'segment_{i + 1}.wav')
        torchaudio.save(output_path, audio_segment, sampling_rate)


# Function to save video segments
def save_video_segments(video_path, timestamps, sampling_rate, output_dir):
    video = VideoFileClip(video_path)
    for i, segment in enumerate(timestamps):
        start_frame = segment['start']
        end_frame = segment['end']
        start_time = start_frame / sampling_rate
        end_time = end_frame / sampling_rate
        video_segment = video.subclip(start_time, end_time)
        output_path = os.path.join(output_dir, f'segment_{i + 1}.mp4')
        video_segment.write_videofile(output_path, codec="libx264")


if __name__ == "__main__":
    # Ask for user input
    video_url = input("Enter the YouTube video URL: ")
    base_name = input("Enter the base name for the files: ")

    # Define file and directory names
    video_file = f"{base_name}.mp4"
    audio_file = f"{base_name}.wav"
    resampled_audio_file = f"{base_name}_resampled.wav"
    audio_output_dir = f"{base_name}_audios"
    video_output_dir = f"{base_name}_videos"

    # Ensure the audio and video directories exist
    os.makedirs(audio_output_dir, exist_ok=True)
    os.makedirs(video_output_dir, exist_ok=True)

    # Download the video
    downloaded_video_file = download_youtube_video(video_url, output_path='.')

    if downloaded_video_file:
        # Convert the downloaded video to audio
        video_to_audio(downloaded_video_file, audio_file)

        # Get the sampling rate of the original audio
        original_sampling_rate = get_sampling_rate(audio_file)
        print(f"The original sampling rate of {audio_file} is {original_sampling_rate} Hz")

        # Resample the audio to 16000 Hz
        target_sample_rate = 16000
        resample_audio(audio_file, resampled_audio_file, target_sample_rate)

        # Set up VAD model
        SAMPLING_RATE = 16000
        torch.set_num_threads(1)
        USE_ONNX = False
        model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', force_reload=True,
                                      onnx=USE_ONNX)
        model.to('cpu')
        (get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils

        # Read the resampled audio file
        wav = read_audio(resampled_audio_file, sampling_rate=SAMPLING_RATE)

        # Get speech timestamps from the resampled audio file
        speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=SAMPLING_RATE, min_speech_duration_ms=1000)
        pprint(speech_timestamps)

        # Save the audio segments
        save_audio_segments(wav, speech_timestamps, SAMPLING_RATE, output_dir=audio_output_dir)

        # Save the video segments
        save_video_segments(downloaded_video_file, speech_timestamps, SAMPLING_RATE, output_dir=video_output_dir)
    else:
        print("Failed to download the video.")

