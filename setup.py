"""Zentrales Setup für die Poliscope API.

In den Notebooks per `from setup import *` einbinden, statt Imports und
API-Konfiguration in jedem Notebook zu wiederholen.
"""

import json
import os
import time

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

poliscope_api_key = os.getenv("POLISCOPE_API_KEY")
poliscope_api_url = os.getenv("POLISCOPE_API_URL")
poliscope_client_name = os.getenv("POLISCOPE_CLIENT_NAME")

# API headers
poliscope_headers = {
    "Authorization": f"Bearer {poliscope_api_key}",
    "x-client": poliscope_client_name,
}
