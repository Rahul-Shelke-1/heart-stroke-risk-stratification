import sys

from src.exception.base import HeartStrokeException, error_message_detail


# -----------------------------
# Helper function to generate exception context
# -----------------------------
def raise_dummy_error():
    return 1 / 0

# -----------------------------
# Test error_message_detail
# -----------------------------
def test_error_message_detail_contains_file_line_and_error():
    try:
        raise_dummy_error()
    except Exception as e:
        result = error_message_detail(e, sys)

        assert "division by zero" in result
        assert "Error occurred in python script name" in result
        assert "line number" in result

# -----------------------------
# Test __str__ method consistency
# -----------------------------
def test_heartstroke_exception_str():
    try:
        raise_dummy_error()
    except Exception as e:
        exc = HeartStrokeException(e, sys)

        assert str(exc) == exc.error_message

# -----------------------------
# Test error captures correct filename
# -----------------------------
def test_error_contains_current_file_name():
    try:
        raise_dummy_error()
    except Exception as e:
        result = error_message_detail(e, sys)

        # current file name should be part of traceback
        assert "test_exception.py" in result
