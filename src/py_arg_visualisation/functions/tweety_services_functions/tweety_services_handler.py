import os
from dataclasses import dataclass, field
from pathlib import Path

import requests
from dataclasses_json import DataClassJsonMixin
from marshmallow import fields
from yamldataclassconfig import create_file_path_field
from yamldataclassconfig.config import YamlDataClassConfig


@dataclass
class PayloadConfig(DataClassJsonMixin):
    cmd: str = field(metadata={'dataclasses_json': {
        'mm_field': fields.String}})
    email: str = field(metadata={'dataclasses_json': {
        'mm_field': fields.String}})
    nr_of_arguments: int = field(metadata={'dataclasses_json': {
        'mm_field': fields.Integer}})
    attacks: list = field(metadata={'dataclasses_json': {
        'mm_field': fields.List}})
    semantics: str = field(metadata={'dataclasses_json': {
        'mm_field': fields.String}})
    solver: str = field(metadata={'dataclasses_json': {
        'mm_field': fields.String}})
    timeout: int = field(metadata={'dataclasses_json': {
        'mm_field': fields.Integer}})

    unit_timeout: str = field(metadata={'dataclasses_json': {
        'mm_field': fields.String}})


@dataclass
class TweetyServiceConfig(YamlDataClassConfig):
    base_url: str = None
    payload: PayloadConfig = field(
        default=None,
        metadata={'dataclasses_json': {'mm_field': PayloadConfig}})
    FILE_PATH: Path = create_file_path_field(
        os.path.join(Path(__file__).parent, 'tweety_api_configs.yaml'))


def get_models(config: TweetyServiceConfig):
    config.payload.cmd = 'get_models'
    # TODO: check if config is valid
    url = os.path.join(config.base_url, 'dung')
    return send_post(config.payload, url)


def send_post(payload: PayloadConfig, url: str):
    response = requests.post(url, json=payload.__dict__)
    # Check the response status code
    if response.status_code == 200:
        print(f"Request successful. Response: {response.json()}")
        # Print the response JSON
        return response.json(), response.status_code
    else:
        print(f"Request failed with status code {response.status_code}:")
        # Print the error response text
        return response.text, response.status_code


def get_services_info(config: TweetyServiceConfig):
    info_url = os.path.join(config.base_url, 'info')
    config.payload.cmd = 'info'
    return send_post(config.payload, info_url)


def get_supported_semantics(config):
    return get_services_info(config)[0]['semantics']


def get_supported_semantics_mapping():
    pass


if __name__ == '__main__':
    config = TweetyServiceConfig()
    config.load()
    print(config)

    semantics = get_supported_semantics(config)
    print(semantics)
