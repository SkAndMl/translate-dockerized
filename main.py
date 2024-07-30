from fastapi import FastAPI, HTTPException
from fastapi import Body
from transformers import AutoProcessor, SeamlessM4Tv2Model
from typing import List, Dict
import json
import os

app = FastAPI()

# Load the pre-trained model and tokenizer
with open("config.json", "r") as f:
    config = json.loads(f.read())
model_path = os.path.join(config['model_dir'], config['model_name'])
processor = AutoProcessor.from_pretrained(model_path)
model = SeamlessM4Tv2Model.from_pretrained(model_path)


@app.post("/translate")
async def translate(sentences: List[str], src_lang: str=Body(default='cmn'), tgt_lang: str=Body(default='eng')) -> Dict[str, List[str]]:
    translations = []
    for sentence in sentences:
        inputs = processor(text=sentence, src_lang=src_lang, return_tensors="pt")
        output_tokens = model.generate(**inputs, tgt_lang=tgt_lang, generate_speech=False)
        translated_text = processor.decode(output_tokens[0].tolist()[0], skip_special_tokens=True)
        translations.append(translated_text)
    return {"translated_sentences": translations}