# Quick Start: Building Production Image with Local Code

## Step 1: Build the Custom Image

From the **root of the MLflow repository**:

```bash
docker build -f docker/Dockerfile.local -t mlflow-custom:latest .
```

This will:
- Copy your local MLflow code into the image
- Install MLflow from source (editable install by default)
- Create a production-ready image

## Step 2: Use in Docker Compose

### Option A: Build directly in docker-compose

Modify `docker-compose.yml` to replace the `image:` line with `build:`:

```yaml
mlflow:
  build:
    context: ..  # Points to MLflow root directory
    dockerfile: docker/Dockerfile.local
  # Remove: image: registry.ai-links.com/mlflow/mlflow:v3.8.1
```

Then run:
```bash
cd docker-compose
docker compose up -d --build mlflow
```

### Option B: Use pre-built image

After building the image (Step 1), update `docker-compose.yml`:

```yaml
mlflow:
  image: mlflow-custom:latest
  # Remove: image: registry.ai-links.com/mlflow/mlflow:v3.8.1
```

### Option C: Use override file (recommended)

Keep your original `docker-compose.yml` unchanged and use:

```bash
cd docker-compose
docker compose -f docker-compose.yml -f docker-compose.local.yml up -d --build mlflow
```

## Step 3: Verify

```bash
# Check the container is running
docker compose ps

# Check logs
docker compose logs mlflow

# Verify MLflow version includes your changes
docker compose exec mlflow python -c "import mlflow; print(mlflow.__version__)"
```

## Rebuilding After Code Changes

### If using editable install (-e):
- **No rebuild needed** - changes are reflected immediately
- Just restart: `docker compose restart mlflow`

### If using regular install:
- Rebuild: `docker build -f docker/Dockerfile.local -t mlflow-custom:latest .`
- Restart: `docker compose up -d mlflow`

## Customization Tips

1. **Remove editable install** for smaller images:
   Change line 15 in `Dockerfile.local`:
   ```dockerfile
   RUN pip install --no-cache-dir /opt/mlflow  # Remove -e flag
   ```

2. **Add dependencies** before MLflow install:
   ```dockerfile
   RUN pip install --no-cache-dir psycopg2-binary boto3
   RUN pip install --no-cache-dir -e /opt/mlflow
   ```

3. **Optimize build context** - create `.dockerignore` in root:
   ```
   .git
   tests/
   examples/
   docs/
   *.pyc
   __pycache__/
   ```

## Troubleshooting

- **Build fails**: Make sure you're running from the MLflow root directory
- **Import errors**: Check that all MLflow dependencies are installed
- **Large image**: Use multi-stage build or remove editable install
- **Changes not reflected**: Rebuild the image if not using editable install
