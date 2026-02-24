import mlflow
import os
from openai import OpenAI
# Set MLflow tracking credentials as environment variables
os.environ["MLFLOW_TRACKING_USERNAME"] = "admin"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "password1234"
# Specify the tracking URI for the MLflow server.
mlflow.set_tracking_uri("http://localhost:5000")

# Specify the experiment you just created for your GenAI application.
mlflow.set_experiment("test")

# Enable automatic tracing for all OpenAI API calls.
mlflow.openai.autolog()

# OpenAI client pointing at local/compatible API (Qwen3 Coder Next)
client = OpenAI(
    base_url="http://172.16.11.60:4000/v1",
    api_key="sk-_OHAQUTM_a901s5iCulk3Q",
)

# Model: qwen3-coder-next:latest (Qwen3 Coder Next), API: openai-completions compatible
# The trace of the following is sent to the MLflow server.
client.chat.completions.create(
    model="qwen3-coder-next:latest",
    messages=[
        {"role": "system", "content": "You are a helpful weather assistant."},
        {"role": "user", "content": "What's the weather like in Seattle?"},
    ],
)