#!/usr/bin/env python3
"""Integration smoke against the REAL desktop process and its loopback JSON-lines control server.

No snapshot pixels, window-size guess or wall-clock performance assertions: tests exercise
document creation, native ZIP save/reopen and real UI screenshot + CPU page renderer.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import socket
import struct
import sys
import time
import zipfile


def request(port: int, id_: int, method: str, params: dict | None = None) -> object:
    msg = {"id": id_, "method": method, "params": params or {}}
    with socket.create_connection(("127.0.0.1", port), timeout=8) as conn:
        conn.settimeout(75)
        conn.sendall((json.dumps(msg, separators=(",", ":")) + "\n").encode())
        response = b""
        while b"\n" not in response:
            chunk = conn.recv(32768)
            if not chunk:
                raise AssertionError(f"{method}: control connection closed without reply")
            response += chunk
            if len(response) > 12 * 1024 * 1024:
                raise AssertionError(f"{method}: oversized response")
    decoded = json.loads(response.split(b"\n", 1)[0])
    assert decoded.get("id") == id_, (method, decoded)
    assert decoded.get("ok") is True, (method, decoded)
    return decoded.get("result")


def png_size(path: pathlib.Path) -> tuple[int, int]:
    data = path.read_bytes()
    assert data.startswith(b"\x89PNG\r\n\x1a\n"), f"not a PNG: {path}"
    assert len(data) > 256, f"unexpectedly small PNG: {path}"
    width, height = struct.unpack(">II", data[16:24])
    assert 1 <= width <= 10000 and 1 <= height <= 10000, (width, height)
    return width, height


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--out", type=pathlib.Path, required=True)
    a = parser.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)

    deadline = time.monotonic() + 90
    while True:
        try:
            with socket.create_connection(("127.0.0.1", a.port), timeout=1):
                break
        except OSError:
            if time.monotonic() >= deadline:
                raise AssertionError("native desktop did not expose its loopback control server")
            time.sleep(0.5)

    commands = [
        ("engine.execute", {"command": "file.new", "params": {"title": "Native CI"}}),
        ("engine.execute", {"command": "frame.create", "params": {
            "rect": [50, 50, 240, 200], "content": "text", "text": "native desktop smoke", "caret": False
        }}),
    ]
    answers = [request(a.port, idx, method, params) for idx, (method, params) in enumerate(commands, 1)]
    assert isinstance(answers[1], dict) and answers[1].get("id") is not None, answers

    inspect = request(a.port, 3, "document.inspect")
    assert isinstance(inspect, dict), inspect
    ui = request(a.port, 4, "ui.inspect")
    assert isinstance(ui, dict), ui

    document = a.out / "native-ci.designcraft"
    save = request(a.port, 5, "app.save", {"path": str(document)})
    assert isinstance(save, dict) and document.exists() and document.stat().st_size > 128, save
    with zipfile.ZipFile(document) as archive:
        assert "document.json" in archive.namelist(), archive.namelist()
        structured = json.loads(archive.read("document.json"))
        assert structured.get("title") == "Native CI", structured.get("title")

    rendered = a.out / "page.png"
    request(a.port, 6, "ui.render", {"path": str(rendered), "page": 0, "scale": 1})
    width, height = png_size(rendered)
    assert width > 100 and height > 100, (width, height)

    screenshot = a.out / "window.png"
    shot = request(a.port, 7, "ui.screenshot", {"path": str(screenshot), "focus": False})
    assert isinstance(shot, dict), shot
    width, height = png_size(screenshot)
    assert width >= 300 and height >= 200, (width, height)

    opened = request(a.port, 8, "app.open", {"path": str(document)})
    assert isinstance(opened, dict), opened
    inspect_again = request(a.port, 9, "document.inspect")
    assert isinstance(inspect_again, dict), inspect_again

    print(json.dumps({"result": "PASS", "native_zip_bytes": document.stat().st_size,
                      "page_png_bytes": rendered.stat().st_size,
                      "window_png_bytes": screenshot.stat().st_size}, sort_keys=True))
    request(a.port, 10, "app.quit")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (AssertionError, OSError, ValueError, json.JSONDecodeError) as error:
        print(f"native desktop E2E FAILED: {error}", file=sys.stderr)
        sys.exit(1)
