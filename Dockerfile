# Base image Debian stretch python 3.6
FROM python:3.6-stretch

# Upgrade pip
RUN pip install --upgrade pip

# Create folder structure and install requirements
RUN mkdir -p /trader
RUN mkdir -p /trader/output

ADD ./requirements.txt /trader
WORKDIR /trader
RUN pip3 install -r requirements.txt

# Add code and update the working directory
ADD . /trader
WORKDIR /trader/trader

VOLUME /trader

# Run the application with unbuffered output to see it on real time
CMD python3 -u trader.py
