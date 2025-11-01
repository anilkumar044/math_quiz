"""
YouTube Transcript Fetcher

This module provides functionality to fetch transcripts from YouTube videos.
"""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from typing import List, Dict, Optional
import re


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
