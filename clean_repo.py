import os
import shutil
import sys

# Directories and files to keep in root
KEEP_DIRS = {
    '.git', '.github', '.zencoder', '.zenflow', 'backups', 'certs', 
    'deployment', 'docs', 'hms', 'hospital', 'import', 'insurance excel', 
    'logs', 'media', 'P20_BUSINESS_CONSULTS', 'scripts', 'staticfiles', 'venv'
}

KEEP_FILES = {
    '.dockerignore', '.env', '.gitignore', '.renderignore', 
    'compose.env', 'manage.py', 'README.md', 'requirements.txt', 
    'cleanup_git.py', 'clean_repo.py', 'to_remove.txt'
}

# File extensions to move to scripts/ instead of deleting
MOVE_EXTS = {'.py', '.bat', '.sh', '.ps1'}

def main():
    root_dir = os.getcwd()
    scripts_dir = os.path.join(root_dir, 'scripts')
    
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)
        
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        
        # Skip directories
        if os.path.isdir(item_path):
            continue
            
        # Skip files in KEEP_FILES
        if item in KEEP_FILES:
            continue
            
        # Get extension
        ext = os.path.splitext(item)[1].lower()
        
        if ext in MOVE_EXTS:
            # Move to scripts/
            dest = os.path.join(scripts_dir, item)
            # Handle collision
            if os.path.exists(dest):
                base, extension = os.path.splitext(item)
                counter = 1
                while os.path.exists(os.path.join(scripts_dir, f"{base}_{counter}{extension}")):
                    counter += 1
                dest = os.path.join(scripts_dir, f"{base}_{counter}{extension}")
            
            try:
                shutil.move(item_path, dest)
            except:
                pass
        else:
            # Delete from disk
            try:
                os.remove(item_path)
            except:
                pass

    print("Cleanup complete.")

if __name__ == "__main__":
    main()
