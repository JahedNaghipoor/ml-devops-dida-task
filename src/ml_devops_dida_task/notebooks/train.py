import mlflow
from mlflow.tracking import MlflowClient
from transformers import pipeline

class FewShotTextClassifier:
    def __init__(self, run_name, model_name, mlflow_experiment_name=None):
        self.mlflow_experiment_name = mlflow_experiment_name
        self.model_name = model_name
        self.run_name = run_name
        self.model_uri = None
        self.client = MlflowClient()
        self.classifier = None
        
        mlflow.set_experiment(experiment_name=self.mlflow_experiment_name)

    def train_and_register_model(self):
        # Train and save the model
        self.classifier = pipeline("zero-shot-classification", model=self.model_name)
        
        # Log the model in MLflow
        with mlflow.start_run(run_name=self.run_name):
            mlflow.log_param("model_name", self.model_name)
            mlflow.pytorch.log_model(self.classifier.model, "model")
            mlflow.pytorch.autolog()

            # Register the model in MLflow model registry
            self.model_uri =mlflow.register_model(f"runs:/{mlflow.active_run().info.run_id}/model", self.run_name)

    def load_model(self, model_name):
        # Load the model from the MLflow model registry
        if self.model_uri is None:
            raise ValueError("Model URI is not set. You need to train and register the model first.")
        
        self.model_uri =f"models:/{model_name}/latest"
        self.classifier = mlflow.pytorch.load_model(self.model_uri)

    def classify(self, text, labels):
        if self.classifier is None:
            raise ValueError("Model not loaded. You need to load the model first.")

        classification = self.classifier(text, labels)
        return classification['labels'][0]

