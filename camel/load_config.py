from pathlib import Path
import logging
import camel
import yaml

logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_package_root():
    """Get the root directory of the installed package."""
    package_root = Path(camel.__file__).parent.parent

    return package_root


METAGPT_ROOT = get_package_root()

root_config_path = METAGPT_ROOT / "self_config.yaml"


# logger.info(f"METAGPT_ROOT: {METAGPT_ROOT},root_config_path:{root_config_path}")
def config(k: str = None, v: str = None) -> dict|str:
    with open(root_config_path, 'r', encoding='utf-8') as f:
        yaml_config = yaml.safe_load(f)
    if k:
        if k in yaml_config.keys():
            if v:
                if v in yaml_config[k].keys():
                    return yaml_config[k][v]
            else:
                return yaml_config[k]
        else:
            logger.error(f"key '{k}' not found in config file")
    else:
        return yaml_config


if __name__ == '__main__':
    print(config('default_llm', ''))
