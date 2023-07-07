#!/usr/bin/env python3

"""Module containing the PMX mutate class and the command line interface."""
import os
from pathlib import Path
import sys
import shutil
import argparse
from typing import Mapping
from biobb_pmx.pmxbiobb.common import create_mutations_file, MUTATION_DICT
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger


class Pmxmutate(BiobbObject):
    """
    | biobb_pmx Pmxmutate
    | Wrapper class for the `PMX mutate <https://github.com/deGrootLab/pmx>`_ module.

    Args:
        input_structure_path (str): Path to the input structure file. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/frame99.pdb>`_. Accepted formats: pdb (edam:format_1476), gro (edam:format_2033).
        output_structure_path (str): Path to the output structure file. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_output_structure.pdb>`_. Accepted formats: pdb (edam:format_1476), gro (edam:format_2033).
        input_b_structure_path (str) (Optional): Path to the mutated input structure file. File type: input. Accepted formats: pdb (edam:format_1476), gro (edam:format_2033).
        properties (dic):
            * **mutation_list** (*str*) - ("2Ala") Mutation list in the format "Chain:Resnum MUT_AA_Code" or "Chain:Resnum MUT_NA_Code"  (no spaces between the elements) separated by commas. If no chain is provided as chain code all the chains in the pdb file will be mutated. ie: "A:15CYS". Possible MUT_AA_Code: 'ALA', 'ARG', 'ASN', 'ASP', 'ASPH', 'ASPP', 'ASH', 'CYS', 'CYS2', 'CYN', 'CYX', 'CYM', 'CYSH', 'GLU', 'GLUH', 'GLUP', 'GLH', 'GLN', 'GLY', 'HIS', 'HIE', 'HISE', 'HSE', 'HIP', 'HSP', 'HISH', 'HID', 'HSD', 'ILE', 'LEU', 'LYS', 'LYSH', 'LYP', 'LYN', 'LSN', 'MET', 'PHE', 'PRO', 'SER', 'SP1', 'SP2', 'THR', 'TRP', 'TYR', 'VAL'. Possible MUT_NA_Codes: 'A', 'T', 'C', 'G', 'U'.
            * **force_field** (*str*) - ("amber99sb-star-ildn-mut") Forcefield to use.
            * **resinfo** (*bool*) - (False) Show the list of 3-letter -> 1-letter residues.
            * **gmx_lib** (*str*) - ("$CONDA_PREFIX/lib/python3.7/site-packages/pmx/data/mutff/") Path to the GMXLIB folder in your computer.
            * **binary_path** (*str*) - ("pmx") Path to the PMX command line interface.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **container_path** (*str*) - (None)  Path to the binary executable of your container.
            * **container_image** (*str*) - (None) Container Image identifier.
            * **container_volume_path** (*str*) - ("/inout") Path to an internal directory in the container.
            * **container_working_dir** (*str*) - (None) Path to the internal CWD in the container.
            * **container_user_id** (*str*) - (None) User number id to be mapped inside the container.
            * **container_shell_path** (*str*) - ("/bin/bash") Path to the binary executable of the container shell.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_pmx.pmxbiobb.pmxmutate import pmxmutate
            prop = {
                'mutation_list': '2Ala, 3Val',
                'gmx_lib': '/path/to/myGMXLIB/',
                'force_field': 'amber99sb-star-ildn-mut'
            }
            pmxmutate(input_structure_path='/path/to/myStructure.pdb',
                    output_structure_path='/path/to/newStructure.pdb',
                    input_b_structure_path='/path/to/myStructureB.pdb'
                    properties=prop)

    Info:
        * wrapped_software:
            * name: PMX mutate
            * version: >=1.0.1
            * license: GNU
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_structure_path: str, output_structure_path: str, input_b_structure_path: str = None,
                 properties: Mapping = None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {"input_structure_path": input_structure_path, "input_b_structure_path": input_b_structure_path},
            "out": {"output_structure_path": output_structure_path}
        }

        # Properties specific for BB
        self.force_field = properties.get('force_field', "amber99sb-star-ildn-mut")
        self.resinfo = properties.get('resinfo', False)
        self.mutation_list = properties.get('mutation_list', '2Ala')
        self.input_mutations_file = properties.get('mutations_file')

        # Properties common in all PMX BB
        self.gmx_lib = properties.get('gmx_lib', None)
        if not self.gmx_lib and os.environ.get('CONDA_PREFIX'):
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
            self.gmx_lib = str(
                Path(os.environ.get('CONDA_PREFIX')).joinpath(f"lib/python{python_version}/site-packages/pmx/data/mutff/"))
            if properties.get('container_path'):
                self.gmx_lib = str(Path('/usr/local/').joinpath("lib/python3.7/site-packages/pmx/data/mutff/"))
        self.binary_path = properties.get('binary_path', 'pmx')

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`Pmxmutate <pmx.pmxmutate.Pmxmutate>` pmx.pmxmutate.Pmxmutate object."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Check if executable exists
        if not self.container_path:
            if not Path(self.binary_path).is_file():
                if not shutil.which(self.binary_path):
                    raise FileNotFoundError(
                        'Executable %s not found. Check if it is installed in your system and correctly defined in the properties' % self.binary_path)

        # Generate mutations file

        mutations_dir = fu.create_unique_dir()
        self.input_mutations_file = create_mutations_file(input_mutations_path=str(Path(mutations_dir).joinpath('mutations.txt')),
                                                          mutation_list=self.mutation_list,
                                                          mutation_dict=MUTATION_DICT)

        # Copy extra files to container: mutations file
        if self.container_path:
            fu.log('Container execution enabled', self.out_log)

            shutil.copy2(self.input_mutations_file, self.stage_io_dict.get("unique_dir"))
            self.input_mutations_file = str(Path(self.container_volume_path).joinpath(Path(self.input_mutations_file).name))

        self.cmd = [self.binary_path, 'mutate',
                    '-f', self.stage_io_dict["in"]["input_structure_path"],
                    '-o', self.stage_io_dict["out"]["output_structure_path"],
                    '-ff', self.force_field,
                    '--script', self.input_mutations_file]

        if self.stage_io_dict["in"].get("input_b_structure_path"):
            self.cmd.append('-fB')
            self.cmd.append(self.stage_io_dict["in"]["input_b_structure_path"])
        if self.resinfo:
            self.cmd.append('-resinfo')

        if self.gmx_lib:
            self.env_vars_dict['GMXLIB'] = self.gmx_lib

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        self.tmp_files.append(self.stage_io_dict.get("unique_dir"))
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)
        return self.return_code


def pmxmutate(input_structure_path: str, output_structure_path: str,
              input_b_structure_path: str = None, properties: dict = None,
              **kwargs) -> int:
    """Execute the :class:`Pmxmutate <pmx.pmxmutate.Pmxmutate>` class and
    execute the :meth:`launch() <pmx.pmxmutate.Pmxmutate.launch> method."""

    return Pmxmutate(input_structure_path=input_structure_path,
                     output_structure_path=output_structure_path,
                     input_b_structure_path=input_b_structure_path,
                     properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Run PMX mutate module",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_structure_path', required=True, help="Path to the input structure file")
    required_args.add_argument('--output_structure_path', required=True, help="Path to the output structure file")
    parser.add_argument('--input_b_structure_path', required=False, help="Path to the mutated input structure file")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    pmxmutate(input_structure_path=args.input_structure_path,
              output_structure_path=args.output_structure_path,
              input_b_structure_path=args.input_b_structure_path,
              properties=properties)


if __name__ == '__main__':
    main()
