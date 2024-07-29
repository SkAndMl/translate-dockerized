import os
import json
from transformers import AutoProcessor, SeamlessM4Tv2Model

# Load configuration
with open("config.json", "r") as f:
    config = json.load(f)

model_name = config["model_name"]
model_dir = config["model_dir"]

if not os.path.exists(model_dir):
    os.makedirs(model_dir)

model_path = os.path.join(model_dir, model_name)

if not os.path.exists(model_path):
    processor = AutoProcessor.from_pretrained(model_name)
    model = SeamlessM4Tv2Model.from_pretrained(model_name)
    processor.save_pretrained(model_path)
    model.save_pretrained(model_path)
else:
    print("Model already exists. Skipping download.")