"""
Analyze all notes in 10_Garden and generate dashboard analysis
Refactored to use shared utilities
"""
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict

# Configure UTF-8 output for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Import shared utilities
from utils import parse_note, write_json
import config

def analyze_garden():
    """Analyze all notes in Garden and generate statistics"""
    
    # Collect all markdown files
    notes = []
    
    for md_file in config.GARDEN_DIR.rglob("*.md"):
        # Skip excluded files
        if md_file.name in config.EXCLUDE_FILES:
            continue
        
        try:
            note_metadata = parse_note(md_file)
            notes.append({
                'filename': note_metadata.filename,
                'title': note_metadata.title,
                'tags': note_metadata.tags,
                'word_count': note_metadata.word_count,
                'wikilinks': note_metadata.wikilinks,
                'modified': note_metadata.modified_time,
                'source_type': note_metadata.source_type,
                'source_asset': note_metadata.source_asset,
            })
        except Exception as e:
            print(f"Error processing {md_file.name}: {e}")
    
    # Sort by modification time
    notes.sort(key=lambda x: x['modified'], reverse=True)
    
    # Analyze tags
    all_tags = []
    for note in notes:
        all_tags.extend(note['tags'])
    tag_counts = Counter(all_tags)
    
    # Identify hot topics (most common tags)
    hot_tags = tag_counts.most_common(10)
    
    # Group notes by tags
    notes_by_tag = defaultdict(list)
    for note in notes:
        for tag in note['tags']:
            notes_by_tag[tag].append(note['title'])
    
    # Identify orphans and stubs
    orphans = [n for n in notes if len(n['wikilinks']) < 2 and n['word_count'] < 2000]
    
    # Generate console report
    print(f"Total notes: {len(notes)}")
    print(f"\nTop 10 tags:")
    for tag, count in hot_tags:
        print(f"  {tag}: {count}")
    
    print(f"\nRecent notes (top 10):")
    for note in notes[:10]:
        mod_time = datetime.fromtimestamp(note['modified']).strftime('%Y-%m-%d %H:%M')
        print(f"  {note['title']} ({mod_time})")
    
    print(f"\nOrphans/Stubs ({len(orphans)}):")
    for note in orphans[:10]:
        print(f"  {note['title']} ({note['word_count']} chars, {len(note['wikilinks'])} links)")
    
    # Save detailed analysis
    analysis_data = {
        'total_notes': len(notes),
        'notes': notes,
        'tag_counts': dict(tag_counts),
        'notes_by_tag': dict(notes_by_tag),
        'orphans': [{'title': n['title'], 'filename': n['filename'], 'word_count': n['word_count']} 
                   for n in orphans]
    }
    
    output_path = config.AGENT_DIR / "dashboard_analysis.json"
    write_json(output_path, analysis_data)
    
    print(f"\n✓ Analysis saved to {output_path.relative_to(config.BRAIN_ROOT)}")

if __name__ == "__main__":
    analyze_garden()
