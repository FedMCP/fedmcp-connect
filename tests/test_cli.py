import subprocess
import shutil

def test_scaffold(tmp_path):
    name = tmp_path / "demo"
    subprocess.run(
        ["python", "-m", "fmcpx", "init", str(name)],
        check=True,
    )
    assert (name / "connector.py").exists()
    assert (name / "tool.schema.json").exists()
    # Clean up
    shutil.rmtree(name)
