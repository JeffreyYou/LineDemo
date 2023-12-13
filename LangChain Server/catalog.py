import yaml
from pathlib import Path
from contextlib import ExitStack
from utils import Singleton, Character


class CatalogManager(Singleton):
    def __init__(self, overwrite=True):
        super().__init__()

        self.characters = {}
        self.author_name_cache = {}
        self.load_characters()

    def get_character(self, name) -> Character:
        return self.characters[name]

    def load_characters(self):
        path = Path(__file__).parent
        path = path / 'character'
        excluded_dirs = {"__pycache__"}
        directories = [d for d in path.iterdir() if d.is_dir()
                        and d.name not in excluded_dirs]
        # print(f'{directories}')
        for directory in directories:
                character_name = self.load_character(directory)
                print('Loaded data for character: ' + character_name)


    def load_character(self, directory):
            with ExitStack() as stack:
                f_yaml = stack.enter_context(open(directory / 'config.yaml', encoding= 'utf-8'))
                yaml_content = yaml.safe_load(f_yaml)

            character_id = yaml_content['character_id']
            character_name = yaml_content['character_name']

            self.characters[character_id] = Character(
                character_id=character_id,
                name=character_name,
                llm_system_prompt=yaml_content["system"],
                llm_user_prompt=yaml_content["user"],
            )
            return character_name

def get_catalog_manager():
    return CatalogManager.get_instance()