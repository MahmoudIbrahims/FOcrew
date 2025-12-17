from crewai import LLM
from helpers.config import get_settings
from Agents.AgentEnums import AgentName
from .BeamLLM import BeamCustomLLM
from .OpenRouterLLM import OpenRouterCustomLLM
from crewai import BaseLLM  # Used for type hinting

class ProviderLLM:
    """
    A unified provider class that dynamically loads either a standard CrewAI LLM 
    or a custom BeamCustomLLM based on the configuration settings.
    """
    def __init__(self):
        self.enums = AgentName
        settings = get_settings()
        
        # 1. Determine whether to use the custom Beam LLM
        # We assume Beam is used if MODEL_NAME matches a specific value (e.g., "beam_custom")
        if settings.PROVIDER_NAME.lower() == "beam_model":
            print(f"Initializing BeamCustomLLM with model name is {settings.BEAM_MODEL_NAME}..")
            
            # Ensure the Beam settings (ENDPOINT, AUTH_TOKEN) are available
            self.llm: BaseLLM = BeamCustomLLM(
                endpoint=settings.BEAM_ENDPOINT,
                auth_token=settings.BEAM_AUTH_TOKEN,
                model=settings.BEAM_MODEL_NAME, # Custom model name for tracking
                temperature=settings.BEAM_TEMPERATURE
            )

        elif settings.PROVIDER_NAME.lower() == "openrouter_provider":
            print(f"Initializing OpenRouterCustomLLM with model name is {settings.OPENROUTER_MODEL_NAME}..")

            self.llm:BaseLLM =OpenRouterCustomLLM(
                endpoint =settings.OPENROUTER_ENDPOINT,
                auth_token =settings.OPENROUTER_AUTH_TOKEN,
                model=settings.OPENROUTER_MODEL_NAME,
                temperature=settings.OPENROUTER_TEMPERATURE

                     )
        # 2. Default Option: Use the standard CrewAI LLM
        elif settings.PROVIDER_NAME.lower() == "google_provider":
            print(f"Initializing CrewAI LLM with model: {settings.MODEL_NAME}...")
            # Standard LLM (usually requires an API key for services like OpenAI, Gemini, etc.)
            self.llm: BaseLLM = LLM(
                model=settings.MODEL_NAME,
                api_key=settings.API_KEY,
                temperature=settings.TEMPERATURE
            )
    
    def get_llm(self) -> BaseLLM:
        """
        Returns the initialized LLM object, whether it is standard (LLM) or custom (BeamCustomLLM).
        """
        return self.llm