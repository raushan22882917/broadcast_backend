from flask import Flask, request, jsonify, stream_with_context, Response
from utils.transcript_fetcher import fetch_transcript
from utils.live_transcript_stream import stream_live_transcript
from utils.fact_checker import fact_check

app = Flask(__name__)

@app.route('/api/transcript', methods=['GET'])
def get_transcript():
    video_url = request.args.get('videoUrl')
    if not video_url:
        return jsonify({"error": "Video URL is required"}), 400

    try:
        transcript = fetch_transcript(video_url)
        return jsonify({"transcripts": transcript})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/liveTranscript', methods=['GET'])
def get_live_transcript():
    video_url = request.args.get('videoUrl')
    if not video_url:
        return jsonify({"error": "Video URL is required"}), 400

    try:
        return Response(stream_with_context(stream_live_transcript(video_url)), content_type='text/event-stream')
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/factCheck', methods=['POST'])
def fact_check_transcript():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Transcript text is required"}), 400

    try:
        result = fact_check(data['text'])
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
