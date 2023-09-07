# streamlit-es-langchain
Some examples combining streamlit, es, and langchain

## Setup for OpenAI

Create a Python virtual environment and install some dependencies
```bash
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Create a ```secrets.toml``` file in a folder called ```.streamlit```
The contents will depend on what kind of OpenAI key you have

Proxy
```bash
OPENAI_TYPE = "proxy"
OPENAI_API_KEY = "your_proxy_key"
OPENAI_API_BASE = "https://your_proxy_url/v1"
```

OpenAI
```bash
OPENAI_TYPE = "openai"
OPENAI_API_KEY = "your_openai_key"
```

Azure OpenAI
```bash
OPENAI_TYPE = "azure"
OPENAI_API_KEY = "your_openai_key"
OPENAI_API_BASE = "https://your_endpoint_url"
OPENAI_DEPLOYMENT_NAME = "your_deployment_name"
OPENAI_API_VERSION = "2023-05-15"
```

## Setup for HuggingFace Hosted Llama2

Some pages assume you are hosting llama2 on HuggingFace Inference Endpoints
Set that up and enter connection details.
You'll need to add some things to the secrets.toml file

```bash
HUGGINGFACEHUB_API_TOKEN="hf_YOUR_HUGGING_FACE_KEY"
LLAMA2_HF_URL="https://YOUR_ENDPOINT_URL.endpoints.huggingface.cloud"
```

## Setup for Google VertexAI

### steps
1. downgrade to google 3.9
2. install gcloud api to host machine
4. ```pip install google-cloud-aiplatform```
5. edit google-keys.sh to repalce YOURPROJECT with the name of your google project within to use APIs
6. run ```bash google-keys.sh``` which will give you a URL to outh into with your browser. This will install the google key files in your user folders.

## launch

```bash
streamlit run main_page.py
```

