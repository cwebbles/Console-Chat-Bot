import os
import subprocess
import shutil

# Define the paths
lambda_code_dir = "./lambda"
zip_file = "lambda.zip"

# Remove old zip file
if os.path.exists(zip_file):
    print("Removing old zip file")
    os.remove(zip_file)

# Zip the lambda code
print("Zipping lambda code")
shutil.make_archive(lambda_code_dir, 'zip', lambda_code_dir)

# Change directory to terraform
os.chdir("terraform")

# Run terraform
print("Running terraform")
try:
    subprocess.run(["terraform", "init"], check=True)
    subprocess.run(["terraform", "apply", "-auto-approve"], check=True)
except subprocess.CalledProcessError as e:
    print(e)
    exit(1)