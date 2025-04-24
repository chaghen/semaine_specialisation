import openai
import anthropic
import requests
import yaml
from pathlib import Path

class LLMClient:
    def __init__(self, provider, model=None):
        self.provider = provider
        self.model = model
        self._load_config()
        
    def _load_config(self):
        config_path = Path(__file__).parent.parent / "config.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        provider_config = config["providers"].get(self.provider, {})
        if not provider_config:
            raise ValueError(f"Provider {self.provider} not configured in config.yaml")
            
        self.model = self.model or provider_config.get("model")
        
        if self.provider == "openai":
            openai.api_key = provider_config.get("api_key", "")
            if not openai.api_key:
                raise ValueError("OpenAI API key not configured")
        elif self.provider == "anthropic":
            self.client = anthropic.Anthropic(api_key=provider_config.get("api_key", ""))
            if not provider_config.get("api_key"):
                raise ValueError("Anthropic API key not configured")
    
    def run(self, prompt, code_snippet):
        if self.provider == "openai":
            return self._call_openai(prompt, code_snippet)
        elif self.provider == "ollama":
            return self._call_ollama(prompt, code_snippet)
        elif self.provider == "anthropic":
            return self._call_anthropic(prompt, code_snippet)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _call_openai(self, prompt, code_snippet):
        response = openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful code review assistant."},
                {"role": "user", "content": prompt.format(code=code_snippet)}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    
    def _call_ollama(self, prompt, code_snippet):
        url = "http://localhost:11434/api/chat"
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt.format(code=code_snippet)}
            ],
            "stream": False
        }
        
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()["message"]["content"]
    
    def _call_anthropic(self, prompt, code_snippet):
        message = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            temperature=0.3,
            system="You are a helpful code review assistant.",
            messages=[
                {"role": "user", "content": prompt.format(code=code_snippet)}
            ]
        )
        return message.content[0].text