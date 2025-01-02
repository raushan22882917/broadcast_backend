from youtube_transcript_api import YouTubeTranscriptApi

def fetch_transcript(video_url):
    video_id = extract_video_id(video_url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return [entry['text'] for entry in transcript]

def extract_video_id(url):
    import re
    match = re.search(r"v=([^&]+)", url)
    if match:
        return match.group(1)
    raise ValueError("Invalid YouTube URL")
