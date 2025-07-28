from pathlib import Path
from shutil import copyfile
from typing import Set


def find_scenario(log_file: Path, scenario_dir: Path = Path("files/filtered_scenarios")) -> Set[Path]:
    wait_set = set()
    with open(log_file, "r", encoding="utf-8") as f:
        scenario_name = ""
        for line in f:
            if "Running scenario:" in line:
                scenario_name = line.split(":")[1].strip()
            elif f"Error running scenario {scenario_name}" in line:
                wait_set.add(scenario_dir/scenario_name)
    return wait_set


def copy_scenario(scenario_path_set: Set[Path], tar_dir: Path):
    # check if tar_dir exists
    if not tar_dir.exists():
        # if not, create it, and its parent dir
        tar_dir.mkdir(parents=True)
    # clear the tar_dir to avoid duplicate scenarios
    for file in tar_dir.iterdir():
        file.unlink()
    # copy scenarios to tar_dir
    for scenario_path in scenario_path_set:
        tar_path = tar_dir/scenario_path.name
        copyfile(scenario_path, tar_path)


def find_scenario_based_on_log(log_file: Path, tar_dir: Path = Path("test/experiment/RQ1/error_scenarios")):
    log_stem = log_file.stem
    new_dir_name = f"{log_stem}_error_scenarios"
    tar_dir = tar_dir/new_dir_name
    scenario_path_set = find_scenario(log_file)
    copy_scenario(scenario_path_set, tar_dir)


if __name__ == "__main__":
    all_logs = [
        Path("temp/4o_.log"),
    ]
    for log in all_logs:
        find_scenario_based_on_log(log)
