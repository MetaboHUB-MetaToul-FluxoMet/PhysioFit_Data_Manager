import argparse

import numpy as np
import pandas as pd


def parse_args():
    """
    Parse arguments from user input

    :return: Argument Parser
    """

    parser = argparse.ArgumentParser("PhysioFit data manager")

    parser.add_argument(
        "-b", "--biomass_file",
        type=str,
        help="Path to biomass file"
    )
    parser.add_argument(
        "-c", "--concentrations_file",
        type=str,
        help="Path to metabolite concentrations file"
    )
    parser.add_argument(
        "-e", "--export_path",
        type=str,
        help="Path to where the generated .mflux mtf file will be exported"
    )
    return parser


def process(args):
    """
    Command Line Interface process of the manager

    :param args: Arguments passed by the parser
    :return: Excel file export message
    """

    try:
        biomass_df = pd.read_csv(
            args.biomass_file,
            sep="\t",
            dtype=float
        )
        concentrations_df = pd.read_csv(
            args.concentrations_file,
            sep="\t",
            dtype=float
        )
    except Exception:
        raise IOError("Error while reading input data file")

    biomass_cols = ["X", "time"]
    for col in biomass_cols:
        if col not in biomass_df.columns:
            raise DataError(
                f"The column {col} is missing from the biomass file"
            )
    if len(biomass_df.columns) > 2:
        raise DataError(
            "Too many columns in biomass data file. Number of columns: "
            f"{len(biomass_df.columns)}"
        )

    if "time" not in concentrations_df.columns:
        raise DataError(
            "The column 'time' must be given in the concentrations file"
        )
    if len(concentrations_df.columns) < 2:
        raise DataError(
            "Concentrations file must contain values for at least one "
            "metabolite"
        )

    biomass_df.set_index("time", inplace=True)
    concentrations_df.set_index("time", inplace=True)

    final_df = pd.merge(
        left=biomass_df,
        right=concentrations_df,
        how="outer",
        on="time"
    )
    final_df = final_df.sort_index()
    final_df.to_csv(
        args.export_path,
        sep="\t",
        na_rep=np.nan
    )

class DataError(Exception):
    pass


def main():

    cli_parser = parse_args()
    cli_args = cli_parser.parse_args()
    process(cli_args)



