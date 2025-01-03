import requests

def fetch_transcript(video_id: str):
    """
    Fetches the transcript for a YouTube video using the SearchAPI.io service.

    Args:
        video_id (str): The YouTube video ID.

    Returns:
        list: A list containing transcript data.

    Raises:
        Exception: If an error occurs during the API call or processing.
    """
    url = "https://www.searchapi.io/api/v1/search"
    params = {
        "api_key": "VdwPw9NJxgp9VyDzjxd7o7rZ",  # API key
        "engine": "youtube_transcripts",  # Specific engine for YouTube video transcripts
        "video_id": video_id  # YouTube video ID
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract transcripts from the API response
        if "transcripts" in data:
            return data["transcripts"]
        else:
            raise Exception("Transcript not found in API response.")
    except requests.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")
