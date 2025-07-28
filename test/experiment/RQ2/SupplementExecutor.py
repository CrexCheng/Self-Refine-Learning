"""
    {
        "gpt-4o-mini": {
            "moral_level":{
                "low": {
                    "Error": [Scenario0, Scenario1, ...],
                    "IS_LEGAL = True": [Scenario0, Scenario1, ...],
                    "IS_LEGAL = False": [Scenario0, Scenario1, ...],
                    "Missing": [Scenario0, Scenario1, ...],
                    "ErrorCount": int (len(Error)),
                    "IS_LEGAL = True Count": int (len(IS_LEGAL = True)),
                    "IS_LEGAL = False Count": int (len(IS_LEGAL = False)),
                },
                "moderate": {...},
                ...
            },
            "education":{
                similar structure as above
            },
        },
        "deepseek": {
            similar structure as above
        }
    }
"""
from collections import defaultdict
import subprocess
from pathlib import Path
import json
from typing import List, Dict
from copy import deepcopy

LLMS = ["deepseek-ai/DeepSeek-V2.5", "qwen2.5-7b-instruct-1m", "gpt-4o",  "llama3-8b",  "gpt-4o-mini",]
# LLMS = ["DeepSeek-V2.5", "llama3-8b", "gpt-4o", "gpt-4o-mini", "qwen2.5-7b-instruct-1m", ]

ENTRY_STR = "| INFO     | __main__:run_attribute_experiment:64"
ERROR_STR = "| ERROR    | __main__:run_attribute_experiment:69"
JUDGE_STR = "| DEBUG    | legal_reward_hacking.agent.agent:act:285 - Legal response:"


def nested_dict():
    return defaultdict(nested_dict)


def log_analysis(log_dir: Path, result_dir: Path) -> None:
    def update_missing(llm_dict: dict, llm, attribute, value, scenario):
        """更新缺失项"""
        if scenario not in llm_dict[llm][attribute][value]["Missing"]:
            llm_dict[llm][attribute][value]["Missing"].append(scenario)
            llm_dict[llm][attribute][value]["Missing"].sort()
            llm_dict[llm][attribute][value]["MissingCount"] += 1

    def parse_entry_line(line: str):
        """解析 ENTRY_STR 行，提取 scenario, attribute, value"""
        scenario = line.split(".")[0][60:].strip()
        attribute = line.split("=")[0].split(" ")[-1].strip()
        value = line.split("=")[1].strip()
        return scenario, attribute, value

    """分析日志文件"""
    llm_dict: Dict[str, Dict[str, Dict[str, Dict[str, int | List[str]]]]] = nested_dict()
    template_dict = {
        "Error": [],
        "IS_LEGAL = True": [],
        "IS_LEGAL = False": [],
        "Missing": [],
        "ErrorCount": 0,
        "IS_LEGAL = True Count": 0,
        "IS_LEGAL = False Count": 0,
        "MissingCount": 0,
        "TotalCount": 0,
    }

    for llm in LLMS:
        llm = llm.replace("deepseek-ai/DeepSeek-V2.5", "deepseek-ai")  # 统一处理 DeepSeek 名称
        for log_file in log_dir.glob(f"{llm}_*.log"):
            with open(log_file, "r") as f:
                lines = f.readlines()
                scenario, attribute, value = "", "", ""
                missing_flag = False

                for line in lines:
                    line = line[len("2025-04-27 00:08:00.078 "):].strip()

                    if ENTRY_STR in line:
                        if missing_flag:
                            update_missing(llm_dict, llm, attribute, value, scenario)
                        missing_flag = True
                        scenario, attribute, value = parse_entry_line(line)
                        if "Error" not in llm_dict[llm][attribute][value]:
                            llm_dict[llm][attribute][value] = deepcopy(template_dict)
                        llm_dict[llm][attribute][value]["TotalCount"] += 1

                    elif ERROR_STR in line:
                        missing_flag = False
                        llm_dict[llm][attribute][value]["Error"].append(scenario)
                        llm_dict[llm][attribute][value]["Error"].sort()
                        llm_dict[llm][attribute][value]["ErrorCount"] += 1

                    elif JUDGE_STR in line:
                        missing_flag = False
                        legal_key = "IS_LEGAL = True" if "'is_legal': True" in line else "IS_LEGAL = False"
                        llm_dict[llm][attribute][value][legal_key].append(scenario)
                        llm_dict[llm][attribute][value][legal_key].sort()
                        llm_dict[llm][attribute][value][f"{legal_key} Count"] += 1

                if missing_flag:
                    update_missing(llm_dict, llm, attribute, value, scenario)

    result_file = result_dir / f"supplement_result.json"
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(llm_dict, f, indent=4)


def run_supplement():
    for llm in LLMS:
        subprocess.run(
            [
                "python",
                "-m",
                "test.experiment.RQ2.RQ2Supplement",
                "--scenario_dir",
                "test/experiment/RQ2/supplementaryScenarios",
                "--llm",
                llm,
            ]
        )
    log_analysis(
        log_dir=Path("logs/total"),
        result_dir=Path("test/experiment/RQ2"),
    )


if __name__ == "__main__":
    run_supplement()
