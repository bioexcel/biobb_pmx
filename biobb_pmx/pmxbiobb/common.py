""" Common functions for package biobb_pmx.pmx """

import re
from typing import Union, Iterable, Mapping


MUTATION_DICT = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'ASPH': 'B', 'ASPP': 'B', 'ASH': 'B', 'CYS': 'C', 'CYS2': 'C', 'CYN': 'C', 'CYX': 'CX', 'CYM': 'CM', 'CYSH': 'C', 'GLU': 'E', 'GLUH': 'J', 'GLUP': 'J', 'GLH': 'J', 'GLN': 'Q', 'GLY': 'G', 'HIS': 'H', 'HIE': 'X', 'HISE': 'X', 'HSE': 'X', 'HIP': 'Z', 'HSP': 'Z', 'HISH': 'Z', 'HID': 'H', 'HSD': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K', 'LYSH': 'K', 'LYP': 'K', 'LYN': 'O', 'LSN': 'O', 'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S', 'SP1': 'SP1', 'SP2': 'SP2', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V', 'A': 'A', 'T': 'T', 'C': 'C', 'G': 'G', 'U': 'U'}


def create_mutations_file(input_mutations_path: str, mutation_list: Union[str, Iterable[str]], mutation_dict: Mapping) -> str:
    try:
        # Check if self.mutation_list is a string
        mutation_list = mutation_list.replace(" ", "").split(',')
    except AttributeError:
        pass
    pattern = re.compile(r"(?P<chain>[a-zA-Z])*:?(?P<resnum>\d+)(?P<mt>[a-zA-Z0-9]+)")
    with open(input_mutations_path, 'w') as mut_file:
        for mut in mutation_list:
            mut_groups_dict = pattern.match(mut.strip()).groupdict()
            if mut_groups_dict.get('chain'):
                mut_file.write(mut_groups_dict.get('chain') + ' ')
            mut_file.write(mut_groups_dict.get('resnum') + ' ')
            if not mut_groups_dict.get('mt').upper() in mutation_dict.keys():
                raise TypeError(
                    f"{mut_groups_dict.get('mt').upper()} is not a valid AA code or NA code. Possible values are {mutation_dict.keys()}")
            mut_file.write(mutation_dict[mut_groups_dict.get('mt').upper()])
            mut_file.write('\n')

    return input_mutations_path
