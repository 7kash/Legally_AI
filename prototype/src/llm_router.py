"""
LLM Router - Provider-agnostic LLM interface
Currently supports Groq API
"""

import os
from groq import Groq
from typing import Dict, Optional, Any
import json
from .constants import GROQ_SETTINGS


class LLMRouter:
    """
    Router for LLM API calls
    Supports multiple providers with fallback
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize LLM router

        Args:
            api_key: Groq API key (or reads from env)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment or provided")

        self.client = Groq(api_key=self.api_key)
        self.model = GROQ_SETTINGS["model"]

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
            temperature: Sampling temperature (default from settings)
            max_tokens: Max tokens to generate (default from settings)
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
            "temperature": temperature or GROQ_SETTINGS["temperature"],
            "max_tokens": max_tokens or GROQ_SETTINGS["max_tokens"],
            "top_p": GROQ_SETTINGS["top_p"]
        }

        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        try:
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content

        except Exception as e:
            raise RuntimeError(f"LLM API call failed: {str(e)}")

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


def test_llm_connection(api_key: Optional[str] = None) -> bool:
    """
    Test LLM connection with simple call

    Args:
        api_key: Groq API key (optional)

    Returns:
        True if connection works
    """
    try:
        router = LLMRouter(api_key=api_key)
        response = router.call("Say 'Hello' if you can read this.")

        return "hello" in response.lower()

    except Exception as e:
        print(f"LLM connection test failed: {e}")
        return False
