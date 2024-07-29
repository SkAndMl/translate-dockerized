import sacrebleu
from transformers import AutoProcessor, SeamlessM4Tv2Model
import chardet
from typing import Tuple, Iterator, Callable
from pathlib import Path
from functools import partial
import os
import json

with open("config.json", "r") as f: config = json.loads(f.read())

def metric(candidate: str, reference: str) -> float:
    reference = [[reference]]
    score = sacrebleu.corpus_bleu([candidate], reference).score
    return score

def detect_encoding(file_path: Path):
    """detects the encoding of the file passed"""
    with open(file_path, 'rb') as file: raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']
    

def read_file(file_path: Path) -> Iterator[str]:
    with open(file_path, 'r', encoding=detect_encoding(file_path)) as file: content = file.read()
    content = content.strip().split("\n")
    for line in content: yield line


def load_model(model_name: str) -> Tuple:
    model = SeamlessM4Tv2Model.from_pretrained(model_name)
    processor = AutoProcessor.from_pretrained(model_name)
    return model, processor


def translate(text: str, model, processor) -> str:
    """
    takes in a list of Chinese sentences and translates them to English
    """
    inputs = processor(text=text, src_lang=config['src_lang'], return_tensors="pt")
    output_tokens = model.generate(**inputs, tgt_lang=config['tgt_lang'], generate_speech=False)
    translated_text = processor.decode(output_tokens[0].tolist()[0], skip_special_tokens=True)
    return translated_text

  
def score_lines(ref_lines : Iterator, hyp_lines : Iterator, metric : Callable) -> Iterator: 
    to_score = zip(ref_lines, hyp_lines)
    get_scores  = lambda line: metric(*line)
    return map(get_scores, to_score)
 
def translate_file(src_file : Path, translate_fn : Callable[[str], str]) -> Iterator:
    src_lines = read_file(src_file) 
    return map(translate_fn, src_lines)
    
def evaluate(src_file : Path, tgt_file : Path, translate_fn : Callable, metric : Callable) -> Iterator:
    hyp_lines = translate_file(src_file, translate_fn)
    ref_lines = read_file(tgt_file) 
    yield from score_lines(ref_lines, hyp_lines, metric)
 

def write2log(scores, logfile):
    with open(logfile, 'a') as f:
        for score in scores: f.write(str(score)+"\n")

def unit_test(src_file = 'chinese.txt', tgt_file = 'english.txt', logfile='results.txt'):
    model, processor = load_model(config['model_name'])
    translate_fn = partial(translate, model=model, processor=processor)
    scores = evaluate(src_file, tgt_file, translate_fn, metric)
    write2log(scores, logfile)
 

def unit_tests(test_folder):
    folders = os.listdir(test_folder)
    folders = [os.path.join(test_folder, folder) for folder in folders]
    folders = [folder for folder in folders if os.path.isdir(folder)]
    for folder in folders:
        files = os.listdir(folder)
        src_file, tgt_file = None, None
        for file in files:
            if config['src_lang'] in file: src_file = os.path.join(folder, file)
            if config['tgt_lang'] in file: tgt_file = os.path.join(folder, file)
        
        if src_file is not None and tgt_file is not None: unit_test(src_file, tgt_file)    

if __name__ == "__main__":
    unit_tests(config['test_folder'])