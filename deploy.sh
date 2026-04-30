# ---- one-time per shell ----
  export AWS_REGION=eu-west-1                 # or your region
  export AWS_ACCOUNT_ID=416558141896
  export ECR_REPO=meridian-chatbot
  export IMAGE_TAG=$(git rev-parse --short HEAD) # or "v1", "latest", etc.
  export ECR_URI=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}
  export BUILDKIT_PROGRESS=plain

  # ---- 1. create the ECR repo (only the first time) ----
  aws ecr create-repository \
    --repository-name "$ECR_REPO" \
    --region "$AWS_REGION" \
    --image-scanning-configuration scanOnPush=true

  # ---- 2. log Docker into ECR ----
  aws ecr get-login-password --region "$AWS_REGION" \
    | docker login --username AWS --password-stdin "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

  # ---- 3. build for linux/amd64, load locally, then push with progress ----
  # Run from the repo root (where the Dockerfile lives).
  # `--load` puts the image into the local Docker daemon so the subsequent
  # `docker push` shows the classic per-layer progress bars (Pushing /
  # Pushed / Layer already exists). `--progress=plain` streams the build
  # log instead of collapsing it.
  docker buildx build \
    --platform linux/amd64 \
    --provenance=false \
    --progress=plain \
    --load \
    -t "${ECR_URI}:${IMAGE_TAG}" \
    -t "${ECR_URI}:latest" \
    .

  echo ">>> Pushing ${ECR_URI}:${IMAGE_TAG}"
  docker push "${ECR_URI}:${IMAGE_TAG}"

  echo ">>> Pushing ${ECR_URI}:latest"
  docker push "${ECR_URI}:latest"

  echo ">>> Pushed digest:"
  docker inspect --format='{{index .RepoDigests 0}}' "${ECR_URI}:${IMAGE_TAG}"
