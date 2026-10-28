# tests/test_browser_engine.py
import os
import sys
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
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

def test_is_connection_alive_when_disconnected():
    async def run():
        engine = BrowserEngine()
        return await engine.is_connection_alive()

    assert asyncio.run(run()) is False

def test_is_connection_alive_switches_stale_page():
    async def run():
        engine = BrowserEngine()
        engine.browser = MagicMock()
        engine.context = MagicMock()

        stale_page = MagicMock()
        stale_page.is_closed.return_value = True

        active_page = MagicMock()
        active_page.is_closed.return_value = False
        active_page.evaluate = AsyncMock(return_value=True)

        engine.context.pages = [stale_page, active_page]
        engine.page = stale_page

        alive = await engine.is_connection_alive()
        return alive, engine.page == active_page

    alive, switched = asyncio.run(run())
    assert alive is True
    assert switched is True

def test_apply_anti_blur_stealth_registers_init_script():
    async def run():
        engine = BrowserEngine()
        engine.context = MagicMock()
        engine.context.add_init_script = AsyncMock()

        page = MagicMock()
        page.is_closed.return_value = False
        page.evaluate = AsyncMock()
        engine.page = page

        await engine.apply_anti_blur_stealth(page)
        engine.context.add_init_script.assert_called_once()
        page.evaluate.assert_called_once()
        # Verify script contains key anti-cheat protections
        script_arg = engine.context.add_init_script.call_args[0][0]
        assert "hasFocus" in script_arg
        assert "visibilityState" in script_arg
        assert "window.open" in script_arg

    asyncio.run(run())

def test_auto_focus_exam_tab_selects_exam_content():
    async def run():
        engine = BrowserEngine()
        engine.context = MagicMock()

        intro_page = MagicMock()
        intro_page.is_closed.return_value = False
        intro_page.url = "https://talent.shixizhi.huawei.com/iexam/123/examInfo?examId=456"

        exam_page = MagicMock()
        exam_page.is_closed.return_value = False
        exam_page.url = "https://talent.shixizhi.huawei.com/iexam/123/examContent?examId=456"
        exam_page.bring_to_front = AsyncMock()
        exam_page.evaluate = AsyncMock()

        engine.context.pages = [intro_page, exam_page]
        engine.page = intro_page

        focused = await engine.auto_focus_exam_tab()
        assert focused == exam_page
        assert engine.page == exam_page
        exam_page.bring_to_front.assert_called_once()

    asyncio.run(run())
