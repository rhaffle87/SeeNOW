# tests/test_browser_engine.py
import os
import sys
from unittest.mock import patch
from core.browser_engine import resource_path, BrowserEngine

def test_resource_path():
    path = resource_path("test_file.txt")
    assert isinstance(path, str)
    assert path.endswith("test_file.txt")

    # Test with _MEIPASS set (PyInstaller bundle mode)
    with patch.object(sys, "_MEIPASS", "C:\\fake\\bundle", create=True):
        bundle_path = resource_path("core/som_injector.js")
        assert bundle_path == os.path.join("C:\\fake\\bundle", "core/som_injector.js")

def test_find_chrome_executable():
    # If Chrome/Edge is installed on test system, it returns a string; otherwise None
    exe = BrowserEngine.find_chrome_executable()
    if exe is not None:
        assert isinstance(exe, str)
        assert os.path.isfile(exe)
