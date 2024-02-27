# imports
import mlflow
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, GenerationConfig

# configurations
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment(experiment_name="compare_llm_models")
run_ids = []
artifact_paths = []
model_names = ["facebook_350", "gpt2large", "distilgpt2"]

gcfg = {
    "max_length": 180,
    "max_new_tokens": 10,
    "do_sample": False,
}

example = (
    "Q: Are elephants larger than mice?\nA: Yes.\n\n"
    "Q: Are mice carnivorous?\nA: No, mice are typically omnivores.\n\n"
    "Q: What is the average lifespan of an elephant?\nA: The average lifespan of an elephant in the wild is about 60 to 70 years.\n\n"
    "Q: Is Mount Everest the highest mountain in the world?\nA: Yes.\n\n"
    "Q: Which city is known as the 'City of Love'?\nA: Paris is often referred to as the 'City of Love'.\n\n"
    "Q: What is the capital of Australia?\nA: The capital of Australia is Canberra.\n\n"
    "Q: Who wrote the novel '1984'?\nA: The novel '1984' was written by George Orwell.\n\n"
)


eval_df = pd.DataFrame(
    {
        "question": [
            "Q: What color is the sky?\nA:",
            "Q: Are trees plants or animals?\nA:",
            "Q: What is 2+2?\nA:",
            "Q: Who is Darth Vader?\nA:",
            "Q: What is your favorite color?\nA:",
        ]
    }
)


class PyfuncTransformer(mlflow.pyfunc.PythonModel):
    """PyfuncTransformer is a class that extends the mlflow.pyfunc.PythonModel class
    and is used to create a custom MLflow model for text generation using Transformers.
    """

    def __init__(self, model_name, gen_config_dict=None, examples=""):
        """
        Initializes a new instance of the PyfuncTransformer class.

        Args:
            model_name (str): The name of the pre-trained Transformer model to use.
            gen_config_dict (dict): A dictionary of generation configuration parameters.
            examples: examples for multi-shot prompting, prepended to the input.
        """
        self.model_name = model_name
        self.gen_config_dict = (
            gen_config_dict if gen_config_dict is not None else {}
        )
        self.examples = examples
        super().__init__()

    def load_context(self, context):
        """
        Loads the model and tokenizer using the specified model_name.

        Args:
            context: The MLflow context.
        """
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map="cpu", # auto
        )

        # Create a custom GenerationConfig
        gcfg = GenerationConfig.from_model_config(model.config)
        for key, value in self.gen_config_dict.items():
            if hasattr(gcfg, key):
                setattr(gcfg, key, value)

        # Apply the GenerationConfig to the model's config
        model.config.update(gcfg.to_dict())

        self.model = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            return_full_text=False,
        )

    def predict(self, context, model_input):
        """
        Generates text based on the provided model_input using the loaded model.

        Args:
            context: The MLflow context.
            model_input: The input used for generating the text.

        Returns:
            list: A list of generated texts.
        """
        if isinstance(model_input, pd.DataFrame):
            model_input = model_input.values.flatten().tolist()
        elif not isinstance(model_input, list):
            model_input = [model_input]

        generated_text = []
        for input_text in model_input:
            output = self.model(
                self.examples + input_text, return_full_text=False
            )
            generated_text.append(
                output[0]["generated_text"],
            )

        return generated_text

facebook_350 = PyfuncTransformer("facebook/opt-350m",gen_config_dict=gcfg,examples=example)
gpt2large = PyfuncTransformer("gpt2-large",gen_config_dict=gcfg,examples=example)
distilgpt2 = PyfuncTransformer("distilgpt2",gen_config_dict=gcfg,examples=example)

for model, name in zip([facebook_350, gpt2large, distilgpt2], model_names):
    with mlflow.start_run(run_name=name):
        pyfunc_model = model
        artifact_path = f"models/{name}"
        mlflow.pyfunc.log_model(
            artifact_path=artifact_path,
            python_model=pyfunc_model,
            input_example="Q: What color is the sky?\nA:",
        )
        mlflow.autolog()
        run_ids.append(mlflow.active_run().info.run_id)
        artifact_paths.append(artifact_path)      