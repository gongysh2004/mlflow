import os
import mlflow

# Set MLflow tracking credentials as environment variables
os.environ["MLFLOW_TRACKING_USERNAME"] = "admin"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "password1234"

# Set tracking URI (adjust if needed)
# mlflow.set_tracking_uri("http://localhost:5000")

# Your training code here
if __name__ == "__main__":
    with mlflow.start_run():
        # Example: log a parameter
        mlflow.log_param("param1", "value1")
        
        # Example: log a metric
        mlflow.log_metric("accuracy", 0.95)
        
        print("MLflow tracking configured with username: admin")
