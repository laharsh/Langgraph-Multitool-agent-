"""Regenerate Python gRPC stubs from proto/agent.proto."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / "proto" / "agent.proto"
OUT = ROOT / "src" / "grpc_gen"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "__init__.py").write_text("", encoding="utf-8")
    cmd = [
        sys.executable,
        "-m",
        "grpc_tools.protoc",
        f"-I{ROOT / 'proto'}",
        f"--python_out={OUT}",
        f"--grpc_python_out={OUT}",
        str(PROTO),
    ]
    subprocess.check_call(cmd, cwd=ROOT)

    # Fix absolute import in generated grpc stub
    grpc_file = OUT / "agent_pb2_grpc.py"
    text = grpc_file.read_text(encoding="utf-8")
    text = text.replace(
        "import agent_pb2 as agent__pb2",
        "from src.grpc_gen import agent_pb2 as agent__pb2",
    )
    grpc_file.write_text(text, encoding="utf-8")
    print(f"Generated stubs in {OUT}")


if __name__ == "__main__":
    main()
