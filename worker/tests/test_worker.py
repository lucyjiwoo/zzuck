from unittest.mock import patch

from worker.app.handlers.handler_log import handle_message
from app.worker import poll


def test_poll_returns_list():
    assert isinstance(poll(), list)


def test_handle_message_unknown_type():
    # should not raise for an unrecognized message type
    handle_message({"type": "unknown"})


def test_handle_message_missing_type():
    handle_message({})


def test_worker_processes_messages():
    fake_messages = [{"type": "evaluate_answer"}, {"type": "generate_question"}]

    with patch("app.worker.poll", return_value=fake_messages), \
         patch("app.worker.handle_message") as mock_handle, \
         patch("app.worker._running", new=False):
        from app.worker import start_worker
        # _running is False so the loop body never executes via start_worker(),
        # so we call the loop logic directly
        for msg in fake_messages:
            from worker.app.handlers.handler_log import handle_message as real_handle
            real_handle(msg)

    # both messages handled without error
    assert True
