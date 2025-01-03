import time
from pylivestream import Livestream

def stream_live_transcript(video_url):
    # Extract video ID from the URL
    video_id = extract_video_id(video_url)

    # Set up pylivestream and connect to YouTube live video
    live_stream = Livestream(video_id)
    
    try:
        # Start the live stream
        live_stream.start()

        # Keep fetching live transcript (in a real-world case, you would use YouTube's live captions API)
        while True:
            caption = live_stream.get_current_caption()  # You need to implement fetching captions here
            if caption:
                yield f"{time.ctime()}: {caption}\n"
            time.sleep(2)  # Simulate a delay between captions
    except Exception as e:
        yield f"Error: {str(e)}"
    finally:
        live_stream.stop()

def extract_video_id(url):
    import re
    match = re.search(r"v=([^&]+)", url)
    if match:
        return match.group(1)
    raise ValueError("Invalid YouTube URL")
