"""Common functions for package biobb_pmx.pmx"""

import re
from typing import Iterable, Mapping, Optional, Union

MUTATION_DICT = {
    "ALA": "A",
    "ARG": "R",
    "ASN": "N",
    "ASP": "D",
    "ASPH": "B",
    "ASPP": "B",
    "ASH": "B",
    "CYS": "C",
    "CYS2": "C",
    "CYN": "C",
    "CYX": "CX",
    "CYM": "CM",
    "CYSH": "C",
    "GLU": "E",
    "GLUH": "J",
    "GLUP": "J",
    "GLH": "J",
    "GLN": "Q",
    "GLY": "G",
    "HIS": "H",
    "HIE": "X",
    "HISE": "X",
    "HSE": "X",
    "HIP": "Z",
    "HSP": "Z",
    "HISH": "Z",
    "HID": "H",
    "HSD": "H",
    "ILE": "I",
    "LEU": "L",
    "LYS": "K",
    "LYSH": "K",
    "LYP": "K",
    "LYN": "O",
    "LSN": "O",
    "MET": "M",
    "PHE": "F",
    "PRO": "P",
    "SER": "S",
    "SP1": "SP1",
    "SP2": "SP2",
    "THR": "T",
    "TRP": "W",
    "TYR": "Y",
    "VAL": "V",
    "A": "A",
    "T": "T",
    "C": "C",
    "G": "G",
    "U": "U",
}


def create_mutations_file(
    input_mutations_path: str,
    mutation_list: Union[str, Iterable[str]],
    mutation_dict: Mapping,
) -> str:
    try:
        # Check if self.mutation_list is a string
        mutation_list = mutation_list.replace(" ", "").split(",")  # type: ignore
    except AttributeError:
        pass
    pattern = re.compile(r"(?P<chain>[a-zA-Z])*:?(?P<resnum>\d+)(?P<mt>[a-zA-Z0-9]+)")
    with open(input_mutations_path, "w") as mut_file:
        for mut in mutation_list:
            match = pattern.match(mut.strip())
            if match:
                mut_groups_dict = match.groupdict()
                if mut_groups_dict.get("chain"):
                    mut_file.write(mut_groups_dict.get("chain", "") + " ")
                mut_file.write(mut_groups_dict.get("resnum", "") + " ")
                if mut_groups_dict.get("mt", "").upper() not in mutation_dict.keys():
                    raise TypeError(
                        f"{mut_groups_dict.get('mt','').upper()} is not a valid AA code or NA code. Possible values are {mutation_dict.keys()}"
                    )
                mut_file.write(mutation_dict[mut_groups_dict.get("mt", "").upper()])
                mut_file.write("\n")

    return input_mutations_path


# TODO: Move this function to biobb_common.tools.file_utils
def _from_string_to_list(input_data: Optional[Union[str, list[str]]]) -> list[str]:
    """
    Converts a string to a list, splitting by commas or spaces. If the input is already a list, returns it as is.
    Returns an empty list if input_data is None.

    Parameters:
        input_data (str, list, or None): The string, list, or None value to convert.

    Returns:
        list: A list of string elements or an empty list if input_data is None.
    """
    if input_data is None:
        return []

    if isinstance(input_data, list):
        # If input is already a list, return it
        return input_data

    # If input is a string, determine the delimiter based on presence of commas
    delimiter = "," if "," in input_data else " "
    items = input_data.split(delimiter)

    # Remove whitespace from each item and ignore empty strings
    processed_items = [item.strip() for item in items if item.strip()]

    return processed_items
