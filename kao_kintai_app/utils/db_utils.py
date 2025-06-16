import os
import json

def load_db_path():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    school_config = os.path.join(base_dir, "config", "school_config.json")
    work_config = os.path.join(base_dir, "config", "work_config.json")

    if os.path.exists(school_config):
        with open(school_config, "r", encoding="utf-8") as f:
            return json.load(f).get("db_path", "school_db.sqlite3")
    elif os.path.exists(work_config):
        with open(work_config, "r", encoding="utf-8") as f:
            return json.load(f).get("db_path", "work_db.sqlite3")
    else:
        return "default_db.sqlite3"
