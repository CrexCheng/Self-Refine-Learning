#-*- coding: utf-8 -*-
#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENTRANCE_MODULE="test.experiment.RQ1.RQ1"
SCENARIO_DIR="files/filtered_scenarios"
IS_INIT_NORM_BASE=True
IS_UPDATE_NORM=False


# Loop over both True and False for IS_UPDATE_NORM
for IS_INIT_NORM_BASE in False True
do
    LOG_FILE="logs/total/$(date +'%Y-%m-%d').log"
    # Run the Python script with the current value of IS_UPDATE_NORM
    if python3 -m "$ENTRANCE_MODULE" --is_update_norm="$IS_UPDATE_NORM" --scenarios_dir="$SCENARIO_DIR" --is_init_norm_base="$IS_INIT_NORM_BASE"; then
        echo "Python script executed successfully with IS_UPDATE_NORM=$IS_UPDATE_NORM."
    else
        echo "Error: Python script execution failed with IS_UPDATE_NORM=$IS_UPDATE_NORM."
        exit 1
    fi

    # Count the number of "Error" occurrences in the log file
    ERROR_COUNT=$(grep -o "Error running scenario" "$LOG_FILE" | wc -l)
    # Count the number of "'is_legal': False" occurrences in the log file
    LEGAL_FALSE_COUNT=$(grep -o "'is_legal': False" "$LOG_FILE" | wc -l)
    # Count the number of "'is_legal': True" occurrences in the log file
    LEGAL_TRUE_COUNT=$(grep -o "'is_legal': True" "$LOG_FILE" | wc -l)
    # Append the counts to result.txt
    echo "Error count (IS_UPDATE_NORM=$IS_UPDATE_NORM): $ERROR_COUNT" >> "$SCRIPT_DIR/RQ1result.txt"
    echo "'is_legal': False count (IS_UPDATE_NORM=$IS_UPDATE_NORM): $LEGAL_FALSE_COUNT" >> "$SCRIPT_DIR/RQ1result.txt"
    echo "'is_legal': True count (IS_UPDATE_NORM=$IS_UPDATE_NORM): $LEGAL_TRUE_COUNT" >> "$SCRIPT_DIR/RQ1result.txt"
    # Rename the log file based on IS_UPDATE_NORM (consistent with variable name)
    NEW_LOG_FILE="logs/total/$(date +'%Y-%m-%d')_NormUpdate${IS_UPDATE_NORM}_InitNormBase${IS_INIT_NORM_BASE}.log"
    mv "$LOG_FILE" "$NEW_LOG_FILE"
done
