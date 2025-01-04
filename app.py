import gradio as gr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi
import os

def generate_content(api_key, yt_video_url):
    os.environ["GOOGLE_API_KEY"] = api_key

    prompt = PromptTemplate(input_variables="transcript", template="""You are an AI content creator tasked with generating a compelling title, description, and timestamps for a YouTube video. The video transcript is provided in JSON format, with each item containing the spoken text, start time, and duration. Your goal is to create engaging and informative content that reflects the video's core message and encourages viewer engagement. Use the following guidelines to structure your output:

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

Following is the transcript of the video:
{transcript}
""")

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.1)

    yt_video_id = YT_video_to_id(yt_video_url)

    try:
        transcript = YouTubeTranscriptApi.get_transcript(yt_video_id, languages=['en'])
        prompt.format(transcript=transcript)
        chain = prompt | llm
        ans = chain.invoke(str(transcript))
        return ans.content
    except Exception as e:
        return f"An error occurred: {e}"

def YT_video_to_id(url):
    return url.split("v=")[-1].split("?")[0].split("/")[0]

iface = gr.Interface(
    fn=generate_content,
    inputs=[
        gr.Textbox(label="Gemini API Key"),
        gr.Textbox(label="YouTube Video URL")
    ],
    outputs=gr.Textbox(label="Generated Content", interactive=True),
    title="YouTube Title/Description/Timestamps Generator",
    description="Generate a compelling title, description, and timestamps for a YouTube video using its transcript."
)

iface.launch()
