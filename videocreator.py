import os
from gtts import gTTS
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from dotenv import load_dotenv
import random
import os
import openai
from gtts import gTTS
from moviepy.editor import *
import moviepy.video.fx.crop as crop_vid
from langchain.llms import AzureOpenAI
import os
import openai
import requests
import streamlit as st
load_dotenv()





# Dummy path to the folder where images are stored
# folder_path = ''

def split_text(text, num_splits):
    
    
   

    # if text.endswith('.txt'):
    #     try:
    #         with open(text, 'r', encoding ='utf-8') as file:
    #             text = file.read()
    #             split_length = len(text) // int(num_splits)
    #             transcripts = [text[i:i+split_length] for i in range(0,len(text), split_length)]
    #             return transcripts
    #     except FileNotFoundError:
    #         print(f"Error: File '{input_text}' not found.")
    #         return
        
    # else:
        split_length = len(text) // int(num_splits)
        transcripts = [text[i:i+split_length] for i in range(0,len(text), split_length)]
        return transcripts
        

    


def image_gen(image_prompt, filename): #generates one image at a time
    file_path_i = f"generated_images/{filename}.png"
    openai.api_type = os.environ.get('OPENAI_API_TYPE')
    openai.api_version = os.environ.get('OPENAI_API_VERSION')
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    openai.api_base = os.environ.get('OPENAI_API_BASE')

    response = openai.Image.create(
    prompt=image_prompt,
    size='1024x1024',
    n=1
    )

    image_url = response["data"][0]["url"]
    img_data = requests.get(image_url).content
    with open(file_path_i, 'wb') as handler:
        handler.write(img_data)

def image_gen2(image_prompt, i): #for generating multiple images at one go
    file_path_i = f"generated_images/section{i+1}.png"
    openai.api_type = os.environ.get('OPENAI_API_TYPE')
    openai.api_version = os.environ.get('OPENAI_API_VERSION')
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    openai.api_base = os.environ.get('OPENAI_API_BASE')

    response = openai.Image.create(
    prompt=image_prompt,
    size='1024x1024',
    n=1
    )

    image_url = response["data"][0]["url"]
    img_data = requests.get(image_url).content
    with open(file_path_i, 'wb') as handler:
        handler.write(img_data)


     

def main():
    st.set_page_config(page_title="Video Creator", layout="wide")

    title = st.title("Video Creator")




    # Ensure the directory exists
    os.makedirs(folder_path, exist_ok=True)

    # List to hold individual video clips
    video_clips = []

    
    
    genvideo = st.button("Generate Video!")
    genimage = st.button("Generate Image!")
    stitchvideo = st.button("Stitch Video!")
    

    text = st.text_input('Please enter your prompt: ')
    num_splits = st.text_input('Please enter number of images: ')
    filename = st.text_input('Filename for Image: ')
    


    if stitchvideo: #create audio from existing script and stitch with existing images
        transcripts = split_text(text, num_splits)

        # Loop through each section and create a video
        for i, transcript in enumerate(transcripts):
            # Generate audio file using text-to-speech
            tts = gTTS(text=transcript, lang='en', tld='ca', slow= False)
            audio_file = os.path.join(folder_path, f"audio_section_{i+1}.mp3")
            tts.save(audio_file)

            # Generate images using Azure OpenAI Dall-E
            # image_gen(transcript, i)

            # Path to the image file
            image_file = os.path.join(folder_path, f"section{i+1}.png")

            # Create a video clip from the image and audio
            audio_clip = AudioFileClip(audio_file)
            video_clip = ImageClip(image_file).set_duration(audio_clip.duration).set_audio(audio_clip)
            video_clips.append(video_clip)

        # Combine all video clips into one video
        final_video = concatenate_videoclips(video_clips)

        # Save the final video
        final_video_file = os.path.join(folder_path, "final_video3.mp4")
        final_video.write_videofile(final_video_file, codec="libx264", fps=24)

    if genvideo: 
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        deployment_id = ''
        model_name = "text-davinci-003"
        llm = AzureOpenAI(deployment_name=deployment_id, model_name=model_name)
        text = llm(text)
        transcripts = split_text(text, num_splits)

        # Loop through each section and create a video
        for i, transcript in enumerate(transcripts):
            # Generate audio file using text-to-speech
            tts = gTTS(text=transcript, lang='en', tld='ca', slow= False)
            audio_file = os.path.join(folder_path, f"audio_section_{i+1}.mp3")
            tts.save(audio_file)

            #Generate images using Azure OpenAI Dall-E
            image_gen2(transcript, i)

            # Path to the image file
            image_file = os.path.join(folder_path, f"section{i+1}.png")

            # Create a video clip from the image and audio
            audio_clip = AudioFileClip(audio_file)
            video_clip = ImageClip(image_file).set_duration(audio_clip.duration).set_audio(audio_clip)
            video_clips.append(video_clip)

        # Combine all video clips into one video
        final_video = concatenate_videoclips(video_clips)

        # Save the final video
        final_video_file = os.path.join(folder_path, "final_video3.mp4")
        final_video.write_videofile(final_video_file, codec="libx264", fps=24)


    if genimage: #for generating one image at a time
        image_gen(text, filename)


    
    

    


if __name__ == "__main__":
    main()



