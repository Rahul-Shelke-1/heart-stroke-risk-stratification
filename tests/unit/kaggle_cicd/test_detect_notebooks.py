from unittest.mock import mock_open, patch

from scripts.kaggle_cicd.detect_notebooks import (find_notebooks,
                                                  get_changed_files,
                                                  write_outputs)

################################################################################
# test : find_notebooks()
################################################################################

def test_find_notebooks():
    files = [
        "README.md",
        "notebooks/train.ipynb",
        "src/main.py"
    ]

    assert find_notebooks(files) == [
        "notebooks/train.ipynb"
    ]

def test_find_notebooks_empty():
    files = [
            "README.md",
            "src/main.py"
        ]
    assert find_notebooks(files) == []

################################################################################
# test : get_changed_files()
################################################################################

@patch("subprocess.check_output")
def test_get_changed_files(mock_check_output):
    mock_check_output.return_value = (
        "notebooks/train.ipynb\nREADME.md\n"
    )

    files = get_changed_files()

    assert files == [
        "notebooks/train.ipynb",
        "README.md",
    ]

################################################################################
# test : write_output()
################################################################################

@patch.dict("os.environ", {"GITHUB_OUTPUT": "tmp/output"})
@patch("builtins.open", new_callable=mock_open)
def test_write_output(mock_file):

    write_outputs(True, "notebooks/train.ipynb")

    handle = mock_file()

    handle.write.assert_any_call("execute=true\n")
    handle.write.assert_any_call("notebook=notebooks/train.ipynb\n")
