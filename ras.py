#!/usr/bin/env python3
#
# A waybar plugin showing the number of errors detected in your RAM.
# This only works if you have ECC RAM running in error detecting and correcting mode

import json
import re
import subprocess
import sys

# The symbol to include in the widget in case anything went wrong
ERROR = "☢️"

# Example output:
#
# $ ras-mc-ctl --error-count
# Label                   CE  UE
# mc#0csrow#2channel#1    0   0
# mc#0csrow#2channel#0    0   0
# mc#0csrow#3channel#0    0   0
# mc#0csrow#3channel#1    0   0

RAS_CMD = ["ras-mc-ctl", "--error-count"]

# Regex capturing the CE and UE counts in the output of RAS_CMD
ERROR_COUNT_REGEX = r"^\S+\s+(\d+)\s+(\d+)$"


def run_ras():
    result = subprocess.run(RAS_CMD, capture_output=True, timeout=2)
    if result.returncode != 0:
        return (
            ERROR,
            f"ras-mc-ctl exited with return code {result.returncode}\n{result.stderr.decode()}",
        )

    # Show the entire output as tooltip
    tooltip = result.stdout.decode()
    # Number of corrected and uncorrectable errors detected
    ce_count = 0
    ue_count = 0
    for match in re.finditer(ERROR_COUNT_REGEX, tooltip, flags=re.MULTILINE):
        (ce, ue) = match.groups()
        ce_count += int(ce)
        ue_count += int(ue)

    ce_label = "CE" if ce_count == 0 else f"{ERROR}CE"
    ue_label = "UE" if ue_count == 0 else f"{ERROR}UE"
    text = f"{ce_label}: {ce_count}, {ue_label}: {ue_count}"

    return (text, tooltip)


try:
    (text, tooltip) = run_ras()
except Exception as err:
    text = ERROR
    tooltip = str(err)

sys.stdout.write(json.dumps({"text": text, "tooltip": tooltip}))
