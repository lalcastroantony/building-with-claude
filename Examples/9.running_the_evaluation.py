import json

import building_with_claude.prompt_evaluation_and_engineering as pe


with open("dataset.json", "r") as f:
    dataset = json.load(f)

results = pe.run_eval(dataset)

with open("results.json", "w") as file:
    json.dump(results, file, indent=2)
