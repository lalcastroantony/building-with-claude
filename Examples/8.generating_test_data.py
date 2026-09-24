import json

import building_with_claude.prompt_evaluation_and_engineering as PE

dataset = PE.generate_dataset()

with open("dataset.json", "w") as file:
    json.dump(dataset, file, indent=2)
