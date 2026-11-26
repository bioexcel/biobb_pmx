"""Common functions for package biobb_pmx.pmx"""

import importlib.util
import re
import shutil
from pathlib import Path
from typing import Iterable, Mapping, Optional, Union

from biobb_common.generic.biobb_object import BiobbObject

# GMXLIB in a container: the mutff folder of the pmx package of the image, found by the image's
# own Python (its version is not known on the host). "\$" is expanded in the container, not on the host.
CONTAINER_GMXLIB = "\\$(python -c 'import os, pmx; print(os.path.dirname(pmx.__file__))')/data/mutff"


def check_binary(binary_path: str, container_path: Optional[str]) -> None:
    """Raise FileNotFoundError if the pmx executable (binary_path) is not on the host. Not checked with a container."""
    if not container_path and not shutil.which(binary_path):
        raise FileNotFoundError(
            f"Executable {binary_path} not found. Check if it is installed in your system and correctly defined in the properties"
        )


def set_gmxlib(block: BiobbObject) -> None:
    """Go from the gmx_lib property of the block to the GMXLIB of its command: gmx_lib (an absolute path on
    the host), or else the mutff folder of the pmx package of the Python environment (in a container, of the image)."""
    if block.container_path:
        if block.gmx_lib:
            block.env_vars_dict["GMXLIB"] = block.gmx_lib
        else:
            block.cmd = ["export", f"GMXLIB={CONTAINER_GMXLIB}", ";"] + block.cmd
    elif block.gmx_lib:
        # The command runs in the sandbox: a relative path is relative to the working directory
        block.env_vars_dict["GMXLIB"] = str(Path(block.gmx_lib).resolve())
    else:
        pmx_spec = importlib.util.find_spec("pmx")
        if pmx_spec and pmx_spec.origin:
            block.env_vars_dict["GMXLIB"] = str(Path(pmx_spec.origin).parent.joinpath("data", "mutff"))


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
