from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Model used for generation of chat response
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0" # "distilgpt2" - this one is faster but less accurate responses

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_text(prompt: str):
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(
        **inputs,
        max_length=256,
        do_sample=True,
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id
    )
    return tokenizer.decode(output[0], skip_special_tokens=True)