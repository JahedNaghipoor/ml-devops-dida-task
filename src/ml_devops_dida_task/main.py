import logging
import uvicorn
import requests
from fastapi import FastAPI
import typer
import mlflow
from ml_devops_dida_task import __title__, __version__
from ml_devops_dida_task.Train import train

mlflow.set_tracking_uri("http://localhost:5000")

logger = logging.getLogger('ml_devops_dida_task')

app = typer.Typer(name='ml_devops_dida_task')


@app.command()
def main():
    """
    In this sample project you are going to deploy a simple text classification service based on a pretrained NLP models
    """
    logger.info("Looks like you're all set up. Let's get going!")
    
    # Initialize the few-shot text classifier with the model and MLflow experiment name
    model_names = ["facebook/bart-large-mnli", "cross-encoder/nli-deberta-base"]
    for run_name, model_name in zip(["facebook_bart", "nli-deberta-base"], model_names):
        classifier = train.FewShotTextClassifier(run_name, model_name, mlflow_experiment_name="ZeroShotClassifier")

        # Train and register the model in mlflow
        classifier.train_and_register_model()
    
    # Serve the model in FastAPI
    app = FastAPI()
    @app.post("/predict")
    def predict(text: str):
        labels = ["Happy", "Sad"]
        prediction = classifier.classify(text, labels)
        return prediction

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    app()

    url = 'http://localhost:8000/predict'
    payload = {"text": "Your text data here"}
    response = requests.post(url, json=payload, timeout=60)
    print(response.json())
