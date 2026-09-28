import logging
from typing import Optional, List, Dict, Any
import google.genai as genai
from google.genai import types
from app.config import settings

logger = logging.getLogger(__name__)

class GeminiService:
    @staticmethod
    def get_client(api_key: Optional[str] = None) -> genai.Client:
        key = (api_key or "").strip() or settings.GEMINI_API_KEY.strip()
        if not key or key == "your_gemini_api_key_here":
            raise ValueError(
                "Gemini API Key is not configured. Please add GEMINI_API_KEY to your .env file "
                "or set it in the Settings page."
            )
        return genai.Client(api_key=key)

    @classmethod
    def verify_api_key(cls, api_key: Optional[str] = None) -> Dict[str, Any]:
        """Test if the API key is valid by querying the Gemini API."""
        try:
            client = cls.get_client(api_key)
            # Fetch at least one model to verify authentication
            pager = client.models.list()
            sample_model = None
            for model in pager:
                sample_model = model.name
                break
            return {
                "valid": True,
                "message": "Successfully connected to Google Gemini API!",
                "sample_model": sample_model
            }
        except ValueError as ve:
            return {"valid": False, "message": str(ve)}
        except Exception as e:
            logger.error(f"API key verification failed: {e}")
            return {"valid": False, "message": f"Connection failed: {str(e)}"}

    @classmethod
    def generate_chat_response(
        cls,
        messages: List[Dict[str, str]],
        system_instruction: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        api_key: Optional[str] = None
    ) -> str:
        """
        Generate chat response for multi-turn conversation.
        messages format: [{'role': 'user'|'model', 'content': '...'}]
        """
        client = cls.get_client(api_key)
        selected_model = model or settings.DEFAULT_MODEL

        # Convert to google.genai Content objects
        formatted_contents = []
        for msg in messages:
            role = "model" if msg.get("role") in ["assistant", "model"] else "user"
            text = msg.get("content", "")
            formatted_contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=text)]
                )
            )

        config = types.GenerateContentConfig(
            temperature=temperature,
            system_instruction=system_instruction or "You are a helpful, brilliant, and polite AI assistant."
        )

        response = client.models.generate_content(
            model=selected_model,
            contents=formatted_contents,
            config=config
        )
        return response.text or "No response generated."

    @classmethod
    def analyze_image(
        cls,
        image_bytes: bytes,
        mime_type: str,
        prompt: str,
        model: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> str:
        """Analyze an image with multimodal Gemini."""
        client = cls.get_client(api_key)
        selected_model = model or settings.DEFAULT_MODEL

        image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
        text_part = types.Part.from_text(text=prompt or "Analyze and describe this image in detail.")

        content = types.Content(
            role="user",
            parts=[image_part, text_part]
        )

        response = client.models.generate_content(
            model=selected_model,
            contents=[content]
        )
        return response.text or "No analysis generated."

    @classmethod
    def process_code(
        cls,
        code: str,
        action: str,
        language: str = "python",
        model: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> str:
        """Explain, debug, optimize, or write unit tests for code snippet."""
        prompts = {
            "explain": f"Explain the following {language} code step by step clearly with bullet points and key concepts:\n\n```{language}\n{code}\n```",
            "debug": f"Find bugs, potential edge cases, security risks, or logic errors in this {language} code and provide the corrected version:\n\n```{language}\n{code}\n```",
            "optimize": f"Optimize the following {language} code for better performance, time/space complexity, and clean code principles. Explain your optimizations:\n\n```{language}\n{code}\n```",
            "test": f"Write comprehensive, clean unit tests for the following {language} code snippet:\n\n```{language}\n{code}\n```",
            "refactor": f"Refactor this {language} code to be more idiomatic, readable, and maintainable following standard design patterns:\n\n```{language}\n{code}\n```"
        }
        prompt_text = prompts.get(action, prompts["explain"])
        system_prompt = f"You are a principal software engineer and expert in {language}. Provide accurate, high quality, production-grade advice with clear Markdown formatting."

        return cls.generate_chat_response(
            messages=[{"role": "user", "content": prompt_text}],
            system_instruction=system_prompt,
            model=model,
            temperature=0.3,
            api_key=api_key
        )

    @classmethod
    def summarize_text(
        cls,
        text: str,
        style: str = "bullets",
        length: str = "medium",
        model: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> str:
        """Summarize text according to specified style and length."""
        style_instructions = {
            "bullets": "Summarize the key points as clear, impactful bullet points.",
            "executive": "Write an executive summary suitable for leadership and stakeholders.",
            "tldr": "Provide a quick 2-3 sentence TL;DR followed by top 3 takeaways.",
            "actionable": "Extract actionable items, tasks, and recommendations from the text.",
            "simplified": "Explain and summarize the content in simple terms as if explaining to a beginner."
        }
        length_guide = {
            "short": "Keep it concise (100-150 words).",
            "medium": "Provide balanced depth (200-300 words).",
            "long": "Provide a comprehensive, detailed breakdown."
        }

        instruction = f"{style_instructions.get(style, style_instructions['bullets'])} {length_guide.get(length, length_guide['medium'])}"
        prompt = f"{instruction}\n\nContent to summarize:\n\"\"\"\n{text}\n\"\"\""

        return cls.generate_chat_response(
            messages=[{"role": "user", "content": prompt}],
            system_instruction="You are an expert editor and synthesizer of complex information. Present findings clearly.",
            model=model,
            temperature=0.4,
            api_key=api_key
        )
