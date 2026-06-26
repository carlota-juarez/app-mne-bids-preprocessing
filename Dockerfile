FROM python:3.11-slim [cite: 1]

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    QT_QPA_PLATFORM=offscreen \
    MNE_BROWSER_BACKEND=matplotlib \
    MPLBACKEND=Agg [cite: 1]

RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean [cite: 1]

RUN pip install --no-cache-dir "numpy<2" "scipy" "matplotlib" "scikit-learn" \
    && rm -rf /root/.cache 

RUN pip install --no-cache-dir mne mne-bids \
    && rm -rf /root/.cache 

RUN pip install --no-cache-dir mne-bids-pipeline==1.10.1 \
    && find /usr/local/lib/python3.11 -type d -name "__pycache__" -exec rm -rf {} + \
    && find /usr/local/lib/python3.11 -type d \( -name "tests" -o -name "test" \) -exec rm -rf {} + \
    && rm -rf /root/.cache 
 
WORKDIR /work [cite: 2]

RUN rm -f /bin/sh && ln -s /bin/bash /bin/sh [cite: 2]

RUN ldconfig [cite: 2]