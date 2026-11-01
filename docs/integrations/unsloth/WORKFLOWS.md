---
title: "Unsloth Workflows & Fleet Integration"
category: integration
status: active
audience: mcp-dev
skill_candidate: true
related:
  - integrations/unsloth/README.md
  - integrations/unsloth/TECHNICAL.md
  - standards/LOCAL_LLM_STANDARDS.md
last_updated: 2026-08-05
---

# Unsloth — Workflows & Fleet Integration

SOP-style playbooks for using Unsloth on Goliath (RTX 4090 24 GB, native Windows). Reference: [README.md](README.md) (assessment) and [TECHNICAL.md](TECHNICAL.md) (install/API detail).

---

## W1. Local SFT / QLoRA Fine-Tune (Core, script-based)

**When:** reproducible, versionable training runs; dataset already exists.

1. **Env** (one-time):
   ```powershell
   uv venv unsloth_env --python 3.13
   .\unsloth_env\Scripts\activate
   uv pip install unsloth --torch-backend=auto
   ```
2. **Verify GPU plumbing**:
   ```python
   import torch
   assert torch.cuda.is_available()
   ```
3. **Script skeleton** (adapted from the official Windows-verified flow; model/dataset examples are 4090-appropriate):
   ```python
   from unsloth import FastLanguageModel, FastModel
   from trl import SFTTrainer, SFTConfig
   from datasets import load_dataset

   max_seq_length = 2048   # 512 for smoke test
   model, tokenizer = FastLanguageModel.from_pretrained(
       model_name="unsloth/gemma-4-e2b-it",   # or Qwen3.5 4B / Llama 3.1 8B
       max_seq_length=max_seq_length,
       load_in_4bit=True,       # QLoRA (fits 14B on 24 GB); False = 16-bit LoRA (≤9B)
       full_finetuning=False,
   )
   model = FastLanguageModel.get_peft_model(
       model,
       r=16,
       target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],
       lora_alpha=16,
       lora_dropout=0,
       bias="none",
       use_gradient_checkpointing="unsloth",
       max_seq_length=max_seq_length,
       random_state=3407,
   )
   trainer = SFTTrainer(
       model=model,
       train_dataset=load_dataset("json", data_files={"train": "train.jsonl"}, split="train"),
       tokenizer=tokenizer,
       args=SFTConfig(
           max_seq_length=max_seq_length,
           per_device_train_batch_size=2,   # 1-3 on 24 GB; drop on OOM
           gradient_accumulation_steps=4,
           max_steps=60,                    # smoke: 60; real: epochs-based
           logging_steps=1,
           output_dir="outputs",
           optim="adamw_8bit",
           seed=3407,
       ),
   )
   trainer.train()
   ```
4. **Validate**: watch the Unsloth banner ("Unsloth 2026.x: Fast patching", GPU detected, Triton version); loss decreasing; no OOM.
5. **Save**:
   ```python
   model.save_pretrained_merged("model-merged", tokenizer, save_method="merged_16bit")   # 16-bit merge
   model.save_pretrained_gguf("model-gguf", tokenizer, quantization_method="q4_k_m")     # GGUF
   ```

**Verify:** `loss` drops over steps; artifacts appear in `outputs/`, `model-merged/`, `model-gguf/`; run inference on a held-out prompt.

---

## W2. Unsloth Studio GUI Flow (validation path)

**When:** quick evaluation, non-engineers, dataset building from documents.

1. Install: `irm https://unsloth.ai/install.ps1 | iex` (use `UNSLOTH_SKIP_AUTOSTART=1` for non-interactive).
2. Launch: `unsloth studio -p 8888` → browse `http://127.0.0.1:8888`.
3. Search/download a model (e.g. Gemma 4 E2B, Qwen3.5 4B — first search shows free-tier GGUFs).
4. Build a dataset via **Data Recipe** (PDF/CSV/DOCX → dataset) or upload JSONL.
5. Train: pick LoRA/QLoRA, batch 1–2, watch live loss/GPU curves.
6. Chat to verify; export GGUF; deploy via §W4.

**Verify:** training completes without OOM; chat reflects the fine-tune behavior.

---

## W3. Reinforcement Learning (GRPO)

**When:** reasoning/format-following tuning (e.g. DeepSeek-V4-Flash RL).

