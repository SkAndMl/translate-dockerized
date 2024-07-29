from fastapi import FastAPI, HTTPException
from transformers import MarianMTModel, MarianTokenizer
from typing import List

app = FastAPI()

# Load the pre-trained model and tokenizer
model_name = 'Helsinki-NLP/opus-mt-zh-en'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)


@app.post("/translate")
async def translate(sentences: List[str]):
    translations = []
    for sentence in sentences:
        inputs = tokenizer.encode(sentence, return_tensors="pt", padding=True)
        outputs = model.generate(inputs, max_length=40, num_beams=4, early_stopping=True)
        translated_sentence = tokenizer.decode(outputs[0], skip_special_tokens=True)
        translations.append(translated_sentence)
    return {"translated_sentences": translations}