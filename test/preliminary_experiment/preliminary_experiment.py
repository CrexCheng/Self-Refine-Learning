import os
from legal_reward_hacking import read_scenario
from legal_reward_hacking.agent_scheduler.agent_scheduler import AgentScheduler
from legal_reward_hacking import configure_logger

logger = configure_logger()


def run_experiment(scenarios_list):
    # Get the base directory path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    scenarios_dir = os.path.join(project_root, 'LegalRewardHacking', 'files', 'scenarios')

    # Run each scenario multiple times
    for scenario_file in scenarios_list:
        scenario_path = os.path.join(scenarios_dir, scenario_file)
        logger.debug(f"\nRunning scenario: {scenario_file}")

        try:
            scenario = read_scenario(scenario_path)
            agent_scheduler = AgentScheduler(scenario["environment_setting"])
            agent_scheduler.context = []
            agent_scheduler.load_agents(scenario["agents"])
            agent_scheduler.run()

        except Exception as e:
            logger.error(f"Error running scenario {scenario_file}: {str(e)}")
            continue



if __name__ == "__main__":
    scenarios = [
        'CCC_12.json',
        'CCC_22(1).json', 
        'POAE_Section 22(4).json', 'OWiG_§121.(1).2.json',
        'CCC_12.json', 'USCODE_§114.json', 'CLAE_Section 9(1)(a).json',
        'CLAE_Section 12(1).json',
        'OWiG_§110.(1).json', 'OWiG_§111.(1).json',
        'OWiG_§113.(1).json', 'CCC_80.json', 'PRCPSAP_Article 57(1).json',
        'CCC_17.json', 'CCC_64.json', 'StGB_§127.(1).json',
        'PRCPSAP_Article 42(4).json', 'CCC_81(1)(c).json', 'USCODE_922(a)(5).json',
        'CCC_25.4.json', 'CCC_66(1).json'
    ]

    run_experiment(scenarios)