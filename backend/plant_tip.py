import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from config import config

endpoint = "https://plant-tip.openai.azure.com/openai/deployments/gpt-4o-mini"
model_name = "gpt-4o-mini"
openAi_key = config.tokens.azure_openai_key

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(openAi_key),
)

plant_type = 'lemon tree'
soil_humidity = 0.3
air_humidity = 0.2
temperature = 23
soil_pH = 5

user_message = (
    f"My {plant_type} is showing signs of stress. "
    f"The soil humidity is {soil_humidity}, air humidity is {air_humidity}, soil pH is {soil_pH}"
    f"and the temperature is {temperature}°C. "
    "Can you provide one advice?"
)


response = client.complete(
    messages=[
        SystemMessage(content=(
            "You are a helpful home plant adviser who provides expert care tips for indoor plants. "
            "Please provide exactly three pieces of advice. "
            "Each piece of advice should be a short sentence ending with a relevant emoji."
        )),
        UserMessage(content=user_message)
    ],
    max_tokens=150,
    temperature=1.0,
    top_p=1.0,
    model=model_name
)

print(response.choices[0].message.content)