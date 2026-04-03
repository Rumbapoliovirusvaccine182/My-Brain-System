"""
Simple template engine for project setup.
Replaces {{variable}} placeholders with provided values.
"""
import re
from pathlib import Path
from datetime import datetime, timedelta


def populate_template(template_path: Path, variables: dict) -> str:
    """Read a template file and replace {{variable}} placeholders."""
    content = template_path.read_text(encoding='utf-8')

    # Add computed defaults
    defaults = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'review_by': (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d'),
    }

    merged = {**defaults, **variables}

    for key, value in merged.items():
        content = content.replace(f'{{{{{key}}}}}', str(value))

    return content


def create_from_template(template_path: Path, output_path: Path, variables: dict) -> Path:
    """Create a new file from a template with variables replaced."""
    content = populate_template(template_path, variables)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding='utf-8')
    return output_path


def list_templates(templates_dir: Path) -> list:
    """List all available templates."""
    return sorted(templates_dir.glob('*.md'))
