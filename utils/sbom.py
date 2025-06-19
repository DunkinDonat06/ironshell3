import subprocess

def generate_cyclonedx_sbom(target_dir, output_path="sbom_cyclonedx.json"):
    cmd = ["syft", target_dir, "-o", "cyclonedx-json"]
    with open(output_path, "w") as f:
        subprocess.run(cmd, stdout=f, check=True)
    return output_path