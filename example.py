"""
Example usage of YouTube Transcript Fetcher

This script demonstrates how to use the youtube_transcript module.
"""

from youtube_transcript import YouTubeTranscriptFetcher, fetch_transcript


def example_basic_usage():
    """Example: Basic transcript fetching"""
    print("=" * 60)
    print("Example 1: Basic Transcript Fetching")
    print("=" * 60)

    # Example video URL (replace with actual YouTube URL)
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    try:
        # Simple way: Get transcript as text
        transcript_text = fetch_transcript(video_url)
        print(f"\nTranscript length: {len(transcript_text)} characters")
        print(f"\nFirst 200 characters:\n{transcript_text[:200]}...")
    except Exception as e:
        print(f"\nError: {e}")


def example_detailed_transcript():
    """Example: Get detailed transcript with timestamps"""
    print("\n" + "=" * 60)
    print("Example 2: Detailed Transcript with Timestamps")
    print("=" * 60)

    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    try:
        fetcher = YouTubeTranscriptFetcher()
        transcript = fetcher.get_transcript(video_url)

        print(f"\nTotal segments: {len(transcript)}")
        print("\nFirst 5 segments:")

        for i, entry in enumerate(transcript[:5]):
            print(f"\n[{i+1}] Time: {entry['start']:.2f}s")
            print(f"    Duration: {entry['duration']:.2f}s")
            print(f"    Text: {entry['text']}")
    except Exception as e:
        print(f"\nError: {e}")


def example_list_available_transcripts():
    """Example: List all available transcripts for a video"""
    print("\n" + "=" * 60)
    print("Example 3: List Available Transcripts")
    print("=" * 60)

    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    try:
        fetcher = YouTubeTranscriptFetcher()
        available = fetcher.list_available_transcripts(video_url)

        print("\nManual transcripts:")
        for transcript in available['manual']:
            print(f"  - {transcript['language']} ({transcript['language_code']})")

        print("\nGenerated transcripts:")
        for transcript in available['generated']:
            print(f"  - {transcript['language']} ({transcript['language_code']})")
    except Exception as e:
        print(f"\nError: {e}")


def example_multiple_languages():
    """Example: Try multiple languages"""
    print("\n" + "=" * 60)
    print("Example 4: Multiple Language Support")
    print("=" * 60)

    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    try:
        # Try English first, fall back to Spanish, then French
        fetcher = YouTubeTranscriptFetcher()
        transcript_text = fetcher.get_transcript_text(video_url, languages=['en', 'es', 'fr'])
        print(f"\nSuccessfully fetched transcript!")
        print(f"Length: {len(transcript_text)} characters")
    except Exception as e:
        print(f"\nError: {e}")


def example_video_id_formats():
    """Example: Different URL formats"""
    print("\n" + "=" * 60)
    print("Example 5: Different URL Format Support")
    print("=" * 60)

    fetcher = YouTubeTranscriptFetcher()

    urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "dQw4w9WgXcQ",
        "https://www.youtube.com/embed/dQw4w9WgXcQ"
    ]

    for url in urls:
        video_id = fetcher.extract_video_id(url)
        print(f"\nURL: {url}")
        print(f"Extracted ID: {video_id}")


if __name__ == "__main__":
    print("\nYouTube Transcript Fetcher - Examples\n")

    # Run examples
    example_video_id_formats()
    example_basic_usage()
    example_detailed_transcript()
    example_list_available_transcripts()
    example_multiple_languages()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
