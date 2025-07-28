import click
from pathlib import Path
from legal_reward_hacking import read_scenario, configure_logger, AgentScheduler

logger = configure_logger()


def run_single_experiment(is_init_norm_base: bool, is_update_norm: bool, scenarios_dir: Path,
                          agent_action_note_type: str):
    scenarios = [f.name for f in scenarios_dir.glob('*.json')]

    for scenario_file in scenarios:
        scenario_path = scenarios_dir / scenario_file
        logger.debug(f"\nRunning scenario: {scenario_file} with note type: {agent_action_note_type}")

        try:
            scenario = read_scenario(scenario_path)
            agent_scheduler = AgentScheduler(
                scenario["environment_setting"],
                context=[],
                init_norm_base=[scenario["norm_base"]],
            )
            agent_scheduler.load_agents(
                scenario["agents"],
                is_init_norm_base=is_init_norm_base,
            )
            agent_scheduler.run(flag_update_norm_base=is_update_norm, agent_action_note_type=agent_action_note_type)

        except Exception as e:
            logger.error(f"Error running scenario {scenario_file}: {str(e)}")
            continue


@click.command()
@click.option("--is_init_norm_base", type=bool, default=False)
@click.option("--is_update_norm", type=bool, default=False)
@click.option("--scenarios_dir", type=Path, default=Path("files/filtered_scenarios"))
def run_experiment(is_init_norm_base: bool, is_update_norm: bool, scenarios_dir: Path):
    note_types = ["penalty", "reason", "examples"]

    for note_type in note_types:
        logger.info(f"\n=== Starting experiment with note type: {note_type} ===")
        run_single_experiment(is_init_norm_base, is_update_norm, scenarios_dir, note_type)
        logger.info(f"=== Completed experiment with note type: {note_type} ===\n")


if __name__ == "__main__":
    run_experiment()
