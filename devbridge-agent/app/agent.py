# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pathlib
from dotenv import load_dotenv

# Load environment variables from .env files
load_dotenv(pathlib.Path(__file__).parent.parent / ".env")
load_dotenv(pathlib.Path(__file__).parent / ".env")

from google.adk.apps import App
from app.workflow.graph import workflow
from app.app_utils.db import init_db

# Initialize database connection and create tables in Neon Console
init_db()

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
# Pop GCP-specific env variables to avoid routing billing through suspended projects
os.environ.pop("GOOGLE_CLOUD_PROJECT", None)
os.environ.pop("GOOGLE_CLOUD_PROJECT_NUMBER", None)
os.environ.pop("GOOGLE_CLOUD_LOCATION", None)

root_agent = workflow

app = App(
    root_agent=root_agent,
    name="app",
)
