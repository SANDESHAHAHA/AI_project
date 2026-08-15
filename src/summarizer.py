import transformers
from transformers import AutoTokenizer,AutoModelForSeq2SeqLM
import torch 

print(transformers.__version__)
# load a pretrained summarizer model 

MODEL_NAME = "facebook/bart-large-cnn"      

print("loading model..")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME        )


# use gpu if available 

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

print(f"using device {device}")


def summarize_text(text:str)->str:
    if not text.strip():
        return "No text provided"
    
    inputs = tokenizer(
        text,
        max_length = 1024,
        truncation = True,
        return_tensors = "pt"
    )
    
    inputs  = {
        key:value.to(device) for key,value in inputs.items()
    }
    
    summary_ids = model.generate(
        **inputs,
        max_length =100,
        min_length = 30,
        num_beams = 4,
        early_stopping=True
    )
    
    summary = tokenizer.decode(
        summary_ids[0],
        skip_special_tokens=True
    )
    
    return summary

if __name__ == "__main__":
    text = """ 
      Photosynthesis is the process by which green plants
    convert light energy into chemical energy. During this
    process, plants use sunlight, carbon dioxide, and water
    to produce glucose and oxygen. Photosynthesis mainly
    takes place in the chloroplasts of plant cells.
    """
    summary = summarize_text(text)
    print(f"\n Original Text")
    print(text)

    print(f"\n Summary")
    print(summary)