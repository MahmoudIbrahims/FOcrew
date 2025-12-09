from enum import Enum

class ModelConfig(Enum):
    MODEL_NAME ="mistralai/Mistral-7B-Instruct-v0.3"              #"meta-llama/Meta-Llama-3.1-8B-Instruct"
    MAX_LENGTH = 512
    TEMPERATURE = 0.7
    TOP_P = 0.95
    TOP_K = 40
    REPETITION_PENALTY = 1.1
    NO_REPEAT_NGRAM_SIZE = 3
    DO_SAMPLE = True
    NUM_BEAMS = 1
    EARLY_STOPPING = True

    BEAM_VOLUME_PATH = "./cached_models"