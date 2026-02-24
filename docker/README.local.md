# Building Production Image with Local Code Changes

This directory contains a custom Dockerfile (`Dockerfile.local`) for building a production MLflow image with your local code modifications.

## Building the Image

### Option 1: Build from MLflow root directory

```bash
# From the root of the MLflow repository
docker build -f docker/Dockerfile.local -t mlflow-custom:latest .
```

### Option 2: Build with specific version tag

```bash
docker build -f docker/Dockerfile.local -t mlflow-custom:v3.8.1-custom .
```

### Option 3: Build with build context optimization

If you want to exclude unnecessary files (faster builds, smaller context):

```bash
# Create a .dockerignore file in the root directory
docker build -f docker/Dockerfile.local -t mlflow-custom:latest .
```

## Using in Docker Compose

Update your `docker-compose.yml` to use the custom image:

```yaml
mlflow:
  # Instead of: image: registry.ai-links.com/mlflow/mlflow:v3.8.1
  image: mlflow-custom:latest
  # ... rest of your configuration
```

Or build it directly in docker-compose:

```yaml
mlflow:
  build:
    context: ..  # Parent directory (MLflow root)
    dockerfile: docker/Dockerfile.local
  # ... rest of your configuration
```

## Editable vs Regular Install

The Dockerfile uses `pip install -e` (editable install) by default. This means:
- **Pros**: Code changes are reflected immediately (useful for development)
- **Cons**: Larger image size, includes source files

For production, you might want to change line 15 to:
```dockerfile
RUN pip install --no-cache-dir /opt/mlflow
```

This creates a regular install (smaller, but requires rebuild for code changes).

## Customization

### Adding Additional Dependencies

Uncomment and modify the optional dependencies section:
```dockerfile
RUN pip install --no-cache-dir psycopg2-binary boto3 <your-packages>
```

### Multi-stage Build (Optional)

For smaller final image, you can use a multi-stage build:
```dockerfile
FROM python:3.10-slim-bullseye AS builder
WORKDIR /build
COPY . /build
RUN pip install --no-cache-dir /build

FROM python:3.10-slim-bullseye
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
WORKDIR /home/mlflow
CMD ["python", "-m", "mlflow", "--help"]
```
