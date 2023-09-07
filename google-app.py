import vertexai
from vertexai.language_models import TextGenerationModel

vertexai.init(project="elastic-sa", location="us-central1")
parameters = {
    "temperature": 0.2,
    "max_output_tokens": 256,
    "top_p": 0.8,
    "top_k": 40
}
model = TextGenerationModel.from_pretrained("text-bison@001")
response = model.predict(
    """hello, what is in the news?""",
    **parameters
)
print(f"Response from Model: {response.text}")