import streamlit as st
from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os

# Function to download the YouTube video
def download_youtube_video(video_url, video_path):
    yt = YouTube(video_url)
    yt_stream = yt.streams.filter(file_extension='mp4').first()
    yt_stream.download(output_path=video_path)

# Function to trim the video
def trim_video(video_path, start_time, end_time, trimmed_path):
    ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=trimmed_path)

def main():
    st.title("YouTube Video Trimmer")

    # Input fields for YouTube URL, start time, and end time
    youtube_url = st.text_input("Enter the YouTube video URL:")
    start_time = st.time_input("Select the start time:")
    end_time = st.time_input("Select the end time:")

    if st.button("Trim and Download"):
        if youtube_url and start_time and end_time:
            # Create temporary directories for video processing
            video_dir = "temp_video"
            trimmed_dir = "trimmed_video"
            os.makedirs(video_dir, exist_ok=True)
            os.makedirs(trimmed_dir, exist_ok=True)

            try:
                st.text("Downloading the video...")
                video_path = os.path.join(video_dir, "original_video.mp4")
                download_youtube_video(youtube_url, video_path)

                st.text("Trimming the video...")
                trimmed_path = os.path.join(trimmed_dir, "trimmed_video.mp4")
                start_seconds = start_time.hour * 3600 + start_time.minute * 60 + start_time.second
                end_seconds = end_time.hour * 3600 + end_time.minute * 60 + end_time.second
                trim_video(video_path, start_seconds, end_seconds, trimmed_path)

                st.text("Download the trimmed video:")
                with open(trimmed_path, "rb") as f:
                    st.download_button(label="Download", data=f, file_name="trimmed_video.mp4")

            except Exception as e:
                st.error(f"An error occurred: {e}")

            finally:
                # Clean up temporary directories
                os.remove(video_path)
                os.remove(trimmed_path)
                os.rmdir(video_dir)
                os.rmdir(trimmed_dir)

        else:
            st.warning("Please provide YouTube URL, start time, and end time.")

if __name__ == "__main__":
    main()
            
