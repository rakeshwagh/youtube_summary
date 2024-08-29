from youtube_transcript_api import YouTubeTranscriptApi
import re

# Function to extract video ID from a YouTube URL
def extract_video_id(youtube_url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, youtube_url)
    
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

def get_youtube_transcript(youtube_url):
    try:
        video_id = extract_video_id(youtube_url)
        
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        transcript_text = " ".join([item['text'] for item in transcript])
        return transcript_text
    
    except Exception as e:
        return str(e)
