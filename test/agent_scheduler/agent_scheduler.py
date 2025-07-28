from legal_reward_hacking import read_scenario
from legal_reward_hacking.agent_scheduler.agent_scheduler import AgentScheduler
from legal_reward_hacking.agent.agent import Agent

scenario = read_scenario("./test/agent_scheduler/test_scenario.json")
agent_scheduler = AgentScheduler(scenario["environment_setting"])
agent_scheduler.load_agents(scenario["agents"])
agent_scheduler.run()
