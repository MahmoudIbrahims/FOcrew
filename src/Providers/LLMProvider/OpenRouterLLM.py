from crewai import BaseLLM
from typing import Any, Dict, List, Optional, Union
import requests
from requests.exceptions import JSONDecodeError, RequestException 

class OpenRouterCustomLLM(BaseLLM):
     
    """
    A custom Large Language Model (LLM) implementation for CrewAI, 
    designed to communicate with the OpenRouter API endpoint.
    """
    def __init__(self, 
                 auth_token: str, 
                 model: str,
                 endpoint: str,
                 temperature: Optional[float] = 0.1):
        
        # Initialize the BaseLLM parent class
        super().__init__(model=model, temperature=temperature)
        
        self.auth_token = auth_token    # OpenRouter API Key
        self.endpoint = endpoint        # OpenRouter Chat Completions URL
        
    def call(
        self,
        messages: Union[str, List[Dict[str, str]]],
        tools: Optional[List[dict]] = None,
        callbacks: Optional[List[Any]] = None,
        available_functions: Optional[Dict[str, Any]] = None,
    ) -> Union[str, Any]:
        """
        Sends a POST request to the OpenRouter API and extracts the response content.
        """
        # 1. Format Messages: Ensure messages are in the list of dicts format
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
            
        # 2. Prepare the Payload (OpenAI/OpenRouter Format)
        payload = {
            "model": self.model, 
            "messages": messages,
            "temperature": self.temperature,
            # Enabling reasoning for better agent performance (as per OpenRouter spec)
            # "reasoning": {"enabled": True}, 
        }
        
        # 3. Make the API Call
        try:
            response = requests.post(
                self.endpoint,
                headers={
                    # OpenRouter requires the API key as a Bearer Token
                    "Authorization": f"Bearer {self.auth_token}",
                    "Content-Type": "application/json"
                },
                json=payload, 
                timeout=60
            )
            
            # Raise exception for 4xx/5xx HTTP errors
            response.raise_for_status() 
            
            # --- Robust JSON Parsing FIX ---
            try:
                # Attempt to parse the response body as JSON
                result = response.json()
            except JSONDecodeError as e:
                # If parsing fails, the server returned non-JSON data (e.g., HTML error page).
                error_message = (
                    f"OpenRouter API returned a non-JSON response. "
                    f"Status Code: {response.status_code}. "
                    f"Raw Text (First 100 chars): '{response.text[:100]}...'. "
                    f"Original JSON Decode Error: {e}"
                )
                raise Exception(f"OpenRouter API call failed: {error_message}")
            # --- END FIX ---

            # 4. Extract Content from the Response
            # Structure: result['choices'][0]['message']['content']
            if result and "choices" in result and result["choices"]:
                
                # Extract the final answer content
                message_content = result["choices"][0]["message"].get("content", "")
                
                return message_content
            
            # Fallback for unexpected API response structure (e.g., valid JSON but missing 'choices')
            raise Exception(f"OpenRouter returned a valid JSON but unexpected structure: {result}")
            
        except RequestException as e:
            # Handle connection, DNS, HTTP, or timeout errors
            raise Exception(f"OpenRouter API call failed: {e}")

    def supports_function_calling(self) -> bool:
        """
        Indicates support for CrewAI's tool-calling/function-calling mechanism.
        """
        return True

    def get_context_window_size(self) -> int:
        """
        Return the context window size of the selected model. 
        (32,768 tokens is common for Mistral-7B).
        """
        return 32768