"""Git gutter for showing file changes"""
from typing import Dict, Set, Tuple
import subprocess


class GitGutter:
    """Tracks and displays git changes in the editor"""
    
    @staticmethod
    def get_changed_lines(file_path: str) -> Dict[int, str]:
        """
        Get changed lines from git.
        Returns dict with line_number: change_type ('added', 'modified', 'deleted')
        """
        try:
            # Get git diff for file
            result = subprocess.run(
                ['git', 'diff', '--unified=0', file_path],
                cwd=file_path.rsplit('\\', 1)[0] if '\\' in file_path else '.',
                capture_output=True,
                text=True,
                timeout=2
            )
            
            changes = {}
            current_line = 0
            
            if result.returncode != 0:
                return changes
            
            # Parse diff output
            for line in result.stdout.split('\n'):
                if line.startswith('@@'):
                    # Extract line number from hunk header
                    # Format: @@ -old_line,old_count +new_line,new_count @@
                    parts = line.split('+')[1].split('@@')[0].split(',')
                    current_line = int(parts[0]) - 1
                elif line.startswith('-'):
                    changes[current_line] = 'deleted'
                elif line.startswith('+'):
                    changes[current_line] = 'added'
                    current_line += 1
                else:
                    current_line += 1
            
            return changes
        except Exception:
            return {}
    
    @staticmethod
    def get_git_status(file_path: str) -> str:
        """Get git status of file (modified, untracked, etc)"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain', file_path],
                cwd=file_path.rsplit('\\', 1)[0] if '\\' in file_path else '.',
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if result.returncode == 0 and result.stdout:
                return result.stdout.strip()
            return "untracked"
        except Exception:
            return "unknown"
