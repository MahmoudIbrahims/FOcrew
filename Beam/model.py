from beam import env
from Enums.ModelEnum import ModelConfig
if env.is_remote():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    
# This function runs once when the container first starts (on_start)
def load_models():
    tokenizer = AutoTokenizer.from_pretrained(
        ModelConfig.MODEL_NAME.value, 
        cache_dir=ModelConfig.BEAM_VOLUME_PATH.value,
        padding_side='left'
    )
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        ModelConfig.MODEL_NAME.value, 
        device_map="auto", 
        torch_dtype=torch.float16, 
        cache_dir=ModelConfig.BEAM_VOLUME_PATH.value,
        use_cache=True,
        low_cpu_mem_usage=True
    )
    model.eval()
    return model, tokenizer