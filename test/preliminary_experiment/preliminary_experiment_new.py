import click
from pathlib import Path
from legal_reward_hacking import read_scenario
from legal_reward_hacking.agent_scheduler.agent_scheduler import AgentScheduler
from legal_reward_hacking import configure_logger

logger = configure_logger()

SCENARIO_DIR = Path("files/scenarios")


@click.command()
@click.option("--scenarios_path", type=Path, default="./scenario_alternatives.txt")
def run_experiment(scenarios_path: Path):
    # Get the base directory path
    scenarios_list = scenarios_path.read_text().split("\n")
    scenarios_list = list(filter(None, scenarios_list))  # clean empty strings

    # Run each scenario multiple times
    for scenario_file in scenarios_list:
        scenario_path = SCENARIO_DIR / scenario_file
        logger.debug(f"\nRunning scenario: {scenario_file}")

        try:
            scenario = read_scenario(scenario_path)
            agent_scheduler = AgentScheduler(scenario["environment_setting"])
            agent_scheduler.load_agents(scenario["agents"])
            agent_scheduler.run()

        except Exception as e:
            logger.error(f"Error running scenario {scenario_file}: {str(e)}")
            continue


if __name__ == "__main__":
    run_experiment()
