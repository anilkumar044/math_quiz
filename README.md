# YouTube Transcript Fetcher

A Python utility to fetch transcripts from YouTube videos using the `youtube-transcript-api` library.

## Features

- Fetch transcripts from YouTube videos using video URL or ID
- Support for multiple URL formats (youtube.com, youtu.be, embed, direct ID)
- Multiple language support with fallback options
- Get detailed transcripts with timestamps or plain text
- List all available transcripts for a video (manual and auto-generated)
- Comprehensive error handling

## Installation

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

```python
from youtube_transcript import fetch_transcript

# Simple usage - get transcript as text
video_url = "https://www.youtube.com/watch?v=VIDEO_ID"
transcript_text = fetch_transcript(video_url)
print(transcript_text)
```

### Advanced Usage

#### Get Detailed Transcript with Timestamps

```python
from youtube_transcript import YouTubeTranscriptFetcher

fetcher = YouTubeTranscriptFetcher()
transcript = fetcher.get_transcript(video_url)

for entry in transcript:
    print(f"[{entry['start']:.2f}s] {entry['text']}")
```

#### Multiple Language Support

```python
# Try English first, then Spanish, then French
transcript = fetcher.get_transcript_text(
    video_url,
    languages=['en', 'es', 'fr']
)
```

#### List Available Transcripts

```python
available = fetcher.list_available_transcripts(video_url)

print("Manual transcripts:", available['manual'])
print("Generated transcripts:", available['generated'])
```

#### Extract Video ID

```python
# Supports multiple formats
video_id = YouTubeTranscriptFetcher.extract_video_id("https://www.youtube.com/watch?v=VIDEO_ID")
video_id = YouTubeTranscriptFetcher.extract_video_id("https://youtu.be/VIDEO_ID")
video_id = YouTubeTranscriptFetcher.extract_video_id("VIDEO_ID")
```

## Examples

Run the example script to see all features in action:

```bash
python example.py
```

## API Reference

### `fetch_transcript(video_url, languages=['en'])`

Convenience function to fetch transcript as text.

**Parameters:**
- `video_url` (str): YouTube video URL or ID
- `languages` (List[str]): List of language codes to try (default: ['en'])

**Returns:** Full transcript as text string

### `YouTubeTranscriptFetcher` Class

#### Methods

##### `get_transcript(video_url, languages=['en'])`

Get detailed transcript with timestamps.

**Returns:** List of dictionaries with 'text', 'start', and 'duration' keys

##### `get_transcript_text(video_url, languages=['en'])`

Get transcript as plain text string.

##### `list_available_transcripts(video_url)`

List all available transcripts for a video.

**Returns:** Dictionary with 'manual' and 'generated' transcript lists

##### `extract_video_id(url)` (static)

Extract video ID from various YouTube URL formats.

## Error Handling

The module raises specific exceptions:

- `ValueError`: Invalid video URL or ID
- `TranscriptsDisabled`: Transcripts are disabled for the video
- `NoTranscriptFound`: No transcript found in requested languages
- `VideoUnavailable`: Video is unavailable

Example:

```python
try:
    transcript = fetch_transcript(video_url)
except ValueError as e:
    print(f"Invalid URL: {e}")
except TranscriptsDisabled:
    print("Transcripts are disabled for this video")
except NoTranscriptFound:
    print("No transcript available in requested language")
except VideoUnavailable:
    print("Video is unavailable")
```

## Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- `https://www.youtube.com/v/VIDEO_ID`
- `VIDEO_ID` (direct video ID)

## Language Codes

Common language codes:
- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `it` - Italian
- `pt` - Portuguese
- `ru` - Russian
- `ja` - Japanese
- `ko` - Korean
- `zh` - Chinese

## License

This project uses the `youtube-transcript-api` library.

## Notes

- Not all YouTube videos have transcripts available
- Some videos only have auto-generated transcripts
- Transcripts may not be available in all languages
- The API fetches publicly available transcript data
