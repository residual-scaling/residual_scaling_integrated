from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from model.base_model import BaseModel


class LocalModel(BaseModel):
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="auto",
            torch_dtype="auto"
        )

    def get_pipline(self, pipeline_type: str):
        return pipeline(pipeline_type, model=self.model, tokenizer=self.tokenizer)

    def generate_distillation(self, txt: str) -> str:
        pipe = self.get_pipline("summarization")
        summarized_txt = pipe(txt)[0]["summary_text"]
        return summarized_txt

    def generate_answer(self, txt: str, context: str = "") -> str:
        # TODO use 'text-generation" or "question-answering"
        pipe = self.get_pipline("text-generation")
        # TODO fine-tune prompt later
        prompt = f"Request: {txt}; Context: {context}"
        output = pipe(
            prompt,
            # max_length=2000,
            # temperature=0.7,
            # top_p=0.9,
            num_return_sequences=1,
        )[0]["generated_text"]
        return output
