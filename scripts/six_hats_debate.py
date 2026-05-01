#!/usr/bin/env python3
"""
Six Hats Debate Orchestrator

Usage:
    python3 scripts/six_hats_debate.py "Your topic here" "/path/to/output/"
    python3 scripts/six_hats_debate.py "Should we launch v2?" "Projects/decisions/"

This script is a reference implementation. The actual debate runs via the SKILL.md
workflow in conversation. This file documents the expected behavior and can be used
for batch processing or testing.
"""

import sys
from datetime import datetime
from pathlib import Path

ROUNDS = 3
# Sequential hats per round; Blue moderates after all rounds (see SKILL.md).
DEBATE_HAT_ORDER = ["white", "red", "yellow", "black", "green"]
HAT_LABELS = {
    "white": "White Hat (Facts & Information)",
    "red": "Red Hat (Emotion & Intuition)",
    "yellow": "Yellow Hat (Optimism & Benefits)",
    "black": "Black Hat (Caution & Risks)",
    "green": "Green Hat (Creativity & Alternatives)",
    "blue": "Blue Hat (Process & Moderation)",
}

STUB_BODY = """# Six Hats Debate: {topic}

**Generated**: {when}

This stub was written by `scripts/six_hats_debate.py`. Replace it with full output by running the conversational workflow described in **SKILL.md** in your agent session (three rounds for the hats below, then Blue Hat synthesis).

**Rounds**: {rounds}, **Hat order each round**: {hat_chain}

Blue Hat (**{blue_label}**) synthesizes after the rounds; it does not take a turn with the other hats during each round.

---
*(Body intentionally empty — populate using the skill.)*
"""


def generate_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def main(topic: str, output_path: str):
    if not topic.strip():
        print("Error: topic cannot be empty")
        sys.exit(1)

    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    when = now.strftime("%Y-%m-%d %H:%M:%S")
    output_file = output_dir / f"debate-{timestamp}.md"

    hat_chain = " → ".join(HAT_LABELS[h] for h in DEBATE_HAT_ORDER)
    body = STUB_BODY.format(
        topic=topic,
        when=when,
        rounds=ROUNDS,
        hat_chain=hat_chain,
        blue_label=HAT_LABELS["blue"],
    )
    output_file.write_text(body, encoding="utf-8")

    print(f"Topic: {topic}")
    print(f"Output: {output_file}")
    print(f"Rounds: {ROUNDS}")
    print(f"Hats per round: {hat_chain}")
    print(f"Moderation: {HAT_LABELS['blue']} after rounds")
    print("---")
    print("Stub written. Replace with full debate via SKILL.md in conversation.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/six_hats_debate.py <topic> <output_path>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
