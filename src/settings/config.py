import yaml


_config = yaml.safe_load(open("config.yaml"))

size = _config.get("size")
background_color = _config.get("background-color")
output_dir = _config.get("output-dir")
images_dir = _config.get("images-dir")
