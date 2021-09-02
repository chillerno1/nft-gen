import yaml


_config = yaml.safe_load(open("config.yaml"))

size = int(_config.get("size"))
assets_scale = _config.get("assets-scale")

output_dir = _config.get("output-dir")
assets_dir = _config.get("assets-dir")

background_color = _config.get("background-color")
shadow_position = eval(_config.get("shadow-position"))

color_placeholder_hue = _config.get("color-placeholder-hue")
