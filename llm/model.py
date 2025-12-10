from transformers import AutoModelForCausalLM, AutoTokenizer

# Create a class for the llm to easy access
class LocalLLM:
    def __init__(self, model_path: str) -> None:
        self.model_path = model_path
        self._load_model()

    # Load the model using only local files
    def _load_model(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            local_files_only=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            dtype="auto",
            device_map="auto",
            local_files_only=True,
        )

    # Method responsible for receive the string question and return the llm response
    def _generate_response(self, prompt: str)-> str:
        messages = [
            {"role": "system", "content": "Você é uma assistente que auxilia na tarefa de resumir documentos pdf."},
            {"role": "user", "content": prompt}
        ]

        # Convert the messages to a text prompt using the model’s chat template
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False  # Switches between thinking and non-thinking modes. Default is True.
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        # Generate the model output with sampling parameters
        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=1024, # Limit the length of the generated response
            do_sample = True, # Enable probabilistic sampling
            temperature=0.7, # Controls randomness
            top_p=0.8, # Nucleus sampling threshold
            top_k=20, # Limit sampling to the top-k tokens
            min_p=0
        )

        # Extract the generated tokens (ignoring the input prompt portion)
        output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()

        # parsing thinking content
        try:
            # rindex finding 151668 (</think>)
            index = len(output_ids) - output_ids[::-1].index(151668)
        except ValueError:
            index = 0

        # thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
        content = self.tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

        return content

    # Public method to send a prompt to the model
    def ask_to_model(self, prompt: str) -> str:
        return self._generate_response(prompt)