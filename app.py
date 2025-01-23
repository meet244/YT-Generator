import gradio as gr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os

load_dotenv()

if "GEMINI_API_KEY" not in os.environ:
    # ask user to provide API key
    api = input("\nPlease provide your Gemini API key: ")
    os.environ["GEMINI_API_KEY"] = api
    # save the API key to .env file
    try:
        with open(".env", "r+") as f:
            content = f.read()
            # Check if key exists but is empty
            if "GEMINI_API_KEY=" in content:
                # Replace empty key with new value
                new_content = content.replace("GEMINI_API_KEY=", f"GEMINI_API_KEY={api}")
                f.seek(0)
                f.write(new_content)
                f.truncate()
            else:
                # Append new key
                f.write(f"GEMINI_API_KEY={api}\n")
    except FileNotFoundError:
        with open(".env", "w") as f:
            f.write(f"GEMINI_API_KEY={api}\n")

def generate_content_from_url(yt_video_url):
    try:
        yt_video_id = YT_video_to_id(yt_video_url)
        transcript = YouTubeTranscriptApi.get_transcript(yt_video_id, languages=['en'])
        return process_transcript(transcript)
    except Exception as e:
        return f"An error occurred: {e}"

def generate_content_from_text(script_text):
    try:
        # Convert plain text to transcript-like format
        transcript = [{"text": script_text, "start": 0.0, "duration": 0.0}]
        return process_transcript(transcript)
    except Exception as e:
        return f"An error occurred: {e}"

def process_transcript(transcript):
    prompt = PromptTemplate(input_variables=["transcript"], template="""You are an AI content creator tasked with generating a compelling title, description, and timestamps for a YouTube video. The video transcript is provided in JSON format, with each item containing the spoken text, start time, and duration. Your goal is to create engaging and informative content that reflects the video's core message and encourages viewer engagement. Use the following guidelines to structure your output:

Analyze the following video transcript in JSON format to generate a compelling YouTube title, description, and detailed timestamps. Ensure the following:

Title:

Be concise (under 60 characters).
Reflect the video’s core content.
Use engaging and search-friendly language (numbers, emotional triggers, or strong verbs).
Avoid misleading or excessive clickbait.

Description:
Summarize the video’s content.
Include keywords for SEO optimization.
Mention resources, links, or highlights covered in the video.
Encourage viewers to engage (e.g., subscribe, like, comment).

Timestamps:
Identify sections by grouping similar topics.
Create clear and meaningful labels for each segment.
Ensure timestamps align with the start times in the JSON.
The input data will be in the following JSON format, where each item includes a text (spoken dialogue), start (timestamp in seconds), and duration (length of the spoken part):
3-6 timestamps are good for a 10-minute video.

[  
  ( "text": "...", "start": 0.0, "duration": 5.0 ),  
  ( "text": "...", "start": 5.0, "duration": 6.0 ),  
  ...  
]
Your output should be formatted as:

Title: [Generated title]
Description: [Generated description]
Timestamps:
00:00 - [Section 1 title]
00:05 - [Section 2 title]
…
Use an engaging tone and structure to maximize audience retention and interest.
Don't use buzz words or jargon that may confuse viewers.

Following is the transcript of the video:
{transcript}
""")

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5)
    chain = prompt | llm
    ans = chain.invoke(str(transcript))
    return ans.content

def YT_video_to_id(url):
    return url.split("v=")[-1].split("?")[0].split("/")[0]

with gr.Blocks(title="YouTube Title/Description/Timestamps Generator") as iface:
    gr.Markdown("# YouTube Title/Description/Timestamps Generator")
    gr.Markdown("Generate a compelling title, description, and timestamps using either a YouTube URL or direct script input.")
    
    with gr.Tab("From YouTube URL"):
        url_input = gr.Textbox(label="YouTube Video URL")
        url_button = gr.Button("Generate from URL")
        url_output = gr.Textbox(label="Generated Content", interactive=True)
        url_button.click(fn=generate_content_from_url, inputs=url_input, outputs=url_output)
    
    with gr.Tab("From Script"):
        text_input = gr.Textbox(label="Enter your script", lines=10)
        text_button = gr.Button("Generate from Script")
        text_output = gr.Textbox(label="Generated Content", interactive=True)
        text_button.click(fn=generate_content_from_text, inputs=text_input, outputs=text_output)

iface.launch()
