import streamlit as st
import streamlink
import signal
import ffmpeg
from streamlink import Streamlink
import os
from datetime import datetime
import subprocess 
from subprocess import Popen,PIPE
from streamlit.components.v1 import components
import soundfile as sf
import librosa
import whisper
import itertools


st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 350px !important; # Set the width to your desired value
        }

    </style>
    """,
    unsafe_allow_html=True,
)

html ="""

<!DOCTYPE html>

    <html lang="en">

    <head>

        <meta charset="UTF-8">

        <meta name="viewport" content="width=device-widt, initial-scale=1.0">

        <title>1 Hour Timer</title>

        <style>

            body {

                font-family: Arial, sans-serif;color: #1F45FC;

                display: flex;

                justify-content: left;

                align-items: center;

                height: 100vh;

                margin: 0;

                background-color: rgba(255,255,255,0);

            }

            #timer {

                font-size: 17px;

                font-weight: bold;

            }

        </style>

    </head>

    <body>

        <div id="timer">00:00:00</div>

 

        <script>

            function updateTimer() {

                const timerElement = document.getElementById('timer');

                let seconds = 0;

 

                function pad(num) {

                    return num.toString().padStart(2, '0');

                }

 

                const intervalId = setInterval(() => {

                    seconds++;

                    const hours = Math.floor(seconds / 3600);

                    const minutes = Math.floor((seconds % 3600) / 60);

                    const remainingSeconds = seconds % 60;

 

                    timerElement.textContent = `${pad(hours)}:${pad(minutes)}:${pad(remainingSeconds)}`;

 

                    if (seconds >= 3600) {

                        clearInterval(intervalId);

                    }

                }, 1000);

            }

 

            updateTimer();

        </script>

    </body>

    </html>

"""




st.subheader(":blue[YTube Live Stream Recorder]",divider='red')
model=whisper.load_model('tiny')
col1, col2 = st.columns(2)

url = st.sidebar.text_input(':blue[Add Live youtube URL here:]'+':red[*]')
if url :
    with col1:
        st.write("Stream Live ")
        play_file=st.sidebar.video(url)
        
videoname=st.sidebar.text_input(':blue[Write Name of File]'+':red[*]')
c=datetime.now()
current_time=c.strftime('%H:%M')
#videoname=videoname +'@'+str(current_time)

def stream_to_url(url, quality='1080p'):
    # The "audio_only" quality may be invalid for some streams (check).
    session = Streamlink()
    streams = session.streams(url)
    return streams[quality].to_url()




  

def recordingaudio():
    os.makedirs('temp', exist_ok=True)
    stream_url = stream_to_url(url)
    fmpeg_process = (ffmpeg
.input(stream_url)
.audio
.output(
'temp/'+videoname+'.wav')
.overwrite_output()
.run_async()
)
    st.write(":red[RECORDING Audio ....]",height=30)
    st.components.v1.html(html,width=100,height=20)
    def Finish():
      fmpeg_process.send_signal(signal.SIGQUIT)
      st.write(':red[Recording FINISHED ..... ]',height=30)
    st.sidebar.button("Finish Recording ",on_click=Finish)


def record():
    os.makedirs('temp', exist_ok=True)
    process= subprocess.Popen( ["streamlink" , url ,
                                "best", "-o",'temp/'+videoname+'.mp4'])
    #process= subprocess.Popen( ["streamlink" , url ,
                               # "best",  "| ffmpeg -i pipe:0 -r 25 -c:v libx264 -preset fast -threads 4","-o",'temp/'+videoname+'.mp4'])
  #streamlink --stdout "STREAM_URL" best | ffmpeg -i pipe:0 -r 25 -c:v libx264 -preset fast -threads 4 output.mp4
  #stdout=process.communicate()
  #st.text('\n'.join(stdout.decode().split('\n')))
    st.write(":red[RECORDING Video ....]",height=30)
    st.components.v1.html(html,width=100,height=20)

    def Finish():
        process.send_signal(signal.SIGQUIT)
        st.write(':red[Recording FINISHED ..... ]',height=30)
    st.button("Finish Recording ",on_click=Finish)

def recording():
    
    stream_url = stream_to_url(url)
    os.makedirs('temp', exist_ok=True)
    fmpeg_process = (ffmpeg
.input(stream_url)
.filter("fps",fps=25)
.output(
'temp/'+videoname+'.mp4',map='0:0')
.overwrite_output()
.run_async()
)
    st.write(":red[RECORDING Video 25fps  ....]",height=30)
    st.components.v1.html(html,width=100,height=20)
    def Finish():
        fmpeg_process.send_signal(signal.SIGQUIT)
        st.write(':red[Recording FINISHED ..... ]',height=30)
        
    st.button("Finish Recording ",on_click=Finish)

if st.button("Play Recorded Video"):
    with col2 :
        st.write("Recorded File : "+ videoname )
        video_file = open('temp/'+videoname+'.mp4', "rb")
        video_bytes = video_file.read()
        st.video(video_bytes)


def done():

    lasttimeinterval=0


    for i in itertools.count():
        audio_array, sr = librosa.load('temp/'+videoname+'.wav', sr=16_000)
        timeinterval=len(audio_array)/sr
        t=audio_array[int(lasttimeinterval)*sr : int(timeinterval)*sr]
        sf.write("temp/split_interval.wav", t, sr)
        result=model.transcribe("temp/split_interval.wav" )
        if result['text']:

            #translated = GoogleTranslator(source='auto', target='en').translate(result['text'])

            yield str(datetime.timedelta(seconds=int(lasttimeinterval))) , result['text'] #st.text_area(label=' Transcript : ', value= result['text'] ,height=200)
            
        yield "\n"
        #yield translated
        #with col2:
                #yield st.write_stream(translated)

        lasttimeinterval=timeinterval

st.sidebar.button("Start Record Video  ",on_click=record) 
st.sidebar.button("Start Record Video 25fps  ",on_click=recording)
st.sidebar.button("Start Record Audio Only  ",on_click=recordingaudio) 
st.sidebar.button("Live Transcribe  ",on_click=done) 
#def pause():
  #fmpeg_process.send_signal(signal.SIGSTOP)
#st.sidebar.button("Pause",on_click=pause)

#def resume():
  #fmpeg_process.send_signal(signal.SIGCONT)
#st.sidebar.button("Resume",on_click=resume)






       #if Pause:
           #fmpeg_process.send_signal(signal.SIGSTOP)
        #if resume:
            #fmpeg_process.send_signal(signal.SIGCONT)
        #if Finish:
            #fmpeg_process.send_signal(signal.SIGQUIT)
def file_selector(folder_path='temp/'):
    
    #os.makedirs('temp', exist_ok=True)
    filenames = os.listdir(folder_path)
    selected_filename = st.sidebar.selectbox(':blue[select your file from Downloads Folder]', filenames)
    #return os.path.join(folder_path, selected_filename)
    with open(folder_path +selected_filename, "rb") as file:
        
        d=file.read()
        btn = st.sidebar.download_button(
                label=":red[Reload Page Before ]"+":blue[ Download ]",
                data=d,
                file_name=selected_filename,
                use_container_width=True
              )
    return os.path.join(selected_filename)
filename=file_selector()
st.sidebar.write('You selected `%s`' % filename) 







#with open('/home/bassem/Desktop/videos/video.mp4', "rb") as file:
#    d=file.read()
#    btn = st.sidebar.download_button(
#            label=":blue[Download Video]",
#            data=d,
#            file_name='recording.mp4',
#            mime='video/mp4',
#            use_container_width=True
#          )


st.sidebar.link_button(":red[Go to Transcription]",
"https://vspar-ia-v-transcript-01.afp.com/editor",
 use_container_width=True)
