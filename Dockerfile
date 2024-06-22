FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive

# python 3.12
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.12 python3.12-dev python3.12-venv gcc g++ && \
    apt-get install -y curl && \
    apt-get clean 

WORKDIR /app

COPY . .

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12 && \
    pip3 install --ignore-installed wheel && \
    pip3 install --ignore-installed --no-cache-dir -r requirements.txt && \
    pip3 install gunicorn

ENV AZURE_OPENAI_API_KEY="1f815dde14ea4d9297a79352b9baa311"
ENV AZURE_OPENAI_API_ENDPOINT="https://pooropenai.openai.azure.com/"
ENV DEPLOYMENT="poorgpt"

ENV TRANSLATOR_TEXT_SUBSCRIPTION_KEY="052f433de075442cbe3a54039eb411bb"
ENV TRANSLATOR_TEXT_REGION="westeurope"
ENV TRANSLATOR_TEXT_ENDPOINT="https://api.cognitive.microsofttranslator.com/"

ENV PORT 8000

#CMD ["python3.12", "server.py"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "server:app"]
