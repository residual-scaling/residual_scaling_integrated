from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from model.base_model import BaseModel
from prompt_manager import PromptManager
from config import model_hyperparameter
from util import clean_string


class LocalModel(BaseModel):
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="auto",
            torch_dtype="auto"
        )
        self.pm = PromptManager()
        self.pipe = pipeline("text-generation", 
                            model=self.model, 
                            tokenizer=self.tokenizer,
                            do_sample=True,
                            temperature=model_hyperparameter["temperature"]
                            )

    def generate_distillation(self, txt: str) -> str:
        summerization_prompt = self.pm.generate_llama_summarize_prompt(txt)
        summarized_result = self.pipe(summerization_prompt)[0]['generated_text']
        summarized_txt = clean_string(self.pm.retrieve_llama_summarized_content(summarized_result))
        return summarized_txt

    def generate_answer(self, txt: str, context: str = "") -> str:
        return output
