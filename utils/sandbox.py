import subprocess
import resource
import os

def run_plugin_sandboxed(plugin_path, timeout=60, mem_limit_mb=256, extra_env=None):
    def set_limits():
        resource.setrlimit(resource.RLIMIT_CPU, (timeout, timeout + 1))
        resource.setrlimit(resource.RLIMIT_AS, (mem_limit_mb * 1024 * 1024, mem_limit_mb * 1024 * 1024))
        os.setuid(65534)  # nobody user; на Linux

    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    process = subprocess.Popen(
        ["python", plugin_path],
        preexec_fn=set_limits,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.dirname(plugin_path)
    )
    out, err = process.communicate(timeout=timeout+5)
    return process.returncode, out.decode(), err.decode()