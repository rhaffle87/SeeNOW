# tests/test_config.py
import os
import tempfile
import pytest
from core.config_manager import ConfigManager, mask_secret, validate_url

def test_validate_url():
    assert validate_url("http://localhost:20128/v1") is True
    assert validate_url("https://api.openai.com/v1") is True
    assert validate_url("ftp://invalid-url.com") is False
    assert validate_url("") is False
    assert validate_url("not_a_url") is False

def test_mask_secret():
    assert mask_secret("") == "[NOT SET]"
    assert mask_secret("123") == "****"
    assert mask_secret("sk-1234567890abcdef") == "sk-****cdef"

def test_config_load_and_save():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_cfg_file = os.path.join(tmpdir, "config.json")
        cfg = ConfigManager(config_path=tmp_cfg_file)

        assert cfg.get("execution_mode") == "auto_click_answer_only"
        assert cfg.get("router_base_url") == "http://localhost:20128/v1"

        # Save valid data
        cfg.save({
            "router_base_url": "https://custom-router.com/v1",
            "action_delay": 2.5
        })

        # Reload from disk
        cfg2 = ConfigManager(config_path=tmp_cfg_file)
        assert cfg2.get("router_base_url") == "https://custom-router.com/v1"
        assert cfg2.get("action_delay") == 2.5

def test_config_invalid_url_rejected():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_cfg_file = os.path.join(tmpdir, "config.json")
        cfg = ConfigManager(config_path=tmp_cfg_file)

        with pytest.raises(ValueError):
            cfg.save({"router_base_url": "invalid_url_without_scheme"})

def test_config_corrupted_json_recovery():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_cfg_file = os.path.join(tmpdir, "config.json")
        # Write corrupted content
        with open(tmp_cfg_file, "w") as f:
            f.write("{corrupt_json_structure!!")

        # ConfigManager should gracefully fall back to default config without crashing
        cfg = ConfigManager(config_path=tmp_cfg_file)
        assert cfg.get("router_base_url") == "http://localhost:20128/v1"

def test_config_atomic_write_leaves_no_tmp_on_success():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_cfg_file = os.path.join(tmpdir, "config.json")
        cfg = ConfigManager(config_path=tmp_cfg_file)
        cfg.save({"action_delay": 3.0})

        assert os.path.exists(tmp_cfg_file)
        assert not os.path.exists(f"{tmp_cfg_file}.tmp")
