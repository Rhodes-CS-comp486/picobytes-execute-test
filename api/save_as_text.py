import sys
import json
from pathlib import Path


directory = Path("to_execute")
directory.mkdir(parents=True, exist_ok=True)

# Read JSON from stdin
json_data = sys.stdin.read()



try:
    data = json.loads(json_data)  # Parse JSON into a dictionary

    code = data.get("code", "")
    tests = data.get("tests", "")

    file_path1 = directory / "code.c"
    file_path1.write_text(code, encoding="utf-8")

    if tests:
        file_path2 = directory / "tests.c"
        file_path2.write_text(tests, encoding="utf-8")

    print("Files saved successfully.", file=sys.stderr)

except json.JSONDecodeError as e:
    print(f"JSON decoding error: {e}", file=sys.stderr)
    sys.exit(1)
