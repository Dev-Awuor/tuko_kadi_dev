"""Gemini Vision tool for analyzing political posters and images."""

from google import genai
from google.genai import types as genai_types
from src.config import get_settings
import logging

logger = logging.getLogger(__name__)

async def analyze_political_image(image_url: str) -> str:
    """Analyze an image of a political poster or news clip for claims.
    
    Args:
        image_url: The URL of the image to analyze.
    
    Returns:
        The text extracted and a preliminary fact-check.
    """
    try:
        client = genai.Client(vertexai=True)
        
        # In a real AT workflow, we would download the image from image_url
        # For this tool definition, we describe how Gemini Vision would process it.
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                "Extract any text and political claims from this image. Then, provide a factual correction for any misinformation detected.",
                genai_types.Part.from_uri(file_uri=image_url, mime_type="image/jpeg")
            ]
        )
        
        return response.text
        
    except Exception as e:
        logger.error(f"Gemini Vision analysis failed: {e}")
        return "I could not analyze the image provided. Please describe the text in the image instead."
