# Project-supplied dataset formatters.
#
# Each function signature: (example: dict) -> {"instruction": str, "response": str, "source": str}
# Add one function per dataset listed in config.yaml, then register it in FORMATTERS below.
#
# The Build cell inlines this entire file into the prepare_dataset KFP component body.
# Any imports used here must be available inside the component container — add them
# to prepare_dataset's packages_to_install if they are not already there.

OPTION_LABELS = ["A", "B", "C", "D", "E"]


def format_medqa(example):
    options = example.get("options", {})
    if isinstance(options, dict):
        choices = "\n".join(f"{k}. {v}" for k, v in options.items())
    else:
        choices = "\n".join(f"{OPTION_LABELS[i]}. {o}" for i, o in enumerate(options))
    question = example.get("question", "")
    answer_key = example.get("answer_idx") or example.get("answer", "")
    instruction = f"{question}\n\nOptions:\n{choices}\n\nAnswer with the letter only."
    return {
        "instruction": instruction,
        "response": str(answer_key).strip(),
        "source": "medqa",
    }


def format_medmcqa(example):
    options = [
        example.get("opa", ""),
        example.get("opb", ""),
        example.get("opc", ""),
        example.get("opd", ""),
    ]
    choices = "\n".join(f"{OPTION_LABELS[i]}. {o}" for i, o in enumerate(options))
    question = example.get("question", "")
    cop = example.get("cop", 0)
    answer_letter = OPTION_LABELS[int(cop)] if cop is not None else "A"
    instruction = f"{question}\n\nOptions:\n{choices}\n\nAnswer with the letter only."
    return {
        "instruction": instruction,
        "response": answer_letter,
        "source": "medmcqa",
    }


def format_pubmedqa(example):
    question = example.get("question", "")
    context_list = example.get("context", {}).get("contexts", [])
    context = " ".join(context_list) if context_list else ""
    final_decision = example.get("final_decision", "yes")
    if context:
        instruction = f"Context: {context}\n\nQuestion: {question}\n\nAnswer yes, no, or maybe."
    else:
        instruction = f"{question}\n\nAnswer yes, no, or maybe."
    return {
        "instruction": instruction,
        "response": str(final_decision).strip().lower(),
        "source": "pubmedqa",
    }


# Map config.yaml dataset names → formatter functions.
# Each key must match a `name:` entry in config.yaml datasets.
FORMATTERS = {
    "medqa": format_medqa,
    "medmcqa": format_medmcqa,
    "pubmedqa": format_pubmedqa,
}
