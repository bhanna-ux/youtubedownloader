import os
import streamlit as st
import datetime
from datetime import datetime
import streamlink
import time
import os
import signal
from subprocess import Popen, PIPE
import sys
import ffmpeg
from streamlink import Streamlink

import streamlit as st
import streamlink
import time

import signal
from streamlink import Streamlink
import ffmpeg

current_datetime = datetime.now().strftime("%H.%M")
output_file="Stream @ "+current_datetime
st.title(":blue[YouTube Live Downloader]")


url = st.sidebar.text_input(':blue[Add Live youtube URL here:]')
def stream_to_url(url, quality='best'):
    # The "audio_only" quality may be invalid for some streams (check).
    session = Streamlink()
    streams = session.streams(url)
    return streams[quality].to_url()





if url :
    play_file=st.video(url)


duration= st.sidebar.number_input("Minutes of recording " , step =1)
record=st.sidebar.button("Record" )
#record2=st.sidebar.button("Record 2 CLI")

#if record2:
    #Popen(["streamlink", url, "best", "-o", f"c:/users/afp/{output_file}.mp4"])
dd=duration*60
def recording():
    stream_url = stream_to_url(url)


    fmpeg_process = (ffmpeg
.input(stream_url,ss='00:00:00',to=dd)
.filter("fps",fps=25)
.output(
'C:/users/afp/video.mp4',map='0:0')
.overwrite_output()
.run_async()
)



if record:
    with st.sidebar:
        with st.spinner("Recording ..."):
            st.code(recording())
            time.sleep(dd)
            st.success('Recording Finished')




    def stop():
        fmpeg_process.send_signal(signal.CTRL_C_EVENT)
    #st.button("Stop",on_click=stop)
    st.sidebar.button("Stop",on_click=stop)


    with open("C:/users/afp/video.mp4", "rb") as file:
        btn = st.sidebar.download_button(
            label="Download Stream",
            data=file,
            file_name="stream.mp4",
            mime="video/mp4"
          )