- Unsloth GRPO uses ~80% less VRAM than vanilla; FP8 RL and vision RL are supported on consumer GPUs.
- 4090 scope: ≤14B models for GRPO runs; use the official GRPO notebooks (Qwen3.5 4B GRPO, gpt-oss 20B GRPO) as templates.
- Studio exposes RL recipes in the training UI; Core uses `GRPOTrainer`.

**Verify:** reward metric improves; generation format complies with the reward function.

---

## W4. GGUF Export & Deployment

**When:** shipping a fine-tuned model to Ollama / llama.cpp / fleet webapps.

1. Train (§W1 or W2) → save GGUF: `model.save_pretrained_gguf(..., quantization_method="q4_k_m")` or Studio Export.
2. Serve options:
   - **Ollama**: `ollama create <name> -f Modelfile` from the GGUF → automatically available to local-llm-mcp and every fleet webapp's Ollama probe (port 11434).
   - **Unsloth Studio API**: OpenAI-compatible `/v1/chat/completions` — usable directly as a provider.
3. (Optional) Test as agent backend: `unsloth start opencode`.

**Verify:** `ollama list` shows the model; a fleet webapp chat page can select and use it.

---

## W5. Agent Bridging (`unsloth start`)

| Goal | Command |
|------|---------|
| Local model as the agent's engine | `unsloth start opencode` (also claude/codex/hermes/openclaw) |
| Keep main model, local subagent | `unsloth start claude --as-subagent --model unsloth/model-GGUF:quant` |
| Serve to fleet webapp | point webapp LLM provider config at Studio's `/v1/chat/completions` |

**Verify:** agent session uses the local model (check provider/model in the agent status).

---

## W6. MCP Control Endpoint (fleet hook)

Unsloth's opt-in MCP control endpoint lets AI clients manage models, training, recipes, checkpoints, and exports over MCP.

**Fleet integration options (decision needed):**
1. **Extend local-llm-mcp** with an `unsloth_*` tool group (train/export/status) — keeps one control plane for local inference + local training.
2. **New MCP repo** (`unsloth-mcp` or fold into a "local-ml-mcp") wrapping the control endpoint + training job queue; needs a port allocation from the 10700–11500 reservoir.
3. **Ad-hoc**: use the endpoint manually from any MCP-capable client during experiments; no repo.

Recommendation: start with (3), graduate to (1) if training becomes a repeatable fleet capability. If a repo is built, follow the **New Repo Gate** in `mcp-central-docs/standards/` (portmanteau `unsloth_ops` with train/export/status/list ops, Prefab surface for job status, README + llms.txt + glama.json).

**Security note:** server-side tools run as the logged-in user; never expose the control endpoint beyond localhost.

---

## W7. Fleet Fit & Guardrails

- **Complement, not replacement**: Ollama remains the serving engine; Unsloth adds the training/RL track. Cloud Foundry finetuning (SFT/DPO/RFT skill) stays for large runs and multi-GPU work.
- **GPU contention rule**: pause Ollama serving (or accept degraded quality) during training runs; 4090 is shared.
- **Model scope on 24 GB**: QLoRA ≤27B (sweet spot 7B–14B); 16-bit LoRA ≤9B; no 32B+ training.
- **Don't point Studio at fleet venvs** — it creates its own 3.11–3.13 env; fleet projects use their own uv venvs.
- **AGPL**: Studio UI is AGPL-3.0 — fine locally; do not vendor Studio into a redistributed fleet product without license review.
- **Disk hygiene**: torch + runs consume tens of GB; clean `outputs/` and old GGUF quants after validation.

---

## Validation Checklist (new machine or reinstall)

- [ ] `uv pip install unsloth --torch-backend=auto` succeeds; `import unsloth` banner shows GPU + torch CUDA version
- [ ] `torch.cuda.is_available()` is `True` with driver 620.02 / cu130
- [ ] Smoke run (max_steps=60, 3B–4B QLoRA, batch 2) completes without OOM, loss drops
- [ ] GGUF export produces a file ≥100 MB that Ollama imports and serves
- [ ] Studio launches on 8888, model search works, first llama.cpp compile finished
- [ ] Training run leaves no zombie python processes holding the GPU (check `nvidia-smi`)

---
*Last updated: 2026-08-05*
