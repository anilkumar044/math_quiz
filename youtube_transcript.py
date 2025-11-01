"""
YouTube Transcript Fetcher

This module provides functionality to fetch transcripts from YouTube videos.
"""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from typing import List, Dict, Optional
import re
import os
from pathlib import Path
from datetime import datetime


class YouTubeTranscriptFetcher:
    """
    A class to fetch and process YouTube video transcripts.
    """

    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """
        Extract video ID from various YouTube URL formats.

        Args:
            url: YouTube URL or video ID

        Returns:
            Video ID if found, None otherwise

        Examples:
            - https://www.youtube.com/watch?v=VIDEO_ID
            - https://youtu.be/VIDEO_ID
            - VIDEO_ID (direct)
        """
        # If it's already a video ID (11 characters, alphanumeric with dashes/underscores)
        if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
            return url

        # Extract from standard YouTube URL
        patterns = [
            r'(?:youtube\.com\/watch\?v=)([a-zA-Z0-9_-]{11})',
            r'(?:youtu\.be\/)([a-zA-Z0-9_-]{11})',
            r'(?:youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
            r'(?:youtube\.com\/v\/)([a-zA-Z0-9_-]{11})'
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return None

    @staticmethod
    def get_transcript(video_url: str, languages: List[str] = ['en']) -> List[Dict]:
        """
        Fetch transcript for a YouTube video.

        Args:
            video_url: YouTube video URL or video ID
            languages: List of language codes to try (default: ['en'])

        Returns:
            List of transcript entries with 'text', 'start', and 'duration'

        Raises:
            ValueError: If video ID cannot be extracted
            TranscriptsDisabled: If transcripts are disabled for the video
            NoTranscriptFound: If no transcript is found in requested languages
            VideoUnavailable: If video is unavailable
        """
        video_id = YouTubeTranscriptFetcher.extract_video_id(video_url)

        if not video_id:
            raise ValueError(f"Could not extract video ID from: {video_url}")

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            return transcript
        except TranscriptsDisabled:
            raise TranscriptsDisabled(f"Transcripts are disabled for video: {video_id}")
        except NoTranscriptFound:
            raise NoTranscriptFound(
                f"No transcript found for video: {video_id} in languages: {languages}"
            )
        except VideoUnavailable:
            raise VideoUnavailable(f"Video unavailable: {video_id}")

    @staticmethod
    def get_transcript_text(video_url: str, languages: List[str] = ['en']) -> str:
        """
        Fetch transcript and return as a single text string.

        Args:
            video_url: YouTube video URL or video ID
            languages: List of language codes to try (default: ['en'])

        Returns:
            Full transcript text
        """
        transcript = YouTubeTranscriptFetcher.get_transcript(video_url, languages)
        return ' '.join([entry['text'] for entry in transcript])

    @staticmethod
    def list_available_transcripts(video_url: str) -> Dict:
        """
        List all available transcripts for a video.

        Args:
            video_url: YouTube video URL or video ID

        Returns:
            Dictionary with manually created and generated transcripts
        """
        video_id = YouTubeTranscriptFetcher.extract_video_id(video_url)

        if not video_id:
            raise ValueError(f"Could not extract video ID from: {video_url}")

        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            result = {
                'manual': [],
                'generated': []
            }

            for transcript in transcript_list:
                info = {
                    'language': transcript.language,
                    'language_code': transcript.language_code,
                    'is_translatable': transcript.is_translatable
                }

                if transcript.is_generated:
                    result['generated'].append(info)
                else:
                    result['manual'].append(info)

            return result
        except Exception as e:
            raise e

    @staticmethod
    def get_downloads_folder() -> Path:
        """
        Get the path to the Downloads folder (cross-platform).

        Returns:
            Path to Downloads folder
        """
        home = Path.home()
        downloads = home / "Downloads"

        # Create Downloads folder if it doesn't exist
        downloads.mkdir(exist_ok=True)

        return downloads

    @staticmethod
    def format_transcript_for_ai(
        video_url: str,
        transcript: List[Dict],
        format_type: str = 'clean',
        video_id: str = None
    ) -> str:
        """
        Format transcript for AI analysis (ChatGPT, Claude, etc.).

        Args:
            video_url: YouTube video URL
            transcript: List of transcript entries
            format_type: Format type - 'clean', 'markdown', or 'timestamped'
            video_id: Video ID (optional, will be extracted if not provided)

        Returns:
            Formatted transcript string
        """
        if not video_id:
            video_id = YouTubeTranscriptFetcher.extract_video_id(video_url)

        # Header
        header = f"YouTube Video Transcript\n"
        header += f"{'=' * 60}\n"
        header += f"Video ID: {video_id}\n"
        header += f"Video URL: https://www.youtube.com/watch?v={video_id}\n"
        header += f"Downloaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        header += f"{'=' * 60}\n\n"

        if format_type == 'clean':
            # Plain text, optimized for AI reading
            content = ' '.join([entry['text'] for entry in transcript])
            return header + content

        elif format_type == 'markdown':
            # Markdown format with paragraphs
            content = "# Transcript\n\n"
            paragraphs = []
            current_paragraph = []

            for entry in transcript:
                current_paragraph.append(entry['text'])
                # Start new paragraph after ~200 characters or at sentence end
                if len(' '.join(current_paragraph)) > 200 and entry['text'].rstrip().endswith(('.', '!', '?')):
                    paragraphs.append(' '.join(current_paragraph))
                    current_paragraph = []

            if current_paragraph:
                paragraphs.append(' '.join(current_paragraph))

            content += '\n\n'.join(paragraphs)
            return header + content

        elif format_type == 'timestamped':
            # Include timestamps for reference
            content = "# Transcript with Timestamps\n\n"
            for entry in transcript:
                timestamp = f"[{int(entry['start'] // 60):02d}:{int(entry['start'] % 60):02d}]"
                content += f"{timestamp} {entry['text']}\n"

            return header + content

        else:
            raise ValueError(f"Unknown format_type: {format_type}. Use 'clean', 'markdown', or 'timestamped'")

    @staticmethod
    def save_transcript(
        video_url: str,
        languages: List[str] = ['en'],
        format_type: str = 'clean',
        output_dir: Optional[Path] = None,
        filename: Optional[str] = None
    ) -> str:
        """
        Fetch transcript and save to Downloads folder (or specified directory).

        Args:
            video_url: YouTube video URL or video ID
            languages: List of language codes to try (default: ['en'])
            format_type: Format type - 'clean', 'markdown', or 'timestamped'
            output_dir: Output directory (default: Downloads folder)
            filename: Custom filename (default: auto-generated from video ID)

        Returns:
            Path to saved file

        Example:
            >>> path = YouTubeTranscriptFetcher.save_transcript(
            ...     "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            ...     format_type='markdown'
            ... )
            >>> print(f"Saved to: {path}")
        """
        # Get video ID
        video_id = YouTubeTranscriptFetcher.extract_video_id(video_url)
        if not video_id:
            raise ValueError(f"Could not extract video ID from: {video_url}")

        # Fetch transcript
        transcript = YouTubeTranscriptFetcher.get_transcript(video_url, languages)

        # Format transcript
        formatted_content = YouTubeTranscriptFetcher.format_transcript_for_ai(
            video_url, transcript, format_type, video_id
        )

        # Determine output directory
        if output_dir is None:
            output_dir = YouTubeTranscriptFetcher.get_downloads_folder()
        else:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

        # Determine filename
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            extension = 'md' if format_type == 'markdown' else 'txt'
            filename = f"youtube_transcript_{video_id}_{timestamp}.{extension}"

        # Save file
        output_path = output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_content)

        return str(output_path)


def fetch_transcript(video_url: str, languages: List[str] = ['en']) -> str:
    """
    Convenience function to fetch YouTube transcript as text.

    Args:
        video_url: YouTube video URL or video ID
        languages: List of language codes to try (default: ['en'])

    Returns:
        Full transcript text
    """
    fetcher = YouTubeTranscriptFetcher()
    return fetcher.get_transcript_text(video_url, languages)


def save_transcript_to_downloads(
    video_url: str,
    languages: List[str] = ['en'],
    format_type: str = 'markdown'
) -> str:
    """
    Convenience function to save YouTube transcript to Downloads folder.
    Optimized for uploading to ChatGPT or Claude for analysis.

    Args:
        video_url: YouTube video URL or video ID
        languages: List of language codes to try (default: ['en'])
        format_type: Format type - 'clean', 'markdown', or 'timestamped' (default: 'markdown')

    Returns:
        Path to saved file

    Example:
        >>> path = save_transcript_to_downloads("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        >>> print(f"Transcript saved to: {path}")
        >>> print("Now you can upload this file to ChatGPT or Claude!")
    """
    return YouTubeTranscriptFetcher.save_transcript(
        video_url=video_url,
        languages=languages,
        format_type=format_type
    )
