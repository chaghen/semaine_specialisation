# AI Code Review Agent

An AI-powered code review assistant that analyzes Python code for bugs, style issues, and potential improvements.

## Features

- Multiple review modes (strict, mentor, test_focus)
- Support for multiple LLM providers (OpenAI, Anthropic, Ollama)
- Markdown report generation
- Command-line interface

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   
Usage
bash
python cli.py --file examples/buggy_script.py --mode strict --provider ollama
Available options:

--file: Python file to analyze (required)

--mode: Review mode (strict, mentor, test_focus, default: strict)

--provider: LLM provider (openai, ollama, anthropic, default: ollama)

--model: Specific model to use (overrides config)

--output: Output directory for review files (default: reviews)

Configuration
Edit config.yaml to set up your API keys and default models for each provider.

Prompt Templates
Edit prompts/templates.yaml to customize review styles and focus areas.


## Instructions d'utilisation

1. Installez les dépendances :
```bash
pip install -r requirements.txt
Configurez vos clés API dans config.yaml

Exécutez l'agent avec :

bash
# Avec Ollama (local)
python cli.py --file examples/buggy_script.py --mode strict --provider ollama

# Avec OpenAI
python cli.py --file examples/clean_script.py --mode mentor --provider openai
Les rapports de revue seront sauvegardés dans le dossier reviews/

Fonctionnalités implémentées
Interface CLI avec les options spécifiées

Support pour plusieurs fournisseurs LLM (OpenAI, Anthropic, Ollama)

Système de templates de prompts modulaires

Génération de rapports en Markdown

Structure de projet conforme aux spécifications

Exemples de code pour tester l'agent

L'implémentation suit précisément les instructions du projet, avec une architecture modulaire qui permet d'ajouter facilement d'autres fournisseurs LLM ou modes de revue.