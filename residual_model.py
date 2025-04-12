class ResidualModel():
    def __init__(self, model_name, model_path, db_type="keyword"):
        self.model_name = model_name
        self.model_path = model_path
        self.model = None

        self.db_type = db_type

    def load_model(self):
        if self.model_name == "openai":
            # import when needed
            from openai import OpenAI
            self.model = OpenAI(model=os.environ["OPENAI_MODEL_VERSION"], api_key=os.environ["OPENAI_API_KEY"])

            response = self. model.responses.create(
                input="Write a one-sentence bedtime story about a unicorn."
            )

            print(response.output_text)
