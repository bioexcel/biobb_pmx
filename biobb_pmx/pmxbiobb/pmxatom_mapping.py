#!/usr/bin/env python3

"""Module containing the PMX atom_mapping class and the command line interface."""
import os
import sys
from pathlib import Path
import shutil
import argparse
from typing import Mapping
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools.file_utils import launchlogger


class Pmxatom_mapping(BiobbObject):
    """
    | biobb_pmx Pmxatom_mapping
    | Wrapper class for the `PMX atom_mapping <https://github.com/deGrootLab/pmx>`_ module.

    Args:
        input_structure1_path (str): Path to the input ligand structure file 1. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_structure2_path (str): Path to the input ligand structure file 2. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_pairs1_path (str): Path to the output pairs for the ligand structure 1. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_mapping_pairs.dat>`_. Accepted formats: dat (edam:format_1637), txt (edam:format_2330).
        output_pairs2_path (str): Path to the output pairs for the ligand structure 2. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_mapping_pairs.dat>`_. Accepted formats: dat (edam:format_1637), txt (edam:format_2330).
        output_log_path (str): Path to the log file. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/atom_mapping.log>`_. Accepted formats: log (edam:format_2330), txt (edam:format_2330), out (edam:format_2330).
        output_structure1_path (str) (Optional): Path to the superimposed structure for the ligand structure 1. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/superimposed_ligand.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_structure2_path (str) (Optional): Path to the superimposed structure for the ligand structure 2. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/superimposed_ligand.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_morph1_path (str) (Optional): Path to the morphable atoms for the ligand structure 1. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/superimposed_ligand.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_morph2_path (str) (Optional): Path to the morphable atoms for the ligand structure 2. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/superimposed_ligand.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_scaffold1_path (str) (Optional): Path to the index of atoms to consider for the ligand structure 1. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/atoms_to_consider.ndx>`_. Accepted formats: ndx (edam:format_2033).
        output_scaffold2_path (str) (Optional): Path to the index of atoms to consider for the ligand structure 2. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/atoms_to_consider.ndx>`_. Accepted formats: ndx (edam:format_2033).
        output_score_path (str) (Optional): Path to the morphing score. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/morph_score.dat>`_. Accepted formats: dat (edam:format_1637), txt (edam:format_2330).

        properties (dic):
            * **noalignment** (*bool*) - (False) Should the alignment method be disabled.
            * **nomcs** (*bool*) - (False) Should the MCS method be disabled.
            * **noH2H** (*bool*) - (True) Should non-polar hydrogens be discarded from morphing into any other hydrogen.
            * **H2Hpolar** (*bool*) - (False) Should polar hydrogens be morphed into polar hydrogens.
            * **H2Heavy** (*bool*) - (False) Should hydrogen be morphed into a heavy atom.
            * **RingsOnly** (*bool*) - (False) Should rings only be used in the MCS search and alignemnt.
            * **dMCS** (*bool*) - (False) Should the distance criterium be also applied in the MCS based search.
            * **swap** (*bool*) - (False) Try swapping the molecule order which would be a cross-check and require double execution time.
            * **nochirality** (*bool*) - (True) Perform chirality check for MCS mapping.
            * **distance** (*float*) - (0.05) Distance (nm) between atoms to consider them morphable for alignment approach.
            * **timeout** (*int*) - (10) Maximum time (s) for an MCS search.
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

            from biobb_pmx.pmxbiobb.pmxatom_mapping import pmxatom_mapping
            prop = {
                'no-alignment' : True,
                'distance': 0.05
            }
            pmxatom_mapping(input_structure1_path='/path/to/myStructure1.pdb',
                    input_structure2_path='/path/to/myStructure2.pdb',
                    output_pairs1_path='/path/to/myPairs1.dat',
                    output_pairs2_path='/path/to/myPairs2.dat',
                    output_log_path='/path/to/myLog.log',
                    properties=prop)

    Info:
        * wrapped_software:
            * name: PMX atom_mapping
            * version: >=1.0.1
            * license: GNU
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_structure1_path: str, input_structure2_path: str, output_pairs1_path: str, output_pairs2_path: str,
                 output_log_path: str, output_structure1_path: str = None, output_structure2_path: str = None, output_morph1_path: str = None,
                 output_morph2_path: str = None, output_scaffold1_path: str = None, output_scaffold2_path: str = None, output_score_path: str = None,
                 properties: Mapping = None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {"input_structure1_path": input_structure1_path, "input_structure2_path": input_structure2_path},
            "out": {"output_pairs1_path": output_pairs1_path, "output_pairs2_path": output_pairs2_path,
                    "output_log_path": output_log_path,
                    "output_structure1_path": output_structure1_path, "output_structure2_path": output_structure2_path,
                    "output_morph1_path": output_morph1_path, "output_morph2_path": output_morph2_path,
                    "output_scaffold1_path": output_scaffold1_path, "output_scaffold2_path": output_scaffold2_path,
                    "output_score_path": output_score_path}
        }

        # Properties specific for BB
        # self.noalignment = properties.get('noalignment', False)
        # self.nomcs = properties.get('nomcs', False)
        # self.noH2H = properties.get('noH2H', True)
        # self.H2Hpolar = properties.get('H2Hpolar', False)
        # self.H2Heavy = properties.get('H2Heavy', False)
        # self.RingsOnly = properties.get('RingsOnly', False)
        # self.dMCS = properties.get('dMCS', False)
        # self.swap = properties.get('swap', False)
        # self.nochirality = properties.get('nochirality', True)
        # self.distance = properties.get('distance', 0.05)
        # self.timeout = properties.get('timeout', 10)

        self.noalignment = properties.get('noalignment')
        self.nomcs = properties.get('nomcs')
        self.noH2H = properties.get('noH2H')
        self.H2Hpolar = properties.get('H2Hpolar')
        self.H2Heavy = properties.get('H2Heavy')
        self.RingsOnly = properties.get('RingsOnly')
        self.dMCS = properties.get('dMCS')
        self.swap = properties.get('swap')
        self.nochirality = properties.get('nochirality')
        self.distance = properties.get('distance')
        self.timeout = properties.get('timeout')

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

        self.cmd = [self.binary_path, 'atomMapping',
                    '-i1', self.stage_io_dict["in"]["input_structure1_path"],
                    '-i2', self.stage_io_dict["in"]["input_structure2_path"],
                    '-o1', self.stage_io_dict["out"]["output_pairs1_path"],
                    '-o2', self.stage_io_dict["out"]["output_pairs2_path"],
                    '-log', self.stage_io_dict["out"]["output_log_path"]
                    ]

        if self.stage_io_dict["out"].get("output_structure1_path"):
            self.cmd.append('-opdb1')
            self.cmd.append(self.stage_io_dict["out"]["output_structure1_path"])

        if self.stage_io_dict["out"].get("output_structure2_path"):
            self.cmd.append('-opdb2')
            self.cmd.append(self.stage_io_dict["out"]["output_structure2_path"])

        if self.stage_io_dict["out"].get("output_morph1_path"):
            self.cmd.append('-opdbm1')
            self.cmd.append(self.stage_io_dict["out"]["output_morph1_path"])

        if self.stage_io_dict["out"].get("output_morph2_path"):
            self.cmd.append('-opdbm2')
            self.cmd.append(self.stage_io_dict["out"]["output_morph2_path"])

        if self.stage_io_dict["out"].get("output_scaffold1_path"):
            self.cmd.append('-n1')
            self.cmd.append(self.stage_io_dict["out"]["output_scaffold1_path"])

        if self.stage_io_dict["out"].get("output_scaffold2_path"):
            self.cmd.append('-n2')
            self.cmd.append(self.stage_io_dict["out"]["output_scaffold2_path"])

        if self.stage_io_dict["out"].get("output_score_path"):
            self.cmd.append('-score')
            self.cmd.append(self.stage_io_dict["out"]["output_score_path"])

        if self.noalignment:
            self.cmd.append('--no-alignment')
        if self.nomcs:
            self.cmd.append('--no-mcs')
        if self.noH2H:
            self.cmd.append('--no-H2H')
        if self.H2Hpolar:
            self.cmd.append('--H2Hpolar')
        if self.H2Heavy:
            self.cmd.append('--H2Heavy')
        if self.RingsOnly:
            self.cmd.append('--RingsOnly')
        if self.dMCS:
            self.cmd.append('--dMCS')
        if self.swap:
            self.cmd.append('--swap')
        if self.nochirality:
            self.cmd.append('--no-chirality')
        if self.distance:
            self.cmd.append('--d')
            self.cmd.append(str(self.distance))
        if self.timeout:
            self.cmd.append('--timeout')
            self.cmd.append(str(self.timeout))

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


def pmxatom_mapping(input_structure1_path: str, input_structure2_path: str, output_pairs1_path: str, output_pairs2_path: str,
                    output_log_path: str, output_structure1_path: str = None, output_structure2_path: str = None, output_morph1_path: str = None,
                    output_morph2_path: str = None, output_scaffold1_path: str = None, output_scaffold2_path: str = None, output_score_path: str = None,
                    properties: dict = None, **kwargs) -> int:
    """Execute the :class:`Pmxatom_mapping <pmx.pmxmutate.Pmxatom_mapping>` class and
    execute the :meth:`launch() <pmx.pmxatom_mapping.Pmxatom_mapping.launch> method."""

    return Pmxatom_mapping(input_structure1_path=input_structure1_path, input_structure2_path=input_structure2_path,
                           output_pairs1_path=output_pairs1_path, output_pairs2_path=output_pairs2_path,
                           output_log_path=output_log_path,
                           output_structure1_path=output_structure1_path, output_structure2_path=output_structure2_path,
                           output_morph1_path=output_morph1_path, output_morph2_path=output_morph2_path,
                           output_scaffold1_path=output_scaffold1_path, output_scaffold2_path=output_scaffold2_path,
                           output_score_path=output_score_path,
                           properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Run PMX atom mapping module",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_structure1_path', required=True, help="Path to the input ligand structure file 1")
    required_args.add_argument('--input_structure2_path', required=True, help="Path to the input ligand structure file 2")
    required_args.add_argument('--output_pairs1_path', required=True, help="Path to the output pairs for the ligand structure 1")
    required_args.add_argument('--output_pairs2_path', required=True, help="Path to the output pairs for the ligand structure 2")
    required_args.add_argument('--output_log_path', required=True, help="Path to the log file")
    parser.add_argument('--output_structure1_path', required=False, help="Path to the superimposed structure for the ligand structure 1")
    parser.add_argument('--output_structure2_path', required=False, help="Path to the superimposed structure for the ligand structure 2")
    parser.add_argument('--output_morph1_path', required=False, help="Path to the morphable atoms for the ligand structure 1")
    parser.add_argument('--output_morph2_path', required=False, help="Path to the morphable atoms for the ligand structure 2")
    parser.add_argument('--output_scaffold1_path', required=False, help="Path to the index of atoms to consider for the ligand structure 1")
    parser.add_argument('--output_scaffold2_path', required=False, help="Path to the index of atoms to consider for the ligand structure 2")
    parser.add_argument('--output_score_path', required=False, help="Path to the morphing score. File type: output")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    pmxatom_mapping(input_structure1_path=args.input_structure1_path, input_structure2_path=args.input_structure2_path,
                    output_pairs1_path=args.output_pairs1_path, output_pairs2_path=args.output_pairs2_path,
                    output_log_path=args.output_log_path,
                    output_structure1_path=args.output_structure1_path, output_structure2_path=args.output_structure2_path,
                    output_morph1_path=args.output_morph1_path, output_morph2_path=args.output_morph2_path,
                    output_scaffold1_path=args.output_scaffold1_path, output_scaffold2_path=args.output_scaffold2_path,
                    output_score_path=args.output_score_path,
                    properties=properties)


if __name__ == '__main__':
    main()
