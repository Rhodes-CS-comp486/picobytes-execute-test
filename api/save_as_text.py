from pathlib import Path
import sys

directory = Path("to_execute")
directory.mkdir(parents=True, exist_ok=True)



def clear_and_save_with_test(code : str, tests: str):
    file_path1 = directory / "code.txt"
    file_path2 = directory / "tests.txt"
    with file_path1.open("w") as text_file:
        pass
    with file_path1.open("w") as text_file:
        print({code}, file=text_file)
    with file_path2.open("w") as text_file:
        pass
    with file_path2.open("w") as text_file:
        print({tests}, file=text_file)

def clear_and_save_wihtout_test(code : str):
    file_path1 = directory / "code.txt"
    file_path2 = directory / "tests.txt"
    with file_path1.open("w") as text_file:
        pass
    with file_path1.open("w") as text_file:
        print({code}, file=text_file)
    with file_path2.open("w") as text_file:
        pass

if len(sys.argv) == 2:
    code = sys.argv[1]
    clear_and_save_wihtout_test(code)
elif len(sys.argv) > 2:
    code = sys.argv[1]
    tests = sys.argv[2]
    clear_and_save_with_test(code, tests)
else: print("we messed up")