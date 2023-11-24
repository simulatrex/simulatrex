"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: json_utils.py
Description: Helpers for json

"""
import json
from typing import Any, Dict


class JSONHelper:
    @staticmethod
    def read_json(file_path: str) -> Dict[str, Any]:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def write_json(file_path: str, data: Dict[str, Any]) -> None:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
