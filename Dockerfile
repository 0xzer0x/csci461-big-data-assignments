FROM ubuntu:latest

RUN apt-get update && \
  apt-get install --no-install-recommends -y python3 python3-pip && \
  rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --break-system-packages pandas numpy seaborn matplotlib scikit-learn scipy openpyxl

WORKDIR /home/doc-bd-a1

# NOTE: copy dataset
COPY cancer_data.xlsx ./
# NOTE: copy scripts
COPY load.py dpre.py eda.py vis.py model/model.py ./

ENTRYPOINT ["/bin/bash"]
