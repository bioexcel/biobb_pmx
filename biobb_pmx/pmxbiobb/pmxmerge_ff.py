#!/usr/bin/env python3

"""Module containing the PMX merge_ff class and the command line interface."""
import os
import sys
from pathlib import Path
import glob
import argparse
from pmx import ligand_alchemy
from typing import Mapping
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger


class Pmxmerge_ff(BiobbObject):
    """
    | biobb_pmx Pmxmerge_ff
    | Wrapper class for the `PMX merge_ff <https://github.com/deGrootLab/pmx>`_ module.

    Args:
        input_topology_path (str): Path to the input ligand topologies as a zip file containing a list of itp files. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand_itps.zip>`_. Accepted formats: zip (edam:format_3987).
        output_topology_path (str): Path to the merged ligand topology file. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand.itp>`_. Accepted formats: itp (edam:format_3883).

        properties (dic):
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

            from biobb_pmx.pmxbiobb.pmxmerge_ff import pmxmerge_ff
            prop = {
                'remove_tmp' : True
            }
            pmxmerge_ff(input_topology_path='/path/to/myTopologies.zip',
                    output_topology_path='/path/to/myMergedTopology.itp',
                    properties=prop)

    Info:
        * wrapped_software:
            * name: PMX merge_ff
            * version: >=1.0.1
            * license: GNU
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_topology_path: str, output_topology_path: str, properties: Mapping = None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {"input_topology_path": input_topology_path},
            "out": {"output_topology_path": output_topology_path}
        }

        # Properties specific for BB
        # None yet

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
        """Execute the :class:`Pmxmerge_ff <pmx.pmxmerge_ff.Pmxmerge_ff>` pmx.pmxmerge_ff.Pmxmerge_ff object."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir()
        self.out_log.info('Creating %s temporary folder' % self.tmp_folder)

        fu.unzip_list(self.stage_io_dict["in"]["input_topology_path"], self.tmp_folder, out_log=self.out_log)
        files = glob.glob(self.tmp_folder+"/*.itp")
        ffsIn_list = []
        for itp in files:
            ffsIn_list.append(itp)

        self.out_log.info('Running merge_FF_files from pmx package...\n')
        ligand_alchemy._merge_FF_files(self.stage_io_dict["out"]["output_topology_path"], ffsIn=ffsIn_list)
        # ffsIn=[self.stage_io_dict["in"]["input_topology1_path"],self.stage_io_dict["in"]["input_topology2_path"]] )

        self.out_log.info('Exit code 0\n')

        if self.gmx_lib:
            self.env_vars_dict['GMXLIB'] = self.gmx_lib

        # Run Biobb block
        # self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        self.tmp_files.append(self.stage_io_dict.get("unique_dir"))
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)
        return self.return_code


def pmxmerge_ff(input_topology_path: str, output_topology_path: str, properties: dict = None, **kwargs) -> int:
    """Execute the :class:`Pmxmerge_ff <pmx.pmxmerge_ff.Pmxmerge_ff>` class and
    execute the :meth:`launch() <pmx.pmxmerge_ff.Pmxmerge_ff.launch> method."""

    return Pmxmerge_ff(input_topology_path=input_topology_path,
                       output_topology_path=output_topology_path,
                       properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Run PMX merge_ff module",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_topology_path', required=True, help="Path to the input ligand topologies as a zip file containing a list of itp files.")
    required_args.add_argument('--output_topology_path', required=True, help="Path to the merged ligand topology file")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    pmxmerge_ff(input_topology_path=args.input_topology_path,
                output_topology_path=args.output_topology_path,
                properties=properties)


if __name__ == '__main__':
    main()
