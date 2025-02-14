import sys
import subprocess
args = sys.argv

def main():
    val = subprocess.run(["bash","-c",  "pwd"])
    print(val.stdout)

if __name__=="__main__":
    main()


