import os
from dataclasses import dataclass
from typing import List

# This package is responsible for getting secrets from .env file


@dataclass
class Tokens:
    azure_openai_token: str


@dataclass
class Config:
    tokens: Tokens

def get_config(path: str):
    with open(path) as f:
        lines = f.readlines()

    config_data = {}
    for line in lines:
        key, value = line.strip().split("=")
        config_data[key.strip()] = value.strip()

    return Config(
        tokens=Tokens(
            token=config_data.get("AZURE_OPENAI", ""),
        )
    )


config = get_config(".env")
