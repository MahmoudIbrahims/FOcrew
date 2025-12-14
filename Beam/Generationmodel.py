from beam import endpoint, Image, Volume,env
from model import load_models
from Enums.ModelEnum import ModelConfig

if env.is_remote():
    import torch


image = (
    Image(python_version="python3.9")
    .add_python_packages(
        [
            "torch",
            "transformers",
            "accelerate",
            "huggingface_hub[hf-transfer]",
            "sentencepiece",     
            "protobuf", 
        ]
    )
    .with_envs({
        "HF_HUB_ENABLE_HF_TRANSFER": "1",
        "TOKENIZERS_PARALLELISM": "false",
        "CUDA_VISIBLE_DEVICES": "0",
    })
)


@endpoint(
    secrets=["HF_TOKEN"],
    on_start=load_models,
    name="mistralai/Mistral-7B-Instruct-v0.3",
    cpu=5,
    memory="16Gi",
    gpu="A10G",
    volumes=[
        Volume(
            name="cached_models",
            mount_path=ModelConfig.BEAM_VOLUME_PATH.value,
        )
    ],
    image=image,
)
def generate_text(context, **inputs):
    # Retrieve model and tokenizer from on_start
    model, tokenizer = context.on_start_value

    # Inputs passed to API
    messages = inputs.pop("messages", None)
    if not messages:
        return {"error": "Please provide messages for text generation."}

    generate_args = {
        "max_new_tokens": inputs.get("max_tokens", ModelConfig.MAX_LENGTH.value),
        "temperature": inputs.get("temperature", ModelConfig.TEMPERATURE.value),
        "top_p": inputs.get("top_p", ModelConfig.TOP_P.value),
        "top_k": inputs.get("top_k", ModelConfig.TOP_K.value),
        "repetition_penalty": inputs.get("repetition_penalty", ModelConfig.REPETITION_PENALTY.value),
        "no_repeat_ngram_size": inputs.get(
            "no_repeat_ngram_size", ModelConfig.NO_REPEAT_NGRAM_SIZE.value
        ),
        "num_beams": inputs.get("num_beams",ModelConfig. NUM_BEAMS.value),
        "early_stopping": inputs.get("early_stopping",ModelConfig.EARLY_STOPPING.value),
        "do_sample": inputs.get("do_sample",ModelConfig.DO_SAMPLE.value),
        "use_cache": True,
        "eos_token_id": tokenizer.eos_token_id,
        "pad_token_id": tokenizer.pad_token_id,
    }

    model_inputs_str = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    
    tokenized_inputs = tokenizer(
        model_inputs_str, 
        return_tensors="pt", 
        padding=True, 
        truncation=True, 
        max_length=2048
    )
    input_ids = tokenized_inputs["input_ids"].to("cuda")
    attention_mask = tokenized_inputs["attention_mask"].to("cuda")
    input_ids_length = input_ids.shape[-1]

    with torch.no_grad():
        outputs = model.generate(
            input_ids=input_ids, 
            attention_mask=attention_mask, 
            **generate_args
        )
        new_tokens = outputs[0][input_ids_length:]
        output_text = tokenizer.decode(new_tokens, skip_special_tokens=True)
        return {"output": output_text}