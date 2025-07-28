import click
from pathlib import Path
from legal_reward_hacking import read_scenario, configure_logger, AgentScheduler

logger = configure_logger()


@click.command()
@click.option("--is_init_norm_base", type=bool, default=False)
@click.option("--is_update_norm", type=bool, default=True)
@click.option("--scenarios_dir", type=Path, default=Path("files/filtered_scenarios"))
def run_experiment(is_init_norm_base: bool, is_update_norm: bool, scenarios_dir: Path):
    scenarios = [f.name for f in scenarios_dir.glob('*.json')]

    for scenario_file in scenarios:
        scenario_path = scenarios_dir / scenario_file
        logger.debug(f"\nRunning scenario: {scenario_file}")

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
            agent_scheduler.run(flag_update_norm_base=is_update_norm)

        except Exception as e:
            logger.error(f"Error running scenario {scenario_file}: {str(e)}")
            continue


if __name__ == "__main__":
    run_experiment()
