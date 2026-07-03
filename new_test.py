import subprocess

result = subprocess.run(
        ["python","testing.py"],
    capture_output=True,
    text=True,
    check=True
)

print(result)