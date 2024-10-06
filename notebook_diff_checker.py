import subprocess
import json
import nbformat

notebook1 = input('Enter name of notebook1 ')
notebook2 = input('Enter name of notebook2 ')

def run_nbdiff(notebook1, notebook2):
    """Run nbdiff to compare two notebooks and return the raw diff output."""
    result = subprocess.run(
        ['nbdiff', notebook1, notebook2],
        stdout=subprocess.PIPE,
        text=True
    )
    return result.stdout  # Return plain text output

def count_changed_lines(diff_output):
    """Count the number of added, removed, changed lines, including metadata and headers."""
    changed_lines = 0
    lines = diff_output.splitlines()

    for line in lines:
        # Count added lines (including headers and metadata)
        if line.startswith('+'):
            changed_lines += 1  # Count all added lines, including headers
        # Count removed lines (including headers and metadata)
        elif line.startswith('-'):
            changed_lines += 1  # Count all removed lines, including headers
        # Count modifications in cells and metadata
        elif line.startswith('@@') or 'replaced' in line or 'modified' in line:
            changed_lines += 1  # Count modifications
    
    return changed_lines


def count_total_lines(notebook_path):
    """Count the total number of lines in a notebook by loading it with nbformat."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
        total_lines = 0
        for cell in notebook.cells:
            if cell.cell_type == 'code' or cell.cell_type == 'markdown':
                total_lines += len(cell.source.split('\n'))
        return total_lines

def calculate_percentage_of_changes(changed_lines, total_lines):
    """Calculate the percentage of changes."""
    if total_lines == 0:
        return 0
    return (changed_lines / total_lines) * 100

diff_output = run_nbdiff(notebook1, notebook2)
print(f"Diff output:\n{diff_output}\n")  # To visualize the diff
changed_lines = count_changed_lines(diff_output)
total_lines = count_total_lines(notebook1)
percentage_of_changes = calculate_percentage_of_changes(changed_lines, total_lines)

print(f'Total lines in original notebook: {total_lines}')
print(f'Number of changed lines: {changed_lines}')
print(f'Percentage of changes: {percentage_of_changes:.2f}%')

