# Databricks notebook source
# Import necessary libraries
from transformers import TextClassificationPipeline, Trainer, TrainingArguments
from datasets import load_dataset
from sklearn.model_selection import train_test_split

# Load dataset
dataset = load_dataset("your_dataset_name")

# Split dataset into train and test sets
train_data, test_data = train_test_split(dataset['train'], test_size=0.2, random_state=42)

# Define model and task
Model_name = "facebook/opt-350m"
model = TextClassificationPipeline(model=model_name, task="zero-shot-classification")

# Fine-tune the model
trainer = Trainer(
    model=model,
    args=TrainingArguments(
        per_device_train_batch_size=8,
        learning_rate=2e-5,
        num_train_epochs=3,
        evaluation_strategy="epoch",
        save_strategy="epoch",
    ),
    train_dataset=train_data,
    eval_dataset=test_data,
)
trainer.train()

# Save the fine-tuned model
trainer.save_model("fine_tuned_model")
