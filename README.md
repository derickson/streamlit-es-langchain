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

You'll need to add some things to the secrest.toml file
```bash
HUGGINGFACEHUB_API_TOKEN="hf_YOUR_HUGGING_FACE_KEY"
LLAMA2_HF_URL="https://YOUR_ENDPOINT_URL.endpoints.huggingface.cloud"
```



## launch

```bash
streamlit run main_page.py
```

