"""
LLM Router - Provider-agnostic LLM interface
Supports both Groq and OpenRouter APIs
"""

import os
from typing import Dict, Optional, Any
import json
import logging

# Try importing both clients
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

logger = logging.getLogger(__name__)


class LLMRouter:
    """
    Router for LLM API calls
    Supports Groq and OpenRouter with automatic fallback
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[float] = None
    ):
        """
        Initialize LLM router

        Args:
            api_key: API key (reads from env if not provided)
            provider: 'groq' or 'openrouter' (auto-detects from env if not provided)
            model: Model name (uses default from constants if not provided)
            timeout: Request timeout in seconds (default: 120s)
        """
        # Determine provider
        self.provider = provider or os.getenv("LLM_PROVIDER", "openrouter")
        self.timeout = timeout or float(os.getenv("LLM_TIMEOUT", "120"))

        logger.info(f"Initializing LLM router with provider: {self.provider}, timeout: {self.timeout}s")

        if self.provider == "groq":
            if not GROQ_AVAILABLE:
                raise ImportError("Groq SDK not installed. Run: pip install groq")

            self.api_key = api_key or os.getenv("GROQ_API_KEY")
            if not self.api_key:
                logger.error("GROQ_API_KEY not found in environment")
                raise ValueError("GROQ_API_KEY not found in environment. Please set it in your .env file.")

            self.client = Groq(api_key=self.api_key, timeout=self.timeout)
            self.model = model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
            logger.info(f"Using Groq with model: {self.model}")

        elif self.provider == "openrouter":
            if not OPENAI_AVAILABLE:
                raise ImportError("OpenAI SDK not installed. Run: pip install openai")

            self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
            if not self.api_key:
                logger.error("OPENROUTER_API_KEY not found in environment")
                raise ValueError("OPENROUTER_API_KEY not found in environment. Please set it in your .env file.")

            # OpenRouter uses OpenAI SDK with custom base URL
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1",
                timeout=self.timeout
            )
            # Default to Llama 3.1 70B (fast, affordable, good quality)
            self.model = model or os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-70b-instruct")
            logger.info(f"Using OpenRouter with model: {self.model}")

        else:
            raise ValueError(f"Unknown provider: {self.provider}. Use 'groq' or 'openrouter'")

    def call(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False
    ) -> str:
        """
        Make LLM API call

        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Sampling temperature (default 0.1)
            max_tokens: Max tokens to generate (default 8000)
            json_mode: Whether to request JSON output

        Returns:
            LLM response text
        """
        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature or 0.1,
            "max_tokens": max_tokens or 8000,
        }

        # Add provider-specific parameters
        if self.provider == "groq":
            kwargs["top_p"] = 0.9
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}

        elif self.provider == "openrouter":
            # OpenRouter supports JSON mode via response_format
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}
            # Add OpenRouter-specific headers for better tracking
            kwargs["extra_headers"] = {
                "HTTP-Referer": "https://legally.ai",
                "X-Title": "Legally AI Contract Analysis"
            }

        try:
            logger.info(f"Making LLM call to {self.provider} with model {self.model}")
            response = self.client.chat.completions.create(**kwargs)
            logger.info(f"LLM call successful, response length: {len(response.choices[0].message.content)} chars")
            return response.choices[0].message.content

        except TimeoutError as e:
            logger.error(f"LLM API call timed out after {self.timeout}s: {str(e)}")
            raise RuntimeError(
                f"LLM API call timed out after {self.timeout} seconds. "
                f"The AI service may be experiencing high load. Please try again in a few moments."
            )
        except Exception as e:
            error_msg = str(e)
            logger.error(f"LLM API call failed ({self.provider}): {error_msg}")

            # Provide more helpful error messages
            if "api key" in error_msg.lower() or "auth" in error_msg.lower():
                raise RuntimeError(
                    f"API authentication failed. Please check your {self.provider.upper()}_API_KEY "
                    f"in the .env file and ensure it's valid."
                )
            elif "rate limit" in error_msg.lower():
                raise RuntimeError(
                    f"API rate limit exceeded. Please wait a moment and try again, "
                    f"or consider using a different LLM provider."
                )
            elif "model" in error_msg.lower():
                raise RuntimeError(
                    f"Model '{self.model}' not available. Please check the model name "
                    f"in your configuration and ensure it's supported by {self.provider}."
                )
            else:
                raise RuntimeError(f"LLM API call failed ({self.provider}): {error_msg}")

    def call_with_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Make LLM call expecting JSON response

        Args:
            prompt: User prompt (should request JSON output)
            system_prompt: System prompt

        Returns:
            Parsed JSON dict
        """
        response_text = self.call(
            prompt=prompt,
            system_prompt=system_prompt,
            json_mode=True
        )

        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM returned invalid JSON: {str(e)}\n\nResponse: {response_text}")

    def estimate_tokens(self, text: str) -> int:
        """
        Rough estimate of token count

        Args:
            text: Text to estimate

        Returns:
            Estimated token count
        """
        # Very rough estimate: 1 token ≈ 4 characters for English
        # Slightly more for Cyrillic/other scripts
        return len(text) // 3


def test_llm_connection(api_key: Optional[str] = None, provider: Optional[str] = None) -> bool:
    """
    Test LLM connection with simple call

    Args:
        api_key: API key (optional)
        provider: 'groq' or 'openrouter' (optional)

    Returns:
        True if connection works
    """
    try:
        router = LLMRouter(api_key=api_key, provider=provider)
        response = router.call("Say 'Hello' if you can read this.")

        return "hello" in response.lower()

    except Exception as e:
        print(f"LLM connection test failed: {e}")
        return False
