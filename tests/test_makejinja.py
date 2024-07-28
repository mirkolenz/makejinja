from dataclasses import dataclass
from pathlib import Path

import pytest
from click.testing import CliRunner


@dataclass
class Paths:
    input: Path
    baseline: Path
    output: Path

    def __repr__(self) -> str:
        return "makejinja"


@pytest.fixture(scope="session")
def exec(tmp_path_factory: pytest.TempPathFactory) -> Paths:
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

    return Paths(input_path, baseline_path, output_path)


def _dir_content(path: Path) -> set[Path]:
    return {item.relative_to(path) for item in path.rglob("*")}


def test_dir_content(exec: Paths):
    assert _dir_content(exec.baseline) == _dir_content(exec.output)


def test_file_content(exec: Paths):
    paths = _dir_content(exec.baseline)

    for item in paths:
        baseline_path = exec.baseline / item
        output_path = exec.output / item

        if baseline_path.is_file() and output_path.is_file():
            baseline = baseline_path.read_text()
            output = output_path.read_text()

            assert baseline.strip() == output.strip(), str(item)
