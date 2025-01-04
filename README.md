
# 📹 YouTube Title/Description/Timestamps Generator

This is a web-based tool that generates a **compelling title, description, and timestamps** for YouTube videos based on their transcripts. The application uses Google Gemini API (via `langchain_google_genai`) to process the video transcript and create engaging and informative content that maximizes audience engagement.

---

## ✨ Features
- 📝 **Title Generation**: Create concise, search-friendly, and engaging titles.
- 🔍 **Description Generation**: Write SEO-optimized descriptions with relevant resources and engagement prompts.
- ⏱️ **Timestamps Generation**: Identify meaningful segments in the video and label them with clear, structured timestamps.

---

## ⚙️ How It Works
1. 🔑 Provide your **Google Gemini API Key**.
2. 🌐 Enter the **YouTube video URL**.
3. 📜 The app fetches the video transcript using the `YouTubeTranscriptApi`.
4. 🛠️ The transcript is processed to generate a **title**, **description**, and **timestamps**.

---

## 🛠️ Installation and Setup

### 📋 Prerequisites
- 🐍 Python 3.8 or higher
- Install required dependencies:
  ```bash
  pip install gradio langchain_google_genai youtube-transcript-api
  ```

### 📂 Clone the Repository
```bash
git clone https://github.com/yourusername/youtube-content-generator.git
cd youtube-content-generator
```

### 🔧 Environment Setup
1. Set up your Google Gemini API access and obtain an API key.
2. (Optional) Use a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

---

## 🚀 Usage
1. Run the app:
   ```bash
   python app.py
   ```
2. Open the app in your browser (default: `http://127.0.0.1:7860`).
3. Enter your **Gemini API Key** and **YouTube Video URL**.
4. 📋 View the generated content.

---

## 📊 Example Input/Output

### Input:
- 🔑 API Key: `<Your Google Gemini API Key>`
- 🔗 YouTube Video URL: `https://www.youtube.com/watch?v=example_video_id`

### Output:
```
Title: 10 Tips for Productive Remote Work
Description: Learn the top 10 strategies for staying productive while working remotely. This video covers time management, work-life balance, and tools to enhance your efficiency. Don't forget to like, comment, and subscribe!
Timestamps:
00:00 - Introduction
00:30 - Tip 1: Setting a Schedule
01:15 - Tip 2: Workspace Optimization
...
```

---

## ❗ Error Handling
- ⚠️ If the YouTube video does not have a transcript or if the provided URL is invalid, the app will display an appropriate error message.

---

## 🛠️ Technologies Used
- 💻 **Gradio**: For building the user interface.
- 🤖 **LangChain Google GenAI**: For leveraging Google Gemini to process and generate content.
- 📜 **YouTube Transcript API**: For fetching video transcripts.

---

## 🤝 Contribution
Contributions are welcome! Please open an issue or submit a pull request.

---
