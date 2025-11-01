# YouTube Transcript Fetcher

A Python utility to fetch transcripts from YouTube videos and save them for AI analysis using ChatGPT or Claude.

## Features

- **Save transcripts to Downloads folder** - Ready to upload to ChatGPT or Claude
- **Multiple output formats** - Clean text, Markdown, or timestamped
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

### Quick Start - Save to Downloads for ChatGPT/Claude

The easiest way to use this tool is to save transcripts directly to your Downloads folder, ready to upload to ChatGPT or Claude:

#### Using the CLI Tool (Recommended)

```bash
# Download transcript to Downloads folder
python download_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Specify format (markdown is recommended for AI)
python download_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" --format markdown
```

#### Using Python

```python
from youtube_transcript import save_transcript_to_downloads

# Save transcript to Downloads folder (markdown format, perfect for AI)
file_path = save_transcript_to_downloads("https://www.youtube.com/watch?v=VIDEO_ID")
print(f"Saved to: {file_path}")

# Now you can:
# 1. Open the file in your Downloads folder
# 2. Upload it to ChatGPT or Claude
# 3. Ask questions about the video content!
```

### Basic Usage - Fetch Only

```python
from youtube_transcript import fetch_transcript

# Simple usage - get transcript as text
video_url = "https://www.youtube.com/watch?v=VIDEO_ID"
transcript_text = fetch_transcript(video_url)
print(transcript_text)
```

### Advanced Usage

#### Saving Transcripts with Different Formats

```python
from youtube_transcript import YouTubeTranscriptFetcher

fetcher = YouTubeTranscriptFetcher()

# Format options:
# - 'clean': Plain text, easy to read (default)
# - 'markdown': Formatted with paragraphs (RECOMMENDED for ChatGPT/Claude)
# - 'timestamped': Includes timestamps for reference

# Save as markdown (recommended)
path = fetcher.save_transcript(video_url, format_type='markdown')

# Save with custom filename and location
from pathlib import Path
path = fetcher.save_transcript(
    video_url,
    format_type='markdown',
    output_dir=Path.home() / "Documents",
    filename='my_video_transcript.md'
)
```

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

# Also works with save_transcript
path = save_transcript_to_downloads(video_url, languages=['en', 'es', 'fr'])
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

### Convenience Functions

#### `save_transcript_to_downloads(video_url, languages=['en'], format_type='markdown')`

Save transcript to Downloads folder, ready for ChatGPT/Claude.

**Parameters:**
- `video_url` (str): YouTube video URL or ID
- `languages` (List[str]): List of language codes to try (default: ['en'])
- `format_type` (str): 'clean', 'markdown', or 'timestamped' (default: 'markdown')

**Returns:** Path to saved file (str)

#### `fetch_transcript(video_url, languages=['en'])`

Fetch transcript as text.

**Parameters:**
- `video_url` (str): YouTube video URL or ID
- `languages` (List[str]): List of language codes to try (default: ['en'])

**Returns:** Full transcript as text string

### `YouTubeTranscriptFetcher` Class

#### Methods

##### `save_transcript(video_url, languages=['en'], format_type='clean', output_dir=None, filename=None)`

Fetch and save transcript to file.

**Parameters:**
- `video_url` (str): YouTube video URL or ID
- `languages` (List[str]): List of language codes to try (default: ['en'])
- `format_type` (str): 'clean', 'markdown', or 'timestamped'
- `output_dir` (Path, optional): Output directory (default: Downloads folder)
- `filename` (str, optional): Custom filename (default: auto-generated)

**Returns:** Path to saved file (str)

##### `get_transcript(video_url, languages=['en'])`

Get detailed transcript with timestamps.

**Returns:** List of dictionaries with 'text', 'start', and 'duration' keys

##### `get_transcript_text(video_url, languages=['en'])`

Get transcript as plain text string.

##### `list_available_transcripts(video_url)`

List all available transcripts for a video.

**Returns:** Dictionary with 'manual' and 'generated' transcript lists

##### `format_transcript_for_ai(video_url, transcript, format_type='clean', video_id=None)` (static)

Format transcript for AI analysis.

**Parameters:**
- `video_url` (str): YouTube video URL
- `transcript` (List[Dict]): List of transcript entries
- `format_type` (str): 'clean', 'markdown', or 'timestamped'
- `video_id` (str, optional): Video ID

**Returns:** Formatted transcript string

##### `get_downloads_folder()` (static)

Get path to Downloads folder (cross-platform).

**Returns:** Path object

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

## Output Formats

### Clean Text
Plain text format, all transcript text joined together. Easy to read and process.

### Markdown (Recommended for AI)
Formatted with paragraphs for better readability. Includes header with video metadata. Best for uploading to ChatGPT or Claude.

### Timestamped
Includes timestamps for each segment in `[MM:SS]` format. Useful when you need to reference specific parts of the video.

## Workflow for AI Analysis

1. **Download transcript:**
   ```bash
   python download_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"
   ```

2. **Find the file** in your Downloads folder (it will be named `youtube_transcript_VIDEO_ID_TIMESTAMP.md`)

3. **Upload to ChatGPT or Claude** and ask questions like:
   - "Summarize this video in 3 key points"
   - "What are the main topics discussed?"
   - "Create study notes from this transcript"
   - "Answer questions about [specific topic]"
   - "Extract action items or key takeaways"
   - "Explain [concept] mentioned in the video"

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
