REGISTRY_USER="jamesari"
REGISTRY="registry.gitlab.com"
IMG_NAME="$REGISTRY/$REGISTRY_USER/aswi-testing/web-dist:latest"

echo "$ASWI_GITLAB_TOKEN" | docker login $REGISTRY -u $REGISTRY_USER --password-stdin
cd web
docker build -t $IMG_NAME .
docker push $IMG_NAME
