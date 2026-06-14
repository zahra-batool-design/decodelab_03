import sys
import subprocess

print("--- DIAGNOSTIC ENVIRONMENT PATH ---")
print(sys.executable)
print("-----------------------------------")

# Force installation to the exact environment executing this script
subprocess.run([sys.executable, "-m", "pip", "install", "scikit-learn", "numpy"])