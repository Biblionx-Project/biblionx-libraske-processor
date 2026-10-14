FROM python:3.12-slim-bookworm

LABEL maintainer="Biblionx Team" \
      org.opencontainers.image.title="Biblionx Libraske Processor" \
      org.opencontainers.image.description="Biblionx sign pose and motion processing worker" \
      org.opencontainers.image.vendor="Biblionx"

COPY . /mediapipe/

WORKDIR /mediapipe/

RUN bash install.sh

CMD ["make", "start"]