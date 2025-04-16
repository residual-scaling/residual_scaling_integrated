from config import prompt_hyperparameter


class PromptManager:
    def __init__(self):
        self.max_summarize_len = prompt_hyperparameter["max_summarize_len"]

    def generate_llama_summarize_prompt(self, txt: str) -> str:
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

    def generate_llama_generation_prompt(self, query: str, context: list) -> str:
        if len(context) == 0:
            # if there are no context
            context = "I don't know"
        else:
            # there exists some context
            context = ",".join(context)
        prompt = f"""<|begin_of_text|><|start_header_id|>user<|end_header_id|>
        Answer the question based on the context below. 
        If the answer is not in the context, say "I don't know".

        Context:
        {context}

        Question:
        {query}

        <|eot_id|><|start_header_id|>assistant<|end_header_id|>
        Answer:"""
        return prompt
    
    """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a helpful AI assistant. Use the provided context to answer the user's question.<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Context: "The Eiffel Tower was constructed in 1887-1889 as the entrance arch for the 1889 World's Fair. It is located in Paris, France and designed by Gustave Eiffel."

Question: When was the Eiffel Tower built?<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>"""


    
