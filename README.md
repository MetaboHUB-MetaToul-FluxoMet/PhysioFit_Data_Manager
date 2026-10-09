# PhysioFit_Data_Manager

Merges separate biomass and metabolite concentration time courses into a single input file for [PhysioFit](https://github.com/MetaSys-LISBP/PhysioFit). It is used as a connector in the fluxomics workflow on [Workflow4Metabolomics](https://workflow4metabolomics.usegalaxy.fr/).

## Installation

From bioconda:

```bash
conda install -c conda-forge -c bioconda physiofit_data_manager
```

Or from a clone of this repository:

```bash
pip install .
```

## Usage

```bash
physiofit_manager -b biomass.tsv -c concentrations.tsv -e physiofit_input.tsv -x WT_rep1
```

| Option | Description |
| --- | --- |
| `-b`, `--biomass_file` | Tab-separated file with exactly two columns: `time` and `X` (biomass) |
| `-c`, `--concentrations_file` | Tab-separated file with a `time` column and one column per metabolite |
| `-e`, `--export_path` | Path of the PhysioFit input file to write |
| `-x`, `--experiment` | Experiment name written in the `experiments` column (default: biomass file name without its extension) |

The output is tab-separated, with the columns PhysioFit expects: `experiments`, `time`, `X`, then one column per metabolite. Rows from both inputs are merged on `time` and sorted; a value measured in only one file is `nan` in the other's columns.

## Development

The project is managed with [Poetry](https://python-poetry.org/):

```bash
poetry install
poetry run pytest
```

The test that reads the output with PhysioFit is skipped unless `physiofit` is installed in the environment.

## License

GPLv3, see [LICENSE](LICENSE).
