import sacrebleu
from transformers import MarianMTModel, MarianTokenizer, AutoModel, AutoTokenizer, PreTrainedModel, PreTrainedTokenizer
import chardet
from typing import List, Tuple, Union, Iterator, Callable
from pathlib import Path
from functools import partial
import os

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


def load_model(model_name: str) -> Tuple[Union[PreTrainedModel, PreTrainedTokenizer]]:
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    return model, tokenizer

model_name = 'Helsinki-NLP/opus-mt-zh-en'
# tokenizer = MarianTokenizer.from_pretrained(model_name)
# model = MarianMTModel.from_pretrained(model_name)

def translate(text: str, model: PreTrainedModel, tokenizer: PreTrainedTokenizer) -> str:
    """
    takes in a list of Chinese sentences and translates them to English
    """
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    translated_tokens = model.generate(**inputs)
    translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    return translated_text

  
def score_lines(ref_lines : Iterator, hyp_lines : Iterator, metric : Callable) -> Iterator: 
    to_score = zip(ref_lines, hyp_lines)
    get_scores  = lambda line: metric(*line)
    return map(get_scores, to_score)
 
def translate_file(src_file : Path, translate_fn : Callable[[str], str]) -> Iterator:
    src_lines = read_file(src_file) #Load as iterator
    return map(translate_fn, src_lines)
    
def evaluate(src_file : Path, tgt_file : Path, translate_fn : Callable, metric : Callable) -> Iterator:
    hyp_lines = translate_file(src_file, translate_fn)
    ref_lines = read_file(tgt_file) # Load as iterator
    yield from score_lines(ref_lines, hyp_lines, metric)
 

def write2log(scores, logfile):
    with open(logfile, 'a') as f:
        for score in scores: f.write(str(score)+"\n")

def unit_test(src_file = 'chinese.txt', tgt_file = 'english.txt', logfile='results.txt'):
    model, tokenizer = load_model(model_name)
    translate_fn = partial(translate, model=model, tokenizer=tokenizer)
    scores = evaluate(src_file, tgt_file, translate_fn, metric)
    write2log(scores, logfile)
 

def unit_tests(folders: List[str]):

    for folder in folders:
        files = os.listdir(folder)
        src_file, tgt_file = None, None
        for file in files:
            if 'chinese' in file: src_file = os.path.join(folder, file)
            if 'english' in file: tgt_file = os.path.join(folder, file)
        
        if src_file is not None and tgt_file is not None: unit_test(src_file, tgt_file)    

if __name__ == "__main__":
    unit_tests(["data"])