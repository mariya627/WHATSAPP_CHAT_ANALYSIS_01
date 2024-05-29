import re
import pandas as pd
import streamlit as st
import zipfile
import os
import speech_recognition as sr
import numpy as np
import soundfile as sf

from googletrans import Translator
def preprocess(data):
    messages = []
    for line in data.split("\n"):
        # Split the line by ' - ' to separate the timestamp and message
        parts = line.split(' - ')
        if len(parts) > 1:
            message = parts[1]
            messages.append(message)
    usernames = []
    messages_cleaned = []
    for message in messages:
        parts = message.split(':')  # Split message on colon
        username = parts[0]  # Take the first part as the username
        message_cleaned = ':'.join(parts[1:]).strip()  # Join the remaining parts as the message
        usernames.append(username)
        messages_cleaned.append(message_cleaned)

    messages = []
    for line in data.split("\n"):
        # Split the line by ' - ' to separate the timestamp and message
        parts = line.split(' - ')
        if len(parts) > 1:
            message = parts[1]
            messages.append(message)

    date_pattern = r"\d{2}/\d{2}/\d{4}"
    dates = []

    for line in data.split("\n"):
        date = line.split("- ")[0]
        if date and re.match(date_pattern, line):
            dates.append(date)
    dates = []
    messages = []

    # Define date pattern
    date_pattern = r"\d{2}/\d{2}/\d{4}"

    # Process each line in the data
    for line in data.split("\n"):
        # Extract date and message
        parts = line.split(' - ')
        if len(parts) > 1:
            date = parts[0]
            message = parts[1]
            # Check if the line contains a valid date
            if re.match(date_pattern, date):
                dates.append(pd.to_datetime(date, format='%d/%m/%Y, %I:%M %p'))
                messages.append(message)

    # Extract usernames and clean messages
    usernames = [message.split(':')[0] for message in messages]
    messages_cleaned = [':'.join(message.split(':')[1:]).strip() for message in messages]

    # Create a dictionary with your lists
    data = {
        #"Message": messages,
        'Usernames': usernames,
        'Messages': messages_cleaned,
        "Date": dates,
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Extract date, month, and year into separate columns
    df['Only_date'] = df['Date'].dt.date
    df['Day'] = df['Date'].dt.day
    df['Day_name'] = df['Date'].dt.day_name()
    df['Month_num'] = df['Date'].dt.month
    df['Month'] = df['Date'].dt.month_name()
    df['Year'] = df['Date'].dt.year
    # Extract time into separate columns
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute
    period = []
    for hour in df[['Day', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period
    df = df.drop(df.index[0])
    return df


def preprocess_data(data):
    messages = []
    for line in data.split("\n"):
        # Split the line by ' - ' to separate the timestamp and message
        parts = line.split(' - ')
        if len(parts) > 1:
            message = parts[1]
            messages.append(message)
    usernames = []
    messages_cleaned = []
    for message in messages:
        parts = message.split(':')  # Split message on colon
        username = parts[0]  # Take the first part as the username
        message_cleaned = ':'.join(parts[1:]).strip()  # Join the remaining parts as the message
        usernames.append(username)
        messages_cleaned.append(message_cleaned)


    data = {
    # "Message": messages,
         'Usernames': usernames,
         'Messages': messages_cleaned,

     }

# Create a DataFrame
    data = pd.DataFrame(data)
    return data

# def main():
#     st.title('Whatsapp Chat Media ANalysis')
#
#     # Upload zip file
#     zip_file = st.file_uploader('Upload a zip file', type='zip')
#
#     if zip_file:
#         # Unzip the uploaded zip file
#         unzip_folder(zip_file)
#
#         # List all media files in the unzipped folder
#         media_files = [f for f in os.listdir('unzipped_folder') if os.path.isfile(os.path.join('unzipped_folder', f))]
#
#         # Display dropdown menu with media file options
#         selected_media = st.selectbox('Select a media file', media_files)
#
#         # Display the selected media file
#         if selected_media:
#             media_path = os.path.join('unzipped_folder', selected_media)
#             if media_path.endswith(('.jpg', '.jpeg', '.png', '.gif')):
#                 st.image(media_path)
#             elif media_path.endswith(('.mp4', '.avi', '.mov')):
#                 st.video(media_path)
#             elif media_path.endswith(('.mp3', '.ogg', '.opus')):
#                 st.audio(media_path, format='audio/ogg')
#             elif media_path.endswith('.pdf'):
#                 st.download_button(
#                     label='Download PDF',
#                     data=open(media_path, 'rb'),
#                     file_name=selected_media,
#                     mime='application/pdf',
#                 )
#             elif media_path.endswith(('.doc', '.docx')):
#                 st.download_button(
#                     label='Download Document',
#                     data=open(media_path, 'rb'),
#                     file_name=selected_media,
#                     mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
#                 )
#             else:
#                 st.write(f'File type not supported: {selected_media}')
#
# def unzip_folder(zip_file):
#     with zipfile.ZipFile(zip_file, 'r') as zip_ref:
#         zip_ref.extractall('unzipped_folder')


def unzip_folder(zip_file):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall('unzipped_folder')


def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()

    # Load the audio file using soundfile
    audio_data, sample_rate = sf.read(audio_path)

    # Convert the audio data to 16-bit PCM WAV format
    audio_data = (audio_data * 32767).astype(np.int16)

    audio_data = audio_data.tobytes()

    # Create an AudioData object directly
    audio = sr.AudioData(audio_data, sample_rate, 2)

    try:
        text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        text = "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        text = f"Could not request results from Google Speech Recognition service; {e}"

    return text

    return text
def main():
    st.title('Whatsapp Chat Media Analysis')

    # Upload zip file
    zip_file = st.file_uploader('Upload a zip file', type='zip')

    if zip_file:
        # Unzip the uploaded zip file
        unzip_folder(zip_file)

        # List all media files in the unzipped folder
        media_files = [f for f in os.listdir('unzipped_folder') if os.path.isfile(os.path.join('unzipped_folder', f))]

        # Display dropdown menu with media file options
        selected_media = st.selectbox('Select a media file', media_files)

        # Display the selected media file
        if selected_media:
            media_path = os.path.join('unzipped_folder', selected_media)
            if media_path.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                st.image(media_path)
            elif media_path.endswith(('.mp4', '.avi', '.mov')):
                st.video(media_path)
            elif media_path.endswith(('.mp3', '.ogg', '.opus')):
                st.audio(media_path, format='audio/ogg')
                if st.button("Transcribe Audio"):
                    text = transcribe_audio(media_path)
                    st.write("Transcribed Text:")
                    st.write(text)
            elif media_path.endswith('.pdf'):
                st.download_button(
                    label='Download PDF',
                    data=open(media_path, 'rb'),
                    file_name=selected_media,
                    mime='application/pdf',
                )
            elif media_path.endswith(('.doc', '.docx')):
                st.download_button(
                    label='Download Document',
                    data=open(media_path, 'rb'),
                    file_name=selected_media,
                    mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                )
            else:
                st.write(f'File type not supported: {selected_media}')
