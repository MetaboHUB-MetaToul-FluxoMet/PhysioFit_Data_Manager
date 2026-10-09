from pathlib import Path

import pandas as pd
import pytest

from physiofit_manager.cli import parse_args, process

TEST_DATA = Path(__file__).resolve().parents[1] / "test-data"


def run(tmp_path, *extra_args):
    output = tmp_path / "physiofit_input.tsv"
    args = parse_args().parse_args([
        "-b", str(TEST_DATA / "biomass.tsv"),
        "-c", str(TEST_DATA / "conc.tsv"),
        "-e", str(output),
        *extra_args,
    ])
    process(args)
    return output


def test_experiment_name_comes_first(tmp_path):
    data = pd.read_csv(run(tmp_path, "-x", "WT_rep1"), sep="\t")
    assert list(data.columns[:3]) == ["experiments", "time", "X"]
    assert set(data["experiments"]) == {"WT_rep1"}


def test_default_experiment_name_is_biomass_file_name(tmp_path):
    data = pd.read_csv(run(tmp_path), sep="\t")
    assert set(data["experiments"]) == {"biomass"}


def test_output_matches_expected_file(tmp_path):
    data = pd.read_csv(run(tmp_path, "-x", "experiment"), sep="\t")
    expected = pd.read_csv(TEST_DATA / "output.tsv", sep="\t")
    pd.testing.assert_frame_equal(data, expected)


def test_output_is_accepted_by_physiofit(tmp_path):
    io = pytest.importorskip("physiofit.base.io")
    data = io.IoHandler.read_data(str(run(tmp_path, "-x", "experiment")))
    assert list(data.columns) == ["experiments", "time", "X", "glc"]
