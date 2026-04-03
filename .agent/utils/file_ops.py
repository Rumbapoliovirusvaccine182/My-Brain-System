"""
File operation utilities for My Brain knowledge management system
"""
import json
import shutil
from pathlib import Path
from typing import Any, Dict


def read_markdown(path: Path) -> str:
    """
    Read a markdown file with UTF-8 encoding
    
    Args:
        path: Path to markdown file
        
    Returns:
        File contents as string
        
    Raises:
        FileNotFoundError: If file doesn't exist
        UnicodeDecodeError: If file encoding is invalid
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write_markdown(path: Path, content: str) -> None:
    """
    Write content to a markdown file with UTF-8 encoding
    
    Args:
        path: Path to markdown file
        content: Content to write
    """
    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def read_json(path: Path) -> Dict[str, Any]:
    """
    Read a JSON file with UTF-8 encoding
    
    Args:
        path: Path to JSON file
        
    Returns:
        Parsed JSON data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If JSON is invalid
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(path: Path, data: Dict[str, Any], indent: int = 2) -> None:
    """
    Write data to a JSON file with UTF-8 encoding
    
    Args:
        path: Path to JSON file
        data: Data to write
        indent: JSON indentation level (default: 2)
    """
    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)


def safe_move(source: Path, dest: Path, overwrite: bool = False) -> bool:
    """
    Safely move a file from source to destination
    
    Args:
        source: Source file path
        dest: Destination file path
        overwrite: Whether to overwrite existing destination file
        
    Returns:
        True if successful, False otherwise
        
    Raises:
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite=False
    """
    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")
    
    if dest.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {dest}")
    
    # Ensure destination directory exists
    dest.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        shutil.move(str(source), str(dest))
        return True
    except Exception as e:
        print(f"Error moving file: {e}")
        return False


def ensure_dir(path: Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary
    
    Args:
        path: Directory path
        
    Returns:
        The directory path
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_file_size(path: Path) -> int:
    """
    Get file size in bytes
    
    Args:
        path: File path
        
    Returns:
        File size in bytes
    """
    return path.stat().st_size if path.exists() else 0


def list_markdown_files(directory: Path, recursive: bool = False, exclude: list = None) -> list[Path]:
    """
    List all markdown files in a directory
    
    Args:
        directory: Directory to search
        recursive: Whether to search recursively
        exclude: List of filenames to exclude
        
    Returns:
        List of markdown file paths
    """
    if exclude is None:
        exclude = []
    
    pattern = "**/*.md" if recursive else "*.md"
    files = directory.glob(pattern)
    
    # Filter out excluded files and topic indices
    result = []
    for f in files:
        if f.name in exclude:
            continue
        # Exclude topic index files (pattern: [FolderName]_主題索引.md)
        if f.name.endswith('_主題索引.md'):
            continue
        result.append(f)
    
    return result
