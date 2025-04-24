from pathlib import Path
import yaml
from .llm_interface import LLMClient

class CodeAnalyzer:
    def __init__(self, provider="ollama", model=None, prompt_mode="strict"):
        self.llm_client = LLMClient(provider, model)
        self.prompt_mode = prompt_mode
        self._load_prompt_templates()
        
    def _load_prompt_templates(self):
        prompts_path = Path(__file__).parent.parent / "prompts" / "templates.yaml"
        with open(prompts_path) as f:
            self.prompt_templates = yaml.safe_load(f)
        
        if self.prompt_mode not in self.prompt_templates:
            raise ValueError(f"Prompt mode '{self.prompt_mode}' not found in templates")
    
    def _read_code(self, file_path):
        with open(file_path, 'r') as f:
            return f.read()
    
    def analyze_code(self, code_or_path):
        # If it's a file path, read the code
        if isinstance(code_or_path, str) and Path(code_or_path).exists():
            code = self._read_code(code_or_path)
        else:
            code = code_or_path
        
        prompt_template = self.prompt_templates[self.prompt_mode]["prompt"]
        review = self.llm_client.run(prompt_template, code)
        
        return {
            "code": code,
            "review": review,
            "mode": self.prompt_mode
        }
    
    def save_review(self, review_data, output_dir="reviews"):
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        filename = f"review_{review_data['mode']}_{len(list(output_path.glob('*.md')) + 1}.md"
        filepath = output_path / filename
        
        with open(filepath, 'w') as f:
            f.write(f"# Code Review Report\n\n")
            f.write(f"**Mode**: {review_data['mode']}\n\n")
            f.write(f"## Code\n```python\n{review_data['code']}\n```\n\n")
            f.write(f"## Review\n{review_data['review']}\n")
        
        return filepath