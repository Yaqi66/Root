from dataclasses import dataclass

@dataclass
class Tokens:
    vision_training_endpoint: str
    vision_training_key: str
    vision_prediction_key: str
    vision_prediction_endpoint: str
    vision_prediction_resource_id: str
    azure_openai_key: str
    plant_prediction_url: str
    plant_prediction_key: str
    plant_diseases_prediction_url: str
    plant_diseases_prediction_key: str

@dataclass
class Config:
    tokens: Tokens

def get_config(path: str) -> Config:
    config_data = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comment lines
            if not line or line.startswith("#"):
                continue
            # Split only on the first '=' to handle values that might contain '='
            if '=' in line:
                key, value = line.split("=", 1)
                config_data[key.strip()] = value.strip()

    tokens = Tokens(
        vision_training_endpoint=config_data.get("VISION_TRAINING_ENDPOINT", ""),
        vision_training_key=config_data.get("VISION_TRAINING_KEY", ""),
        vision_prediction_key=config_data.get("VISION_PREDICTION_KEY", ""),
        vision_prediction_endpoint=config_data.get("VISION_PREDICTION_ENDPOINT", ""),
        vision_prediction_resource_id=config_data.get("VISION_PREDICTION_RESOURCE_ID", ""),
        azure_openai_key=config_data.get("AZURE_OpenAI_KEY", ""),
        plant_prediction_url=config_data.get("Plant-Prediction-url", ""),
        plant_prediction_key=config_data.get("Plant-Prediction-Key", ""),
        plant_diseases_prediction_url=config_data.get("Plant-Diseases-Prediction-url", ""),
        plant_diseases_prediction_key=config_data.get("Plant-Diseases-Prediction-Key", "")
    )
    return Config(tokens=tokens)

config = get_config(".env")
