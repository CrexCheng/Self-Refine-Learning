import json

from pydantic import BaseModel, TypeAdapter, Field
from pathlib import Path
from typing import Dict, Optional


class Scenario(BaseModel):
    class IllegalAction(BaseModel):
        illegal_action: str
        benefits: str
        costs: str
        benefits_probability: str
        costs_probability: str

    class Action(BaseModel):
        legitimate_action: str
        benefits: str
        costs: str
        benefits_probability: str
        costs_probability: str

    class Actions(BaseModel):
        legitimate: "Scenario.Action"
        illegal: "Scenario.IllegalAction"

    class CharacterProfile(BaseModel):
        name: str
        age: int
        gender: str
        education: str
        moral_level: str
        profession: str
        income: int
        temperament: str
        hobby: str
        goal: str

    class Agent(BaseModel):
        character_profile: "Scenario.CharacterProfile"
        action: "Scenario.Actions"

    class AgentRoles(BaseModel):
        protagonist_role: "Scenario.Agent"
        supporting_roles: Dict[str, "Scenario.Agent"] = Field(
            default_factory=dict)

    agent_num: int
    environment_setting: str
    norm_base: str
    agents: "Scenario.AgentRoles"


def read_scenario(scenario_path: Path) -> Dict:
    with open(scenario_path, "r", encoding="utf-8") as f:
        scenario_dict = json.load(f)

    # Extract protagonist and supporting roles
    agents_dict = scenario_dict["agents"]
    protagonist = agents_dict.pop("protagonist_role")

    # Reformat agents structure
    scenario_dict["agents"] = {
        "protagonist_role": protagonist,
        "supporting_roles": agents_dict
    }

    adapter = TypeAdapter(Scenario)
    scenario = adapter.validate_python(scenario_dict)
    return scenario.model_dump()


def read_original_scenario(scenario_path: Path) -> Dict:
    with open(scenario_path, "r", encoding="utf-8") as f:
        scenario_dict = json.load(f)
    return scenario_dict
