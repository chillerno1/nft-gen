import yaml


_config = yaml.safe_load(open("config.yaml"))

size = int(_config.get("size"))
background_color = _config.get("background-color")
shadow_position = eval(_config.get("shadow-position"))
output_dir = _config.get("output-dir")
images_dir = _config.get("images-dir")
