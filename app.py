from flask import Flask, request, jsonify, stream_with_context, Response
from utils.transcript_fetcher import fetch_transcript
from utils.fact_checker import fact_check
from utils.kafka_producer import produce_to_kafka
from utils.kafka_consumer import consume_from_kafka

app = Flask(__name__)

@app.route('/api/transcript', methods=['GET'])
def get_transcript():
    """
    Fetch the transcript for a given video URL.
    """
    video_url = request.args.get('videoUrl')
    if not video_url:
        return jsonify({"error": "Video URL is required"}), 400

    try:
        transcript = fetch_transcript(video_url)
        return jsonify({"transcripts": transcript}), 200
    except Exception as e:
        app.logger.error(f"Error fetching transcript: {e}")
        return jsonify({"error": "Failed to fetch transcript"}), 500


@app.route('/api/liveTranscript', methods=['GET'])
def get_live_transcript():
    """
    Stream live transcripts from Kafka.
    """
    topic = request.args.get('topic', 'live_transcripts')

    try:
        return Response(
            stream_with_context(consume_from_kafka(topic)),
            content_type='text/event-stream'
        )
    except Exception as e:
        app.logger.error(f"Error consuming live transcript: {e}")
        return jsonify({"error": "Failed to stream live transcript"}), 500


@app.route('/api/sendLiveTranscript', methods=['POST'])
def send_live_transcript():
    """
    Send live transcript text to Kafka.
    """
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Live transcript text is required"}), 400

    try:
        topic = data.get('topic', 'live_transcripts')
        produce_to_kafka(topic, data['text'])
        return jsonify({"message": "Live transcript sent to Kafka"}), 200
    except Exception as e:
        app.logger.error(f"Error sending live transcript: {e}")
        return jsonify({"error": "Failed to send live transcript"}), 500


@app.route('/api/factCheck', methods=['POST'])
def fact_check_transcript():
    """
    Perform fact-checking on a given transcript text.
    """
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Transcript text is required"}), 400

    try:
        checked_text = fact_check(data['text'])
        return jsonify({"checkedText": checked_text}), 200
    except Exception as e:
        app.logger.error(f"Error fact-checking transcript: {e}")
        return jsonify({"error": "Failed to perform fact-checking"}), 500


if __name__ == '__main__':
    app.run(debug=True)
