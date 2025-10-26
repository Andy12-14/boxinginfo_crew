# AiBoxing Crew

AiBoxing is a small multi-agent demo built on top of crewAI. It demonstrates how multiple specialized agents (a Boxing Analyst and a News Reporter by default) can collaborate to gather information about boxers, create short reports, and deliver results (for example via WhatsApp) using custom tools.

This repository is intended as a starting point: customize agents in `src/ai_boxing/config/agents.yaml`, tasks in `src/ai_boxing/config/tasks.yaml`, add or extend tools in `src/ai_boxing/tools/`, and adapt `src/ai_boxing/crew.py` to wire agents together.

## Quick demo flow

- User runs `crewai run`
- The `Boxing Analyst` agent looks up the requested boxer
- The `News Reporter` agent gathers recent news and prepares a short report
- (Optional) The `WhatsApp Message Tool` can send the report to a provided phone number

## Prerequisites

- Python 3.10 - 3.13
- Ollama (if you plan to run models locally)
- A working Ollama model such as `gemma3` or `mixtral` (see notes below)

This project uses the `uv` package manager for dependency handling. Learn more about UV here:

- UV docs: https://docs.astral.sh/uv/

Install UV (recommended) with pip:

```bash
pip install uv
```

Install the project dependencies (after installing `uv`) from the repository root:

```bash
uv install
```

Note: older templates sometimes used `crewai install`; `uv install` is the modern, recommended flow for projects using UV.

## Running locally

1. Ensure Ollama is running and the desired model is pulled. Example quick checks:

```bash
ollama list
ollama pull gemma3    # small and fast for local testing
```

2. Run the crew from the repository root:

```bash
crewai run
```

If you experience long model startup times or timeouts when using a large model (e.g., `mixtral`), try testing with a smaller model (`gemma3`) while debugging. Once everything works, switch back to your preferred model and increase timeouts if needed.

## Customization

- `src/ai_boxing/config/agents.yaml` — define agent names, roles, prompts and LLM settings
- `src/ai_boxing/config/tasks.yaml` — define the tasks that will be executed by the crew
- `src/ai_boxing/crew.py` — wires agents, LLM instances and tools together
- `src/ai_boxing/tools/custom_tool.py` — example tools (WhatsApp, Web Search). Replace placeholder logic with real integrations if needed.

## GitHub: push this project to a remote repository

Below are two common workflows to push this code to a new GitHub remote. Choose the one you prefer.

1) Using the GitHub website

- Create a new repository on GitHub (https://github.com/new). Do not initialize with a README (you already have one).
- Back in your project root:

```bash
git init
git add .
git commit -m "Initial commit: AiBoxing crew"
# replace <YOUR_REMOTE_URL> with the HTTPS or SSH URL provided by GitHub
git remote add origin <YOUR_REMOTE_URL>
git branch -M main
git push -u origin main
```

2) Using the `gh` CLI (recommended if you have it installed)

```bash
# create a repo on GitHub using the gh CLI (interactive or from flags)
gh repo create my-ai-boxing --public --source=. --remote=origin --push
```

After pushing, your repository will be available on GitHub. Add a proper `.gitignore` if you haven't already to avoid committing virtual environments, secrets, and large files. A minimal `.gitignore` for this project should include:

```
.venv/
venv/
__pycache__/
*.pyc
.env
report.md
/.ollama/
```

## Recommended next steps

- Add a `.env` file with any required credentials (do not commit it).
- Replace placeholder tool logic (in `src/ai_boxing/tools/custom_tool.py`) with real requests/clients if you need live web scraping or message delivery.
- Add tests in the `tests/` folder and CI (GitHub Actions) for automated checks.

## Support & Resources

- crewAI docs: https://docs.crewai.com
- UV docs: https://docs.astral.sh/uv/
- Ollama: https://ollama.ai

If you want, I can add a `CONTRIBUTING.md`, a sample `.github/workflows/ci.yml`, or the `.gitignore` file for you automatically.

---

Happy hacking — adapt agents, tasks and tools to your use case and iterate fast.
