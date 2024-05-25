import streamlit as st 
import streamlink
import time
import os
import signal
from streamlink import Streamlink
import ffmpeg

st.title(":blue[YouTube Live Downloader]")


url = st.text_input(':blue[Add Live youtube URL here:]')
def stream_to_url(url, quality='best'):
    # The "audio_only" quality may be invalid for some streams (check).
    session = Streamlink()
    streams = session.streams(url)
    return streams[quality].to_url()


if url :
    play_file=st.video(url)
    
    stream_url = stream_to_url(url)
    
    record=st.button("Record" )
    if record:
        stream_url = stream_to_url(url)
        with st.spinner('Recording ...'):
            fmpeg_process = (ffmpeg
    .input(stream_url)
    .output('video.mp4')
    .overwrite_output()
    .run_async())
        
    def stop():
        fmpeg_process.send_signal(signal.SIGQUIT)
    #st.button("Stop",on_click=stop)
                 
        if st.button("Stop",on_click=stop) :
            st.download_button(
                   label="Download Stream ....",
                   data="video.mp4",
                   file_name="stream.mp4",
                   mime="video/mp4"
                 )
