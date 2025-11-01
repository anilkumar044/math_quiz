#!/usr/bin/env python3
"""
Simple CLI tool to download YouTube transcripts to Downloads folder.
Optimized for uploading to ChatGPT or Claude for analysis.

Usage:
    python download_transcript.py <youtube_url>
    python download_transcript.py <youtube_url> --format markdown
    python download_transcript.py <youtube_url> --format timestamped
"""

import sys
from youtube_transcript import save_transcript_to_downloads


def main():
    if len(sys.argv) < 2:
        print("YouTube Transcript Downloader")
        print("=" * 60)
        print("\nUsage:")
        print("  python download_transcript.py <youtube_url>")
        print("  python download_transcript.py <youtube_url> --format <type>")
        print("\nFormats:")
        print("  clean       - Plain text (default)")
        print("  markdown    - Formatted with paragraphs (recommended for AI)")
        print("  timestamped - Includes timestamps")
        print("\nExamples:")
        print("  python download_transcript.py https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print("  python download_transcript.py https://youtu.be/dQw4w9WgXcQ --format markdown")
        print("\nThe transcript will be saved to your Downloads folder.")
        print("You can then upload it to ChatGPT or Claude for analysis!")
        print("=" * 60)
        sys.exit(1)

    video_url = sys.argv[1]
    format_type = 'markdown'  # Default format

    # Check if format is specified
    if len(sys.argv) > 2 and sys.argv[2] == '--format' and len(sys.argv) > 3:
        format_type = sys.argv[3]

    print("\nYouTube Transcript Downloader")
    print("=" * 60)
    print(f"Video URL: {video_url}")
    print(f"Format: {format_type}")
    print("\nDownloading transcript...")

    try:
        file_path = save_transcript_to_downloads(video_url, format_type=format_type)

        print("\n" + "=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print(f"\nTranscript saved to:")
        print(f"  {file_path}")
        print("\nNext steps:")
        print("  1. Open the file in your Downloads folder")
        print("  2. Upload it to ChatGPT or Claude")
        print("  3. Ask questions like:")
        print("     - 'Summarize this video'")
        print("     - 'What are the key points?'")
        print("     - 'Create study notes from this'")
        print("     - 'Answer questions about [topic]'")
        print("=" * 60)

    except Exception as e:
        print("\n" + "=" * 60)
        print("ERROR")
        print("=" * 60)
        print(f"\n{str(e)}")
        print("\nCommon issues:")
        print("  - Video may not have captions/transcripts available")
        print("  - Invalid video URL or ID")
        print("  - Network connection issues")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
