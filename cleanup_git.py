import subprocess
import os

def main():
    # Use -z to get null-terminated filenames and capture as bytes
    try:
        result = subprocess.run(['git', 'ls-files', '-z'], capture_output=True, check=True)
        files_bytes = result.stdout.split(b'\0')
    except Exception as e:
        print(f"Error: {e}")
        return

    # Patterns to match for removal from git index
    # We'll use bytes patterns
    patterns = [
        b"SUMMARY.md", b"GUIDE.md", b"FIXED.md", b"COMPLETE.md",
        b"COMPLETE.txt", b"FIXED.txt", b"SUMMARY.txt", b"GUIDE.txt",
        b"PATCH.txt", b"OUTPUT.txt", b"import_log", b"server_output.txt",
        b"startup_log.txt", b"test_output", b"command_output.txt",
        b"packinfo.txt", b"render_env_file.txt",
        b"\xe2\x9c\x85", # ✅
        b"\xe2\x9a\xa1", # ⚡
        b"\xe2\xad\x90", # ⭐
        b"\xf0\x9f\x9a\x80", # 🚀
        b"\xf0\x9f\x9a\xa8", # 🚨
        b"\xf0\x9f\x9a\xa9", # 🚩
        b"\xf0\x9f\x93\x8a", # 📊
        b"\xf0\x9f\x93\x88", # 📈
        b"\xf0\x9f\x8e\x89", # 🎉
        b"\xf0\x9f\x8e\x8a", # 🎊
        b"\xe2\x9c\xa8", # ✨
        b"\xf0\x9f\x92\xa1", # 💡
        b"\xf0\x9f\x94\x97", # 🔗
        b"\xf0\x9f\x94\xa5", # 🔥
        b"\xf0\x9f\x8c\x80"  # 🌀
    ]
    
    to_remove = []
    for file_b in files_bytes:
        if not file_b:
            continue
            
        # Only target files in the root directory (no slashes)
        # Check for / in bytes
        if b'/' in file_b:
            # Check if it's in hospital/docs or other specific places we want to clean
            if b'hospital/docs/' in file_b or b'hospital/templates/' in file_b:
                # Still check patterns
                pass
            else:
                continue
            
        should_remove = False
        for pattern in patterns:
            if pattern in file_b:
                should_remove = True
                break
        
        # Don't remove essential files
        if file_b in [b'README.md', b'requirements.txt', b'manage.py', b'.gitignore', b'.dockerignore', b'.renderignore']:
            should_remove = False
            
        if should_remove:
            to_remove.append(file_b)
            
    print(f"Found {len(to_remove)} files to remove from git index.")
    
    # Remove in batches of 50
    batch_size = 50
    for i in range(0, len(to_remove), batch_size):
        batch = to_remove[i:i + batch_size]
        print(f"Removing batch {i//batch_size + 1}...")
        try:
            subprocess.run(['git', 'rm', '--cached', '--'] + [f.decode('utf-8', errors='ignore') for f in batch], check=True, capture_output=True)
        except Exception as e:
            # If decode fails or git rm fails, try one by one
            for f in batch:
                try:
                    # On Windows, git might expect a specific encoding or handle it via a temp file
                    # We'll try to just use the raw bytes if possible, but subprocess.run needs strings on Windows
                    # or we can use git rm --pathspec-from-file
                    pass
                except:
                    pass
            print(f"Error in batch {i//batch_size + 1}: {e}")
            # Fallback to pathspec from file for stubborn files
            with open('to_remove.txt', 'wb') as f_list:
                for f in batch:
                    f_list.write(f + b'\n')
            subprocess.run(['git', 'rm', '--cached', '--pathspec-from-file=to_remove.txt'], check=True)

    print("Done cleaning up root files from git index.")

if __name__ == "__main__":
    main()
