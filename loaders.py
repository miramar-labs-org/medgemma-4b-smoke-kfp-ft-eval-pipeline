# Dataset loaders — one lambda per dataset, registered in LOADERS dict.
# Each value: () -> HuggingFace Dataset (train split, mapped through formatter)
# Key must match a `name:` entry in config.yaml datasets.
from datasets import load_dataset

LOADERS = {
    "medqa": lambda: load_dataset(
        "bigbio/med_qa", "med_qa_en_source", trust_remote_code=True, split="train"
    ).map(format_medqa),
    "medmcqa": lambda: load_dataset("medmcqa", split="train").map(format_medmcqa),
    "pubmedqa": lambda: load_dataset(
        "qiaojin/PubMedQA", "pqa_labeled", split="train"
    ).map(format_pubmedqa),
}
