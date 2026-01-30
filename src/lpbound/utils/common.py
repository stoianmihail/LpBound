import numpy as np
import json
import os

# Query utils.
from lpbound.acyclic.join_graph.vertex import Vertex
from lpbound.acyclic.join_graph.predicate import EqualityPredicate, InequalityPredicate

class CustomJSONEncoder(json.JSONEncoder):
  def default(self, o):
    if isinstance(o, Vertex):
      return o.to_dict()
    if isinstance(o, (EqualityPredicate, InequalityPredicate)):
      return o.__dict__
    if isinstance(o, tuple):
      return list(o)
    if isinstance(o, set):
      return list(o)

    # NEW: Handle NumPy scalar types (int64, float64, bool_, etc.)
    if isinstance(o, np.generic):
      return o.item()

    # OPTIONAL: Handle NumPy arrays as lists
    if isinstance(o, np.ndarray):
      return o.tolist()
    return super().default(o)

def pretty_dict(d):
  return json.dumps(d, indent=2, cls=CustomJSONEncoder)

def read_json(json_path):
  # Check if the file exists.
  assert os.path.isfile(json_path)

  # And read the data.
  f = open(json_path, 'r', encoding='utf-8')
  data = json.load(f)
  f.close()

  # Return it.
  return data

def write_json(json_path, json_content, format=True):
  f = open(json_path, 'w', encoding='utf-8')

  # Plain write.
  if not format:
    f.write(json_content)
  else:
    # Dump nicely.
    json.dump(json_content, f, indent=2, ensure_ascii=False)
  f.close()

def read_jsonl(jsonl_path, skip_comments=True, verbose=False):
  if verbose:
    print(f'Loading queries from {jsonl_path} with skip_comments={skip_comments}')
  
  join_sizes = []
  with open(jsonl_path, 'r') as f:
    for line in f:
      # Strip line.
      line = line.strip()

      # Skip lines with comments if being told.
      if line.startswith('//'):
        if skip_comments:
          continue
        else:
          # Remove the comments.
          line = line.strip('//').strip()
    
      # Skip empty lines.
      if line:
        try:
          tmp = json.loads(line)
          join_sizes.append(tmp)
        except (json.JSONDecodeError, KeyError) as e:
          print(f'Warning: Failed to parse line in JSONL file: {line[:100]}..')
          print(f'Error: {e}')
          continue
  return join_sizes

def safe_write(file_path, content, allowed_exts={'.json', '.jsonl', '.txt', '.sql'}):
  '''
    Safely writes text content to a file.
    - Ensures parent directories exist.
    - Checks file extension against allowed list.
    - Performs a plain write (no formatting / encoding magic).

    Args:
      file_path (str): Full path to the output file.
      content (str): Text content to write.
      allowed_exts (set[str]): Allowed file extensions.
  '''
  # Ensure the directory exists
  os.makedirs(os.path.dirname(file_path), exist_ok=True)

  # Check the extension
  _, ext = os.path.splitext(file_path)
  if ext not in allowed_exts:
    raise ValueError(f'Unsupported file extension \'{ext}\'. Allowed extensions: {sorted(allowed_exts)}')

  # Perform the write
  with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
  return