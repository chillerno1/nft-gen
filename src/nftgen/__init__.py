import os
import sys
from pathlib import Path
from shutil import copy2


def create_configs():
    copy_resource("config.yaml")
    copy_resource("attributes.yaml")
    Path("Assets").mkdir(parents=True, exist_ok=True)


def copy_resource(resource: str):
    destination = resource
    if not os.path.exists(destination):
        copy2(resource_path(resource), destination)
        print(f"Created {destination}")


def resource_path(resource: str) -> str:
    """ Returns the absolute path to a bundled resource """
    base_path = getattr(sys, '_MEIPASS')
    return os.path.join(base_path, os.path.join("resources", resource))


if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    create_configs()
