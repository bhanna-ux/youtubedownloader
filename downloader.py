import os
import streamlit as st
import datetime
from datetime import datetime
import streamlink
import time
import os
import signal
import subprocess
from multiprocessing import Process
from subprocess import Popen, PIPE
import sys


st.title(":blue[YouTube Live Downloader]")

current_datetime = datetime.now().strftime("%H-%M")
url = st.text_input(':blue[Add Live youtube URL here:]')
if url :

    play_file=st.video(url)

record=st.sidebar.button("Record" )
stop = st.sidebar.button("Stop" )


output_file="Stream @"
# Function to download YouTube live stream

# Function to download YouTube live stream


if record:
    st.spinner(text="Recording...")
    command = "streamlink", url, "best", "-o", f"c:/users/afp/{output_file}.mp4"
    subprocess.run(command,shell=True)
    if stop:
        subprocess.terminate(shell=True)

with open("c:/users/afp/Stream @.mp4", "rb") as file:
    st.download_button(
                label="Download video",
                data=file,
                file_name="stream.mp4",
                mime="video/mp4"
              )
