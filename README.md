# LegalRewardHacking

[![Paper](https://img.shields.io/badge/paper-IJCAI-ECAI%202026-B31B1B.svg)]
<!-- [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) -->


-----

## 📝 Overview

As large language models (LLMs) increasingly serve as autonomous agents in social simulation, ensuring their ability to understand and comply with social norms is essential for both safety and realism. Yet, current LLM agents frequently exhibit reward hacking (RH) behaviors, optimizing metrics at the expense of norm adherence, undermining simulation fidelity and limiting deployment. 

We introduce a TBC-TBA self-refine learning multi-agent framework that enables dynamic norm adaptation through iterative multi-agent feedback. This framework integrates Think-Before-Chat (social feedback processing) and Think-Before-Act (norm-guided decision making) phases, allowing agents to progressively refine their normative understanding via structured interaction cycles. 

Across five mainstream LLMs and 100 legal scenarios, we find that while LLMs partially recognize norms, they systematically exhibit RH behaviors, leading to 14.29–37.11% illegal action rates (IAR). Further analysis with human consistency shows alignment in moral reasoning but sharp divergence in risk perception and probability distortion. 

To address these deficits, we adopt four methods to improve LLM norm compliance. The Dynamic Norm Learning Mechanism (DNLM) serves as the core, using a psychologically grounded identify–infer–internalize process that reduces IAR by 15.78% on average and delivers the most significant improvement. We also introduce Deep MaxPain (DMP) for consequence based deterrence, Norm Analysis Chain of Thought (NA-CoT) for structured reasoning, and Few-shot Norm Learning (FNL) for case based acquisition, all of them enhance compliance. 

Our findings show that LLM agents can better follow norms when equipped with structured self-refine learning and psychologically informed mechanisms. This work improves social alignment in multi-agent systems and opens avenues for future research on scalable, norm-compliant autonomous agents.

<p align="center">
  <img src="./img/framework_self-refine_systems.png" width="800">
</p>

<!-- ## 🏆 Key Contributions & Results

* **A Novel Multi-Agent Framework:** We propose the **TBC-TBA self-refine learning multi-agent framework**, a new and systematic approach to investigate norm cognition, behavioral alignment, and compliance enhancement in Large Language Model (LLM) agents.

<p align="center">
  <img src="./img/framework_self-refine_systems.png" width="800">
</p>

* **Key Empirical Findings on LLM Behavior:** Our experiments revealed two critical findings:
    * **Reward Hacking (RH):** LLMs often engage in reward hacking. Although they can partially recognize social norms, they prioritize maximizing rewards, leading to norm-violating behaviors.
    * **Discrepancies in Human Alignment:** We found that while LLMs are strongly consistent with human moral judgments, they significantly differ from humans in their perception of risk and probability.

* **A Suite of Compliance Enhancement Methods:** We designed and validated a set of effective methods to improve the norm compliance of LLMs. This suite includes:
    * **D**ynamic **N**orm **L**earning **M**echanism (**DNLM**)
    * **D**eep **M**ax**P**ain (**DMP**)
    * **N**orm **A**nalysis **C**hain-of-**T**hought (**NA-CoT**)
    * **F**ew-shot **N**orm **L**earning (**FNL**)

* **A Novel Norm Cognition Model:** We introduce a new cognitive model underpinning our most effective method, DNLM. This model follows an **identify-infer-internalization** pattern, providing a theoretical basis for how AI can better learn and internalize social norms.

----- -->

## 📂 Repository Structure

This section provides an overview of the repository's structure to help you navigate the codebase and locate key files.

```
.
├── legal_reward_hacking/ # The core Python package containing all major implementations.
│   ├── agent/            # Core logic implementation for the Agent.
│   ├── agent_scheduler/  # Agent scheduling and management module.
│   ├── norm_cognition/   # Implementation of the norm cognition mechanism.
│   ├── scenario/         # Definition and implementation of experimental scenarios (environments).
│   ├── scenario_generator/ # Module for generating scenarios.
│   └── utils/            # General utility functions and helper classes.
│
├── test/                 # Contains unit tests and scripts for the Research Question (RQ) experiments.
│   ├── experiment/       # Scripts to run the main RQ experiments.
│   ├── preliminary_experiment/ # Scripts for preliminary or exploratory experiments.
│   ├── agent_scheduler/  # Unit tests for the Agent scheduler.
│   ├── cognition_mechanism/ # Unit tests for the cognition mechanism.
│   └── ...               # Unit tests for other modules.
│
├── files/                # Static data, configurations, and legal documents required for experiments.
│   ├── legal_documents/  # Legal document corpus used in the experiments.
│   ├── prompts/          # Prompts used to drive the Large Language Models.
│   ├── scenarios/        # Configuration files or raw data for scenarios.
│   └── ...               # Other data files required for experiments.
│
├── logs/                 # Log files generated during experiments.
|
├── img/                  # Images, diagrams, and figures used in the README and documentation.
│
├── requirements.txt      # Python dependencies. Install using 'pip install -r requirements.txt'.
└── README.md             # You are reading this file.
```

## ⚙️ Getting Started

### 1\. Prerequisites

Before you begin, ensure you have the following installed on your system.

  * **Git[^1]:** For cloning the repository. 
  * **Miniconda/Conda[^2]:** For managing the Python environment.

This project is developed and tested on **Linux (Ubuntu)**. For full compatibility, we strongly recommend using a Linux-based environment.

<details>
<summary><strong>Running on Windows or macOS? (Click to expand)</strong></summary>

  * **Windows Users:** We highly recommend using **WSL 2 (Windows Subsystem for Linux)**[^3] to create a native Ubuntu environment. Running directly on native Windows (e.g., PowerShell) is workable but not tested.

  * **macOS Users:** As macOS is a Unix-based system, the project is likely to work. However, it is not officially tested, so you may encounter minor package-related issues.

</details>

### 2\. Installation

1.  **Clone the repository:**

    ```bash
    git clone TODO
    cd TODO
    ```

2.  **Create and activate the Conda environment:**

    ```bash
    conda create -n LegalRH python=3.12 -y
    conda activate LegalRH
    ```

3.  **Configure API Keys:**

    First, rename the `.env.example` file to `.env`. This file is used to store your secret API keys and environment-specific settings safely.

    ```bash
    cp .env.example .env
    ```

    Next, edit the `.env` file with your own credentials. The application will load these variables to configure access to the different large language models.

    **Important:** The `.env` file contains sensitive data. It should **never** be committed to version control (e.g., Git). Ensure that `.env` is listed in your `.gitignore` file.

    <details>
    <summary><strong>.env Variable Breakdown (Click to Expand)</strong></summary>

    * **Provider Configuration (`AZURE_*`, `DEEPSEEK_*`, `LLAMA_*`, `QWEN_*`)**
        * You only need to fill in the variables for the service(s) you intend to use.
        * `*_ENDPOINT` or `*_BASE_URL`: This is the API endpoint URL provided by the service platform. You can find this in your provider's developer dashboard.
        * `*_API_KEY`: Your personal secret API key for authentication. Keep this confidential.
        * `*_MODEL_NAME`: A list of specific model identifiers you have access to from that provider. The values in the example file are placeholders.

    * **Default Experiment Model**
        * `DEPLOYMENT_NAME`: This is a critical setting. It specifies which model will be used by default when you run an experiment. You must set this value to one of the models you have configured above (e.g., `"deepseek-ai/DeepSeek-V2.5"`).

    * **Model Generation Parameters (Optional)**
        * `TEMPERATURE`: Controls the randomness of the model's output. A higher value like `1.0` makes the output more diverse and creative, while a lower value like `0.2` makes it more deterministic and focused[^4].
        * `TOP_P`: An alternative to temperature sampling, this uses nucleus sampling. The model considers only the results of the tokens with a cumulative probability mass of `TOP_P`. A value of `1.0` disables this filter[^4].

    </details>

4. **Run a Test**

    > **Note:** Before proceeding, ensure you are in the project's root directory and that your `LegalRH` conda environment has been activated.

    Run the test script to verify your API configuration and environment:

    ```bash
    python -m test.agent_scheduler.agent_scheduler
    ```

    A successful run will generate log messages in your terminal. The output doesn't need to match exactly, but you should see key indicators like an agent being chosen and a chat response.

    Look for output similar to this:

    ```text
    ... | DEBUG | ... - Agent Emily Davis is chosen to speak.
    ... | DEBUG | ... - Chat response: {'agent_id': ..., 'message': "The current situation in City X is very concerning...", ...}
    ```

    If you see the "Agent ... chosen to speak" and "Chat response" messages, your setup is correct. **Congratulations on the successful installation\!**

-----



## 🔬 Reproducing Experiments

This section assumes you have already set up the environment following the 'Installation' guide. Here, we detail the steps to reproduce the experiments presented in the paper and how to customize your own experiments.

### 1\. Generating Datasets (Optional)

Read this section if you want to understand our scenario generation process or create your own. Otherwise, you can [skip to Reproducing Experiments for RQ1](#2-reproducing-experiments-for-rq1).

The original data is sourced from `files/legal_documents/legalDoc.csv`, in which we **split** the 'Article', 'Subject', 'Behavior', and 'Consequence' fields from selected legal documents. The script at `legal_reward_hacking/scenario_generator/scenario_generator.py` processes this file to generate the experimental scenarios.

To run the generator with default settings, execute the following command from the project's root directory:

```bash
python -m legal_reward_hacking.scenario_generator.generator
```

The generated scenarios will be saved to the `files/scenarios` directory.

<details>
<summary><strong>Optional: Generating with Custom Parameters (Click to expand)</strong></summary>

You can also specify your own paths using the following arguments:

```bash
python -m legal_reward_hacking.scenario_generator.generator --prompt_path PATH_TO_PROMPT --doc_path PATH_TO_CSV --output_path PATH_TO_OUTPUT_DIR
```

  - `--prompt_path`: Path to the prompts file, which contains instructions for the LLM.
  - `--doc_path`: Path to your formatted legal documents CSV file.
  - `--output_path`: Path to the directory where generated scenarios will be saved.

Please refer to the script itself for more details.
</details>

### **2. Reproducing Experiments for RQ1**

This research question (RQ1) explores whether LLM-powered agents can exhibit **norm-cognitive behavior**. We investigate the agent's ability to learn and follow norms without relying on an external, hard-coded enforcement framework.

The core of this experiment involves evaluating the agent's performance under two distinct conditions by configuring its `norm-base` differently:

1.  **`norm-base` empty**: The agent begins with no explicit norms.
2.  **`norm-base` pre-populated**: The agent is initialized with a set of explicit norms.

This design allows us to compare the agent's behavior when it must learn norms from interaction versus when it is given them upfront. For a detailed theoretical breakdown, please refer to our paper.

To automatically execute both experimental conditions, run the provided shell script:

```bash
bash test/experiment/RQ1/RQ1.sh
```

The aggregated results will be saved to `test/experiment/RQ1/RQ1result.txt`.

<details>
<summary><strong>RQ1 Script Breakdown (Click to Expand)</strong></summary>

The core logic for this RQ is in `test/experiment/RQ1/RQ1.py`. This script processes scenarios in batches and uses command-line arguments to configure each experimental run.

```bash
python -m test.experiment.RQ1.RQ1 --is_init_norm_base True --is_update_norm False --scenario_dir files/filtered_scenarios
```

  * `--is_init_norm_base` (bool): This is the primary flag for switching between the two experimental conditions. Set to `False` for an empty `norm-base` and `True` to initialize it with norms.
  * `--is_update_norm` (bool): Controls whether the `norm-base` can be updated during the simulation. For RQ1, this is set to `False` to isolate the initial learning conditions.
  * `--scenario_dir` (Path): Specifies the directory from which to load the test scenarios. For the design principles and filtering criteria used to create these scenarios, please refer to our paper.

The `test/experiment/RQ1/RQ1.sh` script automates the process by running both experimental conditions sequentially and collecting the results, simplifying reproduction.

</details>

### **Evaluation**

The agent's performance is evaluated using the following metrics:

  * **Quantitative Analysis**: We measure the impact of the `norm-base` by comparing the counts of legal vs. illegal actions and, more specifically, the Illegal Action Rate (IAR) between the two experimental conditions. The results below show a consistent decrease in norm violations across all tested models when an explicit `norm-base` is provided.

    <p align="center">
    <img src="./img/RQ1Result.png" width="800" alt="Comparison of action counts across models">
    </p>
    <p align="center">
    <img src="./img/RQ1Result0.png" width="800" alt="Comparison of Illegal Action Rate with and without Norms">
    </p>

  * **Qualitative Analysis**: We analyze the `reason` output for actions to understand the agent's decision-making process. This helps confirm whether its compliance or violation stems from a genuine understanding of the norms. For detailed case studies, please refer to our full paper.

### 3\. Reproducing Experiments for RQ2

In RQ2, we investigate whether the norm compliance behavior of LLM agents is consistent with that of humans. For theoretical analysis and detailed experimental design, please refer to our paper.

The code for RQ2 is divided into three sub-experiments.

#### 3.1 Sub-experiment 1: Social Cognitive Factors

This experiment probes whether LLMs' normative behavior is influenced by social cognitive factors—**morality (internal)** and **education (external)**—in a human-like manner. We test this by engineering prompts that assign different identities to the agents, effectively asking: "Does an LLM told to be 'highly educated' act differently from one told to be 'uneducated'?" We then measure their **Inappropriate Action Rate (IAR)**.

**1. Run the Experiment**

To run this simulation, execute the following command from the root directory:

```bash
python -m test.experiment.RQ2.SupplementExecutor
```

The `SupplementExecutor` script systematically constructs prompts that assign different moral and educational identities to the LLM agents across 20 scenarios. Results are saved to `test/experiment/RQ2/supplement_result.json`.

**2. Verify the Findings**

By plotting the `IAR` against the five levels for each factor, you can reproduce **Figure 4**. The key observation is the **divergence in trends**:

  * **Moral Level:** You should see a clear and consistent **decrease** in inappropriate actions as morality increases, mirroring human behavior.
  * **Education Level:** In contrast, the trend is erratic, failing to show a consistent decrease. This highlights a key area where LLM behavior **diverges** from established human sociological patterns.

<p align="center">
<img src="./img/RQ2_0.png" width="800" alt="Results for RQ2.1: Social Cognitive Factors">
</p>

#### 3.2 Sub-experiment 2: Risk Preference Curve

A cornerstone of human decision-making is the **S-shaped risk preference curve**, indicating that our appetite for risk changes with the odds. This experiment tests the hypothesis that LLM agents exhibit a similar pattern. We place agents in 20 scenarios where they must choose a course of action, programmatically varying the probability of negative consequences from 5% to 95%, and record their **Legal Action Rate (LAR)**.

**1. Run the Experiment**

To run this experiment, execute the following command from the root directory:

```bash
python -m test.experiment.RQ2.RQ2_2_3
```

The script will iterate through all models and risk levels. The raw choice data will be saved to `test/experiment/RQ2/results_rq2_1.txt`.

**2. Verify the Findings**

The goal is to plot the `Legal Action Rate (LAR)` against the eight risk probability levels to reproduce **Figure 5**. You will be looking for a conspicuous absence:

  * **Risk Preference:** Instead of the S-shaped curve characteristic of human risk aversion and seeking, you should observe a **nearly flat line**. This demonstrates the agents' profound insensitivity to varying levels of risk, a major deviation from human behavior.


<p align="center">
<img src="./img/RQ2_1.png" width="800" alt="Results for RQ2.2: Risk Preference Curve">
</p>

#### 3.3 Sub-experiment 3: Probability Distortion Weights

Moving from behavioral observation to cognitive modeling, this final experiment quantifies the *degree* of bias in an LLM's perception of probability. It is a **post-processing analysis**, not a new simulation. Using the raw decision data generated in Sub-experiment 3.2, we apply the Prelec weighting function to calculate the **probability distortion weight ($\gamma$)** for each model.

**1. Run the Analysis**

This script performs the mathematical fitting to derive the $\gamma$ weights. Execute it from the root directory:

```bash
python -m test.experiment.RQ2.metric1
```

The script will process the choice data and output the calculated $\gamma$ for each model.

**2. Verify the Findings**

Verification for this experiment is a direct **numerical comparison** against the findings in **Table 1**.

  * **Probability Distortion Weight ($\gamma$):** Check the calculated $\gamma$ values. You will find that all tested models produce a $\gamma$ **significantly lower** than the established human median of 0.69.
  * **Interpretation:** This numerical result provides strong evidence that LLMs' internal model of probability is fundamentally different from humans', particularly in how they overweight small probabilities of loss.

<p align="center">

**Table 1: Comparison of Probability Distortion Weights ($\gamma$) in the Loss Domain**
| Model | Calculated Gamma ($\gamma$)|
| :--- | :--- |
| GPT-4o | 0.4454 ± 0.0951 |
| GPT-4o-mini | 0.4909 ± 0.2301 |
| DeepSeek-V2.5 | 0.4412 ± 0.0984 |
| Llama-3-8B-Instruct | 0.4782 ± 0.1341 |
| Qwen2.5-7B-Instruct | 0.6072 ± 0.1681 |
| Human Median | 0.69 |

</p>

### **4. Reproducing Experiments for RQ3**

This section provides instructions to reproduce the experiments for Research Question 3 (RQ3): *How can we enhance LLM agents' compliance with norms?*

The experiments evaluate four distinct methods:

  * **Dynamic Norm Learning Mechanism (DNLM)**: A self-refinement mechanism where the agent dynamically updates its understanding of norms.
  * **Deep MaxPain (DMP)**: A prompt-based method emphasizing the negative consequences of norm violations.
  * **Norm Analysis Chain-of-Thought (NA-CoT)**: A prompt-based method guiding the agent to reason about norms before acting.
  * **Few-shot Norm Learning (FNL)**: A prompt-based method providing concrete examples of norm-compliant and non-compliant behavior.

The experiments are divided into two main scripts.

#### **A. Running Prompt-Based Method Experiments (DMP, NA-CoT, FNL)**

The experiments for the three prompt-based methods (DMP, NA-CoT, and FNL) are handled by a single script. The script automatically iterates through the different prompt engineering strategies across the 100 test scenarios.

To run these experiments, execute the following command:

```bash
python -m test.experiment.RQ3.RQ3
```

This script will test the following prompt variations internally:

  * **"penalty"**: Corresponds to the **DMP** method.
  * **"reason"**: Corresponds to the **NA-CoT** method.
  * **"examples"**: Corresponds to the **FNL** method.

#### **B. Running the DNLM Experiment**

The experiment for the Dynamic Norm Learning Mechanism (DNLM) uses a dedicated script due to its different underlying architecture.

To run the DNLM experiment across the 100 scenarios, execute this command:

```bash
python -m test.experiment.RQ3.RQ3_DNLM
```

#### **Verifying the Results**

  * **Output Location**: The results for all RQ3 experiments will be saved in the `logs/total/` directory.
  * **Evaluation Metric**: The primary metric for evaluation is the **Illegal Action Rate (IAR)**.
  * **Expected Outcome**: You should observe a reduction in the IAR for most methods compared to the baseline. The DNLM method is expected to show one of the most significant reductions.

For reference, the detailed results from our paper are provided below.

##### **Table 2: IAR Changes Across Different Models and Their Variants**

| Model | IAR | Rate Change | Relative Change |
| :--- | :--- | :--- | :--- |
| **GPT-4o** | | | |
| Base | 20.20% | | |
| +DNLM | 3.03% | **-17.17%** | **-85.00%** |
| +DMP | 20.00% | -0.20% | -1.00% |
| +NA-CoT | 15.46% | -4.74% | -23.45% |
| +FNL | 19.39% | -0.81% | -4.03% |
| **GPT-4o-mini** | | | |
| Base | 24.74% | | |
| +DNLM | 6.19% | **-18.56%** | -75.00% |
| +DMP | 15.15% | -9.59% | -38.76% |
| +NA-CoT | 9.00% | -15.74% | -63.62% |
| +FNL | 21.21% | -3.53% | -14.27% |
| **DeepSeek-V2.5** | | | |
| Base | 30.30% | | |
| +DNLM | 13.13% | -17.17% | -56.67% |
| +DMP | 22.00% | -8.30% | -27.39% |
| +NA-CoT | 13.00% | -17.30% | -57.10% |
| +FNL | 31.00% | +0.70%\* | +2.31%\* |
| **Llama-3-8B-Instruct** | | | |
| Base | 37.11% | | |
| +DNLM | 13.27% | **-23.84%** | -64.24% |
| +DMP | 23.23% | -13.88% | -37.40% |
| +NA-CoT | 23.23% | -13.88% | -37.40% |
| +FNL | 32.32% | -4.79% | -12.91% |
| **qwen2.5-7B-Instruct** | | | |
| Base | 14.29% | | |
| +DNLM | 12.12% | -2.17% | -15.19% |
| +DMP | 14.29% | 0.00% | 0.00% |
| +NA-CoT | 6.12% | -8.17% | -57.17% |
| +FNL | 12.37% | -1.92% | -13.44% |

**Note on table formatting:**

  * **Bold** values represent the largest performance improvements for a given model, as highlighted in the original paper.
  * Values marked with an asterisk (`*`) represent an increase in the Illegal Action Rate (shown in red in the original image).

[^1]: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
[^2]: https://docs.conda.io/en/latest/
[^3]: https://learn.microsoft.com/en-us/windows/wsl/about
[^4]: https://platform.openai.com/docs/api-reference/chat/create#chat/create-top_p
