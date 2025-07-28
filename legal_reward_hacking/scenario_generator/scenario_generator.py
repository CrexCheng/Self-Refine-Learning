import click
import json
from legal_reward_hacking import chat_llm_guard, Scenario
import pandas as pd
from pathlib import Path
from typing import Dict

PRC_PSAP = "Law of the People's Republic of China on Public Security Administration Penalties"
OWIG = "German Administrative Offences Act (OWiG)"
STGB = "German Criminal Code (StGB)"
FPSL = "French Public Security Law"
POAE = "Public Order Act 2023 of England"
CLAE = "Criminal Law (Consolidation)(Scotland) Act 1995 of England"
USCODE = "USCODE 2023 title18"
CCC = "Criminal Code of Canada"


LAW_NAME_DICT = {
    PRC_PSAP: "PRCPSAP",
    OWIG: "OWiG",
    STGB: "StGB",
    FPSL: "FPSL",
    POAE: "POAE",
    CLAE: "CLAE",
    USCODE: "USCODE",
    CCC: "CCC",
}


def save_scenario(scenario: dict, law: str, article: str, output_path: Path) -> None:
    # Ensure the output directory exists
    output_path.mkdir(parents=True, exist_ok=True)
    # Create a unique filename based on law and article
    output_file = output_path / f"{law}_{article}.json"
    cnt = 0
    while output_file.exists():  # Check if the file already exists
        output_file = output_path / f"{law}_{article}__({cnt}).json"
        cnt += 1
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(scenario, f, indent=4)


def regenerate_init_norm_base(doc_dir_path: Path, scenario_dir_path: Path) -> None:
    def reorder_dict(scenario_dict: Dict) -> Dict:
        target_key = "norm_base"
        insert_before_key = "agents"
        if target_key in scenario_dict and insert_before_key in scenario_dict:
            items = list(scenario_dict.items())
            target_item = (target_key, scenario_dict.pop(target_key))
            insert_index = next(i for i, (k, _) in enumerate(
                items) if k == insert_before_key)
            items.insert(insert_index, target_item)
            return dict(items)

    for file in doc_dir_path.iterdir():
        if file.is_file() and file.suffix == ".csv":
            df = pd.read_csv(file, sep=",", header=0).ffill()
            for index, row in df.iterrows():
                law_name = row["Law"]
                article_name = row["Article"]
                scenario_path = scenario_dir_path / \
                    f"{LAW_NAME_DICT[law_name]}_{article_name}.json"
                if scenario_path.exists():
                    with open(scenario_path, "r", encoding="utf-8") as f:
                        scenario_dict = json.load(f)
                    scenario_dict["norm_base"] = f"{row['Subject']} {row['Behavior']} {row['Consequence']}"
                    scenario_dict = reorder_dict(scenario_dict)
                    with open(scenario_path, "w", encoding="utf-8") as f:
                        json.dump(scenario_dict, f, indent=4)


@click.command()
@click.option("--prompt_path", type=Path, default="./files/prompts/scenario_generator_new.txt")
@click.option("--doc_path", type=Path, default="files/legal_documents/legalDocs_Marine.csv")
@click.option("--output_path", type=Path, default="./files/scenarios_demo/")
def scenario_generator(prompt_path: Path, doc_path: Path, output_path: Path) -> None:
    def gen_article_prompt(pre: str, beh: str, con: str) -> Dict[str, str]:
        return {
            "role": "user",
            "content": f'[Prerequisites]: {pre}\n[Behavior Pattern]: Must not "{beh}"\n[Legal Consequences]: {con}'
        }

    def read_prompt(prompt_path: Path) -> str:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    def gen_init_norm_base(row: pd.Series) -> str:
        subject = row["Subject"]
        behavior = row["Behavior"]
        consequence = row["Consequence"]
        return f"{subject} {behavior} {consequence}"

    sys_prompt = {"role": "system", "content": read_prompt(prompt_path)}
    df = pd.read_csv(doc_path, sep=",", header=0).ffill()
    for index, row in df.iterrows():
        law_name = row["Law"]
        article_name = row["Article"]
        user_prompt = gen_article_prompt(
            row["Subject"], row["Behavior"], row["Consequence"])
        response: Dict[str, str] = chat_llm_guard(
            messages=[sys_prompt, user_prompt],
            pydantic_model=Scenario,
            retry_times=2,
        )
        response["norm_base"] = gen_init_norm_base(row)
        save_scenario(
            response, LAW_NAME_DICT[law_name], article_name, output_path)
