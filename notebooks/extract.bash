echo "Processing robust scaling configurations..."

python -c "
import json, os, re, ast

notebook_path = '${{ env.CHANGED_FILE }}'
with open(notebook_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# --- 1. Establish Default Metadata Configurations ---
configs = {
    'enable_gpu': False,
    'enable_tpu': False,
    'keywords': ['healthcare', 'classification'],
    'dataset_sources': [],
    'kernel_sources': []
}

# --- 2. Dynamically Parse Notebook Metadata Overrides ---
          for cell in data.get('cells', []):
              if cell.get('cell_type') == 'code':
                  for line in cell.get('source', []):
                      # Matches: # KAGGLE_CONFIG: key = value
                      match = re.search(r'#\s*KAGGLE_CONFIG:\s*([\w_]+)\s*=\s*(.+)', line)
                      if match:
                          key = match.group(1).strip()
                          val_str = match.group(2).strip()
                          try:
                              # Safely evaluate strings, booleans, and arrays (e.g., '[...]')
                              configs[key] = ast.literal_eval(val_str)
                          except Exception as e:
                              print(f'Warning: Could not parse config {key}={val_str}. Error: {e}')

# Ensure your primary default repository dataset is always attached safely
default_dataset = f'{os.environ[\"KAGGLE_USERNAME\"]}/{os.environ[\"KAGGLE_DATASET_NAME\"]}'
if default_dataset not in configs['dataset_sources']:
    configs['dataset_sources'].append(default_dataset)

# Write parsed configs to temporary file for bash execution step
with open('parsed_config.json', 'w') as cf:
    json.dump(configs, cf)
"

# 4. Extract standard parameters for Metadata Template
FILENAME=$(basename "${{ env.CHANGED_FILE }}" .ipynb)
SLUG=$(echo "$FILENAME" | tr '[:upper:]' '[:lower:]' | tr ' _' '-')

# Helper vars to format final configuration directly into json template strings
GPU=$(python -c "import json; print(json.load(open('parsed_config.json'))['enable_gpu'])" | tr '[:upper:]' '[:lower:]')
TPU=$(python -c "import json; print(json.load(open('parsed_config.json'))['enable_tpu'])" | tr '[:upper:]' '[:lower:]')
KEYWORDS=$(python -c "import json; print(json.load(open('parsed_config.json'))['keywords'])")
DATASETS=$(python -c "import json; print(json.load(open('parsed_config.json'))['dataset_sources'])")
KERNELS=$(python -c "import json; print(json.load(open('parsed_config.json'))['kernel_sources'])")

# 5. Compile the fully scaled metadata map
cat <<EOF > kernel-metadata.json

{
"id": "${{ secrets.KAGGLE_USERNAME }}/$SLUG",
"title": "$FILENAME",
"code_file": "${{ env.CHANGED_FILE }}",
"language": "python",
"kernel_type": "notebook",
"is_private": true,
"enable_gpu": $GPU,
"enable_tpu": $TPU,
"enable_internet": true,
"keywords": $KEYWORDS,
"dataset_sources": $DATASETS,
"kernel_sources": $KERNELS,
"competition_sources": []
}
EOF
