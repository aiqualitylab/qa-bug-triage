import os
import json
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag import search_bugs, init_store
from openai import OpenAI

DATASET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eval_dataset.json")
RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")