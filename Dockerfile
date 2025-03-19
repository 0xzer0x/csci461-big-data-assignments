# Use Ubuntu as the base image
FROM ubuntu:latest

# Update the package list and install Python3 and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip 

RUN pip3 install --break-system-packages pandas numpy seaborn matplotlib scikit-learn scipy openpyxl
# Create the /home/doc-bd-a1/ directory
RUN mkdir -p /home/doc-bd-a1

# Copy the dataset into the container
COPY cancer_data.xlsx /home/doc-bd-a1/cancer_data.xlsx
COPY load.py /home/doc-bd-a1/load.py

# Set the working directory
WORKDIR /home/doc-bd-a1

# Open the bash shell upon container startup
CMD ["/bin/bash"]