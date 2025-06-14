from dataclasses import dataclass
from pathlib import Path

import pytest
from click.testing import CliRunner


@dataclass(slots=True, frozen=True)
class MakejinjaPaths:
    """Paths used in makejinja test execution.

    Attributes:
        input: Path to input template directories
        baseline: Path to expected output files
        output: Path to actual generated output files
    """

    input: Path
    baseline: Path
    output: Path

    def __repr__(self) -> str:
        return "makejinja"


@pytest.fixture(scope="session")
def test_run(tmp_path_factory: pytest.TempPathFactory) -> MakejinjaPaths:
    """Execute makejinja on test data and return paths to input, expected, and actual output."""
    assert __package__ is not None
    data_path = Path(__package__, "data")
    input_path = data_path / "input"
    baseline_path = data_path / "output"
    output_path = tmp_path_factory.mktemp("data")

    with pytest.MonkeyPatch.context() as m:
        m.chdir(data_path)
        runner = CliRunner()

        # Need to import it AFTER chdir
        from makejinja.cli import makejinja_cli

        runner.invoke(
            makejinja_cli,
            [
                # Override it here to use our tmp_path
                "--output",
                str(output_path),
            ],
            catch_exceptions=False,
            color=True,
        )

    return MakejinjaPaths(input_path, baseline_path, output_path)


def _dir_content(path: Path) -> set[Path]:
    return {item.relative_to(path) for item in path.rglob("*")}


def test_output_structure(test_run: MakejinjaPaths):
    """Test that makejinja generates the expected directory structure."""
    expected_files = _dir_content(test_run.baseline)
    actual_files = _dir_content(test_run.output)

    if expected_files != actual_files:
        missing = sorted(expected_files - actual_files)
        extra = sorted(actual_files - expected_files)
        pytest.fail(f"Directory structure mismatch. Missing: {missing}, Extra: {extra}")


def test_template_rendering(test_run: MakejinjaPaths):
    """Test that makejinja renders all templates with correct content."""
    paths = _dir_content(test_run.baseline)

    for item in paths:
        baseline_path = test_run.baseline / item
        output_path = test_run.output / item

        if baseline_path.is_file() and output_path.is_file():
            expected_content = baseline_path.read_text()
            actual_content = output_path.read_text()

            if expected_content.strip() != actual_content.strip():
                pytest.fail(
                    f"Content mismatch in {item}: expected '{expected_content.strip()}', got '{actual_content.strip()}'"
                )


def test_custom_delimiters(test_run: MakejinjaPaths):
    """Test that custom Jinja delimiters (<< >>, <% %>) work correctly."""
    not_empty_file = test_run.output / "not-empty.yaml"
    content = not_empty_file.read_text()

    assert "NOT EMPTY" in content, (
        f"Custom delimiters not working. Expected 'NOT EMPTY' in {not_empty_file}"
    )


def test_file_specific_data(test_run: MakejinjaPaths):
    """Test that file-specific data loading works correctly."""
    file_specific_output = test_run.output / "file-specific.yaml"
    content = file_specific_output.read_text()

    # Should contain data from data1.yaml
    assert "Value from data1" in content, (
        f"File-specific data not loaded. Expected 'Value from data1' in {file_specific_output}"
    )
    assert "item1" in content and "item2" in content, (
        f"File-specific list data not loaded correctly in {file_specific_output}"
    )


def test_plugin_features(test_run: MakejinjaPaths):
    """Test that custom plugin filters and functions work."""
    # Test that secret files are excluded by plugin path filter
    secret_file = test_run.output / "secret.yaml"
    assert not secret_file.exists(), (
        f"Secret file should be excluded by plugin but exists: {secret_file}"
    )


def test_partial_inclusion(test_run: MakejinjaPaths):
    """Test that partial template inclusion works."""
    ui_lovelace_file = test_run.output / "ui-lovelace.yaml"
    content = ui_lovelace_file.read_text()

    # Should contain content from include.yaml.partial
    assert "icon: mdi:home" in content, (
        f"Partial inclusion not working. Expected 'icon: mdi:home' in {ui_lovelace_file}"
    )


def test_empty_template_handling(test_run: MakejinjaPaths):
    """Test that empty templates are handled correctly."""
    # The empty.yaml.jinja should not produce output (contains only comments)
    empty_file = test_run.output / "empty.yaml"
    assert not empty_file.exists(), (
        f"Empty template should not generate output file but {empty_file} exists"
    )


def test_nested_directory_processing(test_run: MakejinjaPaths):
    """Test that nested directories are processed correctly."""
    nested_file = test_run.output / "views" / "home.yaml"
    assert nested_file.exists(), (
        f"Nested directory processing failed. Expected {nested_file} to exist"
    )

    content = nested_file.read_text()
    assert len(content.strip()) > 0, (
        f"Nested template should have content but {nested_file} is empty"
    )
