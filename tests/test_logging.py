import json
from src.logging_utils import get_logger, log_event

def test_logging_isolated_to_temp_directory(tmp_path):
    logger = get_logger("unit_test_logging", tmp_path)
    log_event(logger, "unit_test_event", value=123)
    log_file = tmp_path / "unit_test_logging.log"
    assert log_file.exists()
    payload = json.loads(log_file.read_text().strip().splitlines()[-1])
    assert payload["event"] == "unit_test_event"
    assert payload["value"] == 123
