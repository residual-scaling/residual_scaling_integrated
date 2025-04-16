from config import prompt_hyperparameter
class PromptManager:
    def __init__(self):
        self.max_summarize_len = prompt_hyperparameter["max_summarize_len"]

    def get_llama_summarize_prompt(self, txt: str) -> str:
        prompt = f"""<|begin_of_text|><|start_header_id|>user<|end_header_id|>
        Summarize this text in {self.max_summarize_len - 1}-{self.max_summarize_len} concise sentences:

        {txt}

        <|eot_id|><|start_header_id|>assistant<|end_header_id|>
        Summary:"""
        return prompt

    def retrieve_llama_summarized_content(self, txt: str) -> str:
        keyword = "Summary:"
        summary_start = txt.rfind(keyword)
        if summary_start < 0:
            raise Exception("In retrieve_llama_summarized_content(), there should be a keyword but there isn't")
        summary_start += len(keyword)
        summary = txt[summary_start:].strip()
        return summary

    
