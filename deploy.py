import os
import subprocess
import shutil

# Define the paths
lambda_code_dir = "lambda"
layer_code_dir = "create_layer"
python_code_dir = "python"
zip_file = "lambda.zip"
layer_zip_file = "layer_content.zip"

# Remove old zip file
if os.path.exists(zip_file):
    print("Removing old lambda zip")
    os.remove(zip_file)

print("Managing dependencies")
subprocess.run(["python", "reqs.py"], check=True)

# Zip the lambda code
print("Zipping lambda code")
shutil.make_archive(lambda_code_dir, 'zip', lambda_code_dir)

# Change directory to terraform
os.chdir("terraform")

# Run terraform
print("Running terraform")
try:
    subprocess.run(["terraform", "init"], check=True)
    subprocess.run(["terraform", "apply"], check=True)
except subprocess.CalledProcessError as e:
    print(e)
    exit(1)