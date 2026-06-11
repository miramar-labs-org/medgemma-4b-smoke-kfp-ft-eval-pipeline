# Eval helper functions — inlined into baseline_eval and post_finetune_eval
# by scripts/build_pipeline.py at the # <<< EVAL_HELPERS_INJECT >>> marker.
# Customize extract_answer and _make_user_content for your dataset.
# Do not add imports here that aren't available in the component container.

import re as _re


def extract_answer(text):
    text = text.strip()
    # "Final Answer: X" prefix
    m = _re.search(r'final answer[:\s]+([A-Ea-e])', text, _re.IGNORECASE)
    if m:
        return m.group(1).upper()
    # standalone letter A–E (MCQ)
    m = _re.match(r'^([A-Ea-e])[.\s]', text)
    if m:
        return m.group(1).upper()
    m = _re.search(r'\b([A-Ea-e])\b', text)
    if m:
        return m.group(1).upper()
    # yes / no / maybe (PubMedQA)
    lower = text.lower()
    for token in ("yes", "no", "maybe"):
        if lower.startswith(token):
            return token
    for token in ("yes", "no", "maybe"):
        if token in lower:
            return token
    return text.split()[0].lower() if text else ""


def make_infer_fn(tokenizer, model, system_message, max_new_tokens, do_sample):
    import torch as _torch

    def _infer(row):
        user_content = _make_user_content(row)
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_content},
        ]
        inputs = tokenizer.apply_chat_template(
            messages, return_tensors="pt", add_generation_prompt=True
        ).to(model.device)
        with _torch.no_grad():
            output_ids = model.generate(
                inputs, max_new_tokens=max_new_tokens, do_sample=do_sample
            )
        return tokenizer.decode(output_ids[0][inputs.shape[1]:], skip_special_tokens=True)

    return _infer


def _make_user_content(row):
    source = row.get("source", "")
    instruction = row.get("instruction", "")
    if source == "pubmedqa":
        return instruction  # already includes "Answer yes, no, or maybe."
    return instruction  # MCQ instructions already contain "Answer with the letter only."
