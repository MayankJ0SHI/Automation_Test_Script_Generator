import os
ALLOWED_EXTENSIONS = {'.java', '.xml', '.properties', '.yaml', '.yml'}
def read_codebase_files(root_path):
    file_contents = []
    for root, _, files in os.walk(root_path):
        for file in files:
            if any(file.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_contents.append({
                            'path': full_path,
                            'content': f.read()
                        })
                except Exception as e:
                    print(f"Failed to read {full_path}: {e}")
    return file_contents
