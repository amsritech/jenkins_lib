import os
import yaml  # pip install pyyaml

def list_tags(root_dir: str):
    """
    Scan all immediate sub-folders of `root_dir`,
    locate an `inventory.yaml` file in each,
    and display the tags defined inside it.
    """
    for app_name in os.listdir(root_dir):
        app_path = os.path.join(root_dir, app_name)

        if not os.path.isdir(app_path):
            continue  # skip non-directories

        yaml_path = os.path.join(app_path, "inventory.yaml")

        if not os.path.isfile(yaml_path):
            print(f"{app_name}: No inventory.yaml found.")
            continue

        try:
            with open(yaml_path, "r") as f:
                data = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"{app_name}: Failed to parse YAML: {e}")
            continue

        tags = data.get("tags")

        if tags is None:
            print(f"{app_name}: No 'tags' key in inventory.yaml.")
        else:
            print(f"{app_name}: tags -> {tags}")


if __name__ == "__main__":
    ROOT_SITES_DIR = "sites"  # change path if needed
    list_tags(ROOT_SITES_DIR)