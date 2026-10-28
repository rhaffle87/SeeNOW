# tests/test_worker.py
from core.config_manager import ConfigManager
from core.agent_worker import AgentWorker

def test_agent_worker_initialization():
    cfg = ConfigManager()
    status_updates = []
    result_updates = []

    def dummy_status(state: str, msg: str):
        status_updates.append((state, msg))

    def dummy_result(data: dict):
        result_updates.append(data)

    worker = AgentWorker(cfg, dummy_status, dummy_result)
    assert worker.daemon is True
    assert worker.browser_engine is not None
    assert worker.llm_client is not None
    assert worker.is_running is False
    assert worker.task_queue is None

def test_agent_worker_start_and_exit():
    cfg = ConfigManager()
    worker = AgentWorker(cfg, lambda s, m: None, lambda d: None)
    worker.start()
    worker.ready_event.wait(timeout=2.0)
    assert worker.ready_event.is_set()
    assert worker.task_queue is not None

    # Dispatch exit command
    worker.dispatch("exit")
    worker.join(timeout=3.0)
    assert not worker.is_alive()
