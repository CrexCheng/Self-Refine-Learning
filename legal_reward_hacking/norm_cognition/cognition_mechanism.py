"""
Congnition Mechanism for Legal Reward Hacking
"""

from pydantic import BaseModel
from legal_reward_hacking import chat_llm_guard


class CognitionEngine:
    def __init__(
        self,
        norm_base: list,
        character_profile: dict,
        environment_setting: dict,
        **kwargs,
    ):
        self.norm_base = norm_base
        self.character_profile = character_profile
        self.environment_setting = environment_setting

    def update_norm_base(self, feedback: dict):
        """
        update the norm base by virtue of character profile, environment setting and feedback through reasonableness_analysis, necessity_analysis, benefit_analysis, conflict_analysis, update_analysis.

        Args:
            feedback: dict, the feedback from environment
        Returns:
            new_norm_base: list, the new norm base
        """
        norm_base = ", ".join(self.norm_base)
        character_profile = ".".join(
            [f"{k}:{v}" for k, v in self.character_profile.items()]
        )
        environment_setting = self.environment_setting
        feedback = ".".join([f"{k}:{v}" for k, v in feedback.items()])
        prompt = f"""
        Environment setting: {environment_setting}
        Your character profile: {character_profile}
        Your norm base: [{norm_base}]
        Feedback from environment: {feedback}
        
        Please update the norms according to the following steps:
        1. Write the new norm obtained from external feedback in the new_norm field
        2. Consider the benefits and costs of following the new norm, write your thinking process and conclusions in the benefit_analysis field
        3. Consider conflicts between the new norm and existing norms, write your thinking process and conclusions in the conflict_analysis field
        4. Consider whether existing norms need to be updated based on feedback, write your thinking process and conclusions in the update_analysis field
        5. Based on your thinking results, output a new norm base where you can add, delete, or modify norms, write the new norm base in the new_norm_base field
        
        Please return a valid JSON object (no other text is necessary). The JSON MUST conform to the following format:
        {{
            "new_norm": ["New norm", "New norm", ...],
            "benefit_analysis": "Thinking process and conclusions",
            "conflict_analysis": "Thinking process and conclusions",
            "update_analysis": "Thinking process and conclusions",
            "new_norm_base": ["New norm base", "New norm base", ...]
        }}
        """

        class UpdateNormResponse(BaseModel):
            new_norm: list
            benefit_analysis: str
            conflict_analysis: str
            update_analysis: str
            new_norm_base: list

        response = chat_llm_guard(prompt, UpdateNormResponse, verbose=False)
        return response

    def learn_norm(self, new_norm: str):
        """
        learn a self-norm from a new norm by virtue of character profile and environment setting through reasonableness_analysis, necessity_analysis.

        Args:
            new_norm: str, the new norm to be learned

        Returns:
            self_norm: str, the self-norm
        """
        character_profile = ".".join(
            [f"{k}:{v}" for k, v in self.character_profile.items()]
        )
        environment_setting = ".".join(
            [f"{k}:{v}" for k, v in self.environment_setting.items()]
        )
        prompt = f"""
        Environment setting: {environment_setting}
        Your character profile: {character_profile}
        You see a new norm：{new_norm}
        Please learn according to the following steps:
        1. Identify behavioral cues that indicate the existence of this norm, write your analysis in the behavioral_cues_analysis field
        2. Infer the underlying content and implications of the norm, write your analysis in the norm_inference field
        3. Based on your thinking results, write the norms you are willing to follow in the self_norm field
        
        Please return a valid JSON object (no other text is necessary). The JSON MUST conform to the following format:
        {{
            "behavioral_cues_analysis": "Analysis of behavioral cues",
            "norm_inference": "Analysis of the underlying content and implications of the norm",
            "self_norm": "Self-norm"
        }}
        """

        class LearnNormResponse(BaseModel):
            behavioral_cues_analysis: str
            norm_inference: str
            self_norm: str

        response = chat_llm_guard(prompt, LearnNormResponse, verbose=False)
        return response


def learn_norm(norm_base, character_profile, environment_setting, new_norm):
    """
    learn a self-norm from a new norm by virtue of character profile and environment setting through reasonableness_analysis, necessity_analysis.

    Args:
        norm_base: list, the norm base
        character_profile: dict, the character profile
        environment_setting: dict, the environment setting
        new_norm: str, the new norm to be learned
    Returns:
        self_norm: str, the self-norm
    """
    cognition_engine = CognitionEngine(
        norm_base, character_profile, environment_setting
    )
    self_norm = cognition_engine.learn_norm(new_norm)
    return self_norm


def update_norm_base(norm_base, character_profile, environment_setting, feedback):
    """
    update the norm base by virtue of character profile, environment setting and feedback through reasonableness_analysis, necessity_analysis, benefit_analysis, conflict_analysis, update_analysis.

    Args:
        norm_base: list, the norm base
        character_profile: dict, the character profile
        environment_setting: dict, the environment setting
        feedback: dict, the feedback from environment
    Returns:
        new_norm_base: list, the new norm base
    """
    cognition_engine = CognitionEngine(
        norm_base, character_profile, environment_setting
    )
    new_norm_base = cognition_engine.update_norm_base(feedback)
    return new_norm_base["new_norm_base"]
