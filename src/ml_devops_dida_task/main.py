import logging
import uvicorn
import requests
import pandas as pd
from fastapi import FastAPI
import typer
import mlflow
from pprint import pprint
from mlflow import MlflowClient
from ml_devops_dida_task import __title__, __version__
from ml_devops_dida_task.notebooks import train

mlflow.set_tracking_uri("http://localhost:5003")

logger = logging.getLogger('ml_devops_dida_task')

app = typer.Typer(name='ml_devops_dida_task')


@app.command()
def main():
    """
    In this sample project you are going to deploy a simple text classification service based on a pretrained NLP

    Note: This is the entry point of your command line application. The values of the CLI params
    that are passed to this application will show up als parameters to this function.
    This docstring is where you describe what your command line application does.
    Try running `python -m ml_devops_dida_task --help` to see how this shows up in the
    command line.
    """
    logger.info("Looks like you're all set up. Let's get going!")
    
    # Initialize the few-shot text classifier with the model and MLflow experiment name
    model_names = ["facebook/opt-350m", "gpt2-large", "distilgpt2"]
    for run_name, model_name in zip(["facebook_350", "gpt2large", "distilgpt2"], model_names):
        classifier = train.FewShotTextClassifier(run_name, model_name, mlflow_experiment_name="ZeroShotClassifier")

        # Train and register the model
        classifier.train_and_register_model()


    # Define input sentence and label examples
    sentence = "feeling like a million bucks"
    labels = ["happy", "sad"]


    # # Classify the sentence
    # predicted_label = classifier.classify(sentence, labels)

    # print("Input Sentence:", sentence)
    # print("Predicted Label:", predicted_label)
    
    # logged_model = 'runs:/fd4478e9d0e24e4aa8629720109bef87/distilgpt2'

    # # Load model as a PyFuncModel.
    # loaded_model = mlflow.pyfunc.load_model(logged_model)

    # # model = mlflow.sklearn.load_model(model_uri=f"models:/{model_name}")

    # loaded_model.predict("I am not happy at all!")
    # loaded_model = mlflow.pyfunc.load_model(model_uri)

    # predictions = loaded_model.predict("I am sad")
    
      # Serve the model in FastAPI

    app = FastAPI()
    @app.post("/predict")
    def predict(text: str):

        loaded_model = classifier.load_model("facebook_350") # load facebook_350 model

        predictions = loaded_model.predict(text)
        return predictions
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    app()


    url = 'http://localhost:8000/predict'
    payload = {"text": "Your text data here"}
    response = requests.post(url, json=payload, timeout=60)
    print(response.json())
