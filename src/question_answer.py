# question answering

import torch 
from transformers import AutoTokenizer,AutoModelForQuestionAnswering


MODEL_NAME = "distilbert-base-cased-distilled-squad"

print("Loading querstion answering model...")

tokenizer =  AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForQuestionAnswering.from_pretrained(MODEL_NAME)

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model = model.to(device)

print(f"Using device {device}")

def answer_question(context:str,question:str)->str:
    
    if not context.strip():
        return "No context provided"
    
    if not question.strip():
        return "No context provided"

    inputs = tokenizer(
        question,
        context,
        return_tensors="pt",
        truncation=True,
        max_length = 512
    )
    
    inputs = {
        key:value.to(device) for key,value in inputs.items()
    }
    
    with torch.no_grad():
        outputs = model(**inputs)

    start_index = torch.argmax(outputs.start_logits).item()
    end_index = torch.argmax(outputs.end_logits).item()

    if end_index<start_index:
        end_index = start_index
        
    answers_token = inputs["input_ids"][0][
        start_index:end_index + 1
    ]
    
    answer = tokenizer.decode(
        answers_token,
        skip_special_tokens=True
    )
    
    return answer


if __name__ == "__main__":
    
    context =  """
    Photosynthesis is the process by which green plants
    convert light energy into chemical energy. During this
    process, plants use sunlight, carbon dioxide, and water
    to produce glucose and oxygen. Photosynthesis mainly
    takes place in the chloroplasts of plant cells.
    """
    
    question = "What is photosynthesis?"
    
    answer = answer_question(
        context,
        question
    )
    
    print("\n Context")
    print(context)

    print("\n Qustions")
    print(question)

    print("\n Answers")
    print(answer)