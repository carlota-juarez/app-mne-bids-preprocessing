FROM python:3.11-slim
 
ENV DEBIAN_FRONTEND=noninteractive
 
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir mne-bids-pipeline==1.10.1
 
WORKDIR /work
 
RUN rm -f /bin/sh && ln -s /bin/bash /bin/sh
 
RUN ldconfig