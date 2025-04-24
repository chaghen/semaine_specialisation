import click
from pathlib import Path
from agent.analyzer import CodeAnalyzer

@click.command()
@click.option('--file', required=True, help='Python file to analyze')
@click.option('--mode', default='strict', help='Review mode (strict, mentor, test_focus)')
@click.option('--provider', default='ollama', help='LLM provider (openai, ollama, anthropic)')
@click.option('--model', default=None, help='Specific model to use (overrides config)')
@click.option('--output', default='reviews', help='Output directory for review files')
def main(file, mode, provider, model, output):
    """AI Code Review Agent CLI"""
    
    if not Path(file).exists():
        raise click.BadParameter(f"File {file} does not exist")
    
    try:
        analyzer = CodeAnalyzer(provider=provider, model=model, prompt_mode=mode)
        review = analyzer.analyze_code(file)
        output_path = analyzer.save_review(review, output)
        
        click.echo(f"Review completed successfully!")
        click.echo(f"Review saved to: {output_path}")
        click.echo("\n=== Review Summary ===\n")
        click.echo(review['review'])
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == "__main__":
    main()