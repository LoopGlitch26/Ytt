import streamlit as st
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
import ffmpeg

def download_and_trim_video(youtube_url, start_time, end_time):
    try:
        # Download YouTube video using pytube
        yt = YouTube(youtube_url)
        stream = yt.streams.filter(file_extension='mp4').first()
        video_path = stream.download()

        # Trim the video using moviepy
        clip = VideoFileClip(video_path).subclip(start_time, end_time)
        trimmed_path = 'trimmed_video.mp4'
        clip.write_videofile(trimmed_path, codec='libx264')

        # Return the trimmed video path
        return trimmed_path

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def main():
    st.title("YouTube Video Trimmer")

    # Get user input: YouTube URL, start time, and end time
    youtube_url = st.text_input("Enter the YouTube video URL:")
    start_time = st.text_input("Enter the start time (in seconds):")
    end_time = st.text_input("Enter the end time (in seconds):")

    if st.button("Trim and Download"):
        # Check if input fields are not empty
        if youtube_url and start_time and end_time:
            try:
                start_time = float(start_time)
                end_time = float(end_time)
                trimmed_path = download_and_trim_video(youtube_url, start_time, end_time)

                if trimmed_path:
                    # Offer the download link
                    st.success("Video successfully trimmed and downloaded!")
                    st.download_button(label="Download Trimmed Video", data=trimmed_path)
            except ValueError:
                st.error("Invalid input for start or end time. Please enter a valid number.")
        else:
            st.error("Please fill in all the required fields.")

if __name__ == "__main__":
    main()

