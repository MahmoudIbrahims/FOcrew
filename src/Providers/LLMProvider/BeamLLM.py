from crewai import BaseLLM
from typing import Any, Dict, List, Optional, Union
import requests

class BeamCustomLLM(BaseLLM):
    """
    A custom Large Language Model (LLM) implementation for CrewAI, 
    designed to communicate with a specific Beam Cloud endpoint.
    """
    def __init__(self, endpoint: str,
                            auth_token: str, model: str = "mistralai/Mistral-7B-Instruct-v0.3",
                            temperature: Optional[float] = 0.1):
        # 1. Initialize the BaseLLM parent class with required parameters
        # 'model' and 'temperature' are necessary for BaseLLM, even if the 
        # external endpoint doesn't use them directly by name.
        super().__init__(model=model, temperature=temperature)
        
        self.auth_token = auth_token  # Beam Cloud Authorization Token
        self.endpoint = endpoint      # Beam Cloud API URL
        
    def call(
        self,
        messages: Union[str, List[Dict[str, str]]],
        tools: Optional[List[dict]] = None,
        callbacks: Optional[List[Any]] = None,
        available_functions: Optional[Dict[str, Any]] = None,
    ) -> Union[str, Any]:
        """
        Sends a POST request to the Beam Cloud endpoint and processes the response.
        This method is the core interface for CrewAI to interact with the LLM.
        """
        # 1. Format Messages: Ensure messages are in the list of dicts format
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
            
        # 2. Prepare the Payload
        # The Beam endpoint generally expects an array of 'messages'.
        payload = {
            "messages": messages,
            # If your Beam model supports them, you could include:
            # "model": self.model, 
            # "temperature": self.temperature, 
        }
        
        # 3. Make the API Call
        try:
            response = requests.post(
                self.endpoint,
                headers={
                    # Use the Auth Token in the Authorization Header (Bearer Token)
                    "Authorization": f"Bearer {self.auth_token}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=60 # Increased timeout for potential long-running model responses
            )
            response.raise_for_status() # Raise an exception for HTTP error codes (4xx/5xx)
            
            result = response.json()
            
            # 4. Extract Content from the Response
            # Standard API response structure (like OpenAI/many custom endpoints) is often:
            # {"choices": [{"message": {"content": "..."}}]}
            if result and "choices" in result and result["choices"]:
                # Return the main content from the first choice
                return result["choices"][0]["message"]["content"]
            
            # Fallback if the expected path is missing (e.g., if the Beam structure differs)
            return str(result)
            
        except requests.exceptions.RequestException as e:
            # Handle connection errors (e.g., Timeout, 404)
            raise Exception(f"Beam Cloud API call failed: {e}")

    def supports_function_calling(self) -> bool:
        """
        Indicate whether the custom LLM supports CrewAI's tool-calling/function-calling mechanism.
        """
        return True

    def get_context_window_size(self) -> int:
        """
        Return the context window size of your Beam Cloud model.
        """
        return 32768 # Adjust this value based on your specific model's context limit