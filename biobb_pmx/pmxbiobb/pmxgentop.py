#!/usr/bin/env python3

"""Module containing the PMX gentop class and the command line interface."""
import os
import sys
import argparse
import shutil
from pathlib import Path
from typing import Mapping
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger


class Pmxgentop(BiobbObject):
    """
    | biobb_pmx Pmxgentop
    | Wrapper class for the `PMX gentop <https://github.com/deGrootLab/pmx>`_ module.

    Args:
        input_top_zip_path (str): Path the input GROMACS topology TOP and ITP files in zip format. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/topology.zip>`_. Accepted formats: zip (edam:format_3987).
        output_top_zip_path (str): Path the output TOP topology in zip format. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_output_topology.zip>`_. Accepted formats: zip (edam:format_3987).
        properties (dic):
            * **force_field** (*str*) - ("amber99sb-star-ildn-mut") Force field to use. If **input_top_zip_path** is a top file, it's not necessary to specify the forcefield, as it will be determined automatically. If **input_top_zip_path** is an itp file, then it's needed.
            * **split** (*bool*) - (False) Write separate topologies for the vdW and charge transformations.
            * **scale_mass** (*bool*) - (False) Scale the masses of morphing atoms so that dummies have a mass of 1.
            * **gmx_lib** (*str*) - ("$CONDA_PREFIX/lib/python3.7/site-packages/pmx/data/mutff/") Path to the GMXLIB folder in your computer.
            * **binary_path** (*str*) - ("pmx") Path to the PMX command line interface.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **container_path** (*str*) - (None)  Path to the binary executable of your container.
            * **container_image** (*str*) - ("gromacs/gromacs:latest") Container Image identifier.
            * **container_volume_path** (*str*) - ("/inout") Path to an internal directory in the container.
            * **container_working_dir** (*str*) - (None) Path to the internal CWD in the container.
            * **container_user_id** (*str*) - (None) User number id to be mapped inside the container.
            * **container_shell_path** (*str*) - ("/bin/bash") Path to the binary executable of the container shell.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_pmx.pmxbiobb.pmxgentop import pmxgentop
            prop = {
                'gmx_lib': '/path/to/myGMXLIB/',
                'force_field': 'amber99sb-star-ildn-mut'
            }
            pmxgentop(input_top_zip_path='/path/to/myTopology.zip',
                    output_top_zip_path='/path/to/newTopology.zip',
                    properties=prop)

    Info:
        * wrapped_software:
            * name: PMX gentop
            * version: >=1.0.1
            * license: GNU
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_top_zip_path: str, output_top_zip_path: str,
                 properties: Mapping = None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {},
            "out": {"output_top_zip_path": output_top_zip_path}
        }
        # Should not be copied inside container
        self.input_top_zip_path = input_top_zip_path

        # Properties specific for BB
        self.force_field = properties.get('force_field', "amber99sb-star-ildn-mut")
        self.split = properties.get('split', False)
        self.scale_mass = properties.get('scale_mass', False)

        # Properties common in all PMX BB
        self.gmx_lib = properties.get('gmx_lib', None)
        if not self.gmx_lib and os.environ.get('CONDA_PREFIX'):
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
            self.gmx_lib = str(
                Path(os.environ.get('CONDA_PREFIX')).joinpath(f"lib/python{python_version}/site-packages/pmx/data/mutff/"))
            if properties.get('container_path'):
                self.gmx_lib = str(Path('/usr/local/').joinpath("lib/python3.8/site-packages/pmx/data/mutff/"))
        self.binary_path = properties.get('binary_path', 'pmx')

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`Pmxgentop <pmx.pmxgentop.Pmxgentop>` pmx.pmxgentop.Pmxgentop object."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Check if executable exists
        if not self.container_path:
            if not Path(self.binary_path).is_file():
                if not shutil.which(self.binary_path):
                    raise FileNotFoundError('Executable %s not found. Check if it is installed in your system and correctly defined in the properties' % self.binary_path)

        # Unzip topology to topology_out
        top_file = fu.unzip_top(zip_file=self.input_top_zip_path, out_log=self.out_log)
        top_dir = str(Path(top_file).parent)

        # Copy extra files to container: topology folder
        if self.container_path:
            fu.log('Container execution enabled', self.out_log)
            fu.log(f"Unique dir: {self.stage_io_dict['unique_dir']}", self.out_log)
            fu.log(f"{self.stage_io_dict['unique_dir']} files: {os.listdir(self.stage_io_dict['unique_dir'])}", self.out_log)
            fu.log(f"Copy all files of the unzipped original topology to unique dir: {self.out_log}")
            shutil.copytree(top_dir, str(Path(self.stage_io_dict.get("unique_dir")).joinpath(Path(top_dir).name)))
            top_file = str(Path(self.container_volume_path).joinpath(Path(top_dir).name, Path(top_file).name))

        output_file_name = fu.create_name(prefix=self.prefix, step=self.step, name=str(Path(top_file).name))
        unique_dir_output_file = str(Path(fu.create_unique_dir()).joinpath(output_file_name))
        fu.log(f"unique_dir_output_file: {unique_dir_output_file}", self.out_log)

        if self.container_path:
            fu.log("Change references for container:", self.out_log)
            unique_dir_output_file = str(Path(self.container_volume_path).joinpath(Path(output_file_name)))
            fu.log(f"    unique_dir_output_file: {unique_dir_output_file}", self.out_log)

        self.cmd = [self.binary_path, 'gentop',
                    '-o', str(Path(unique_dir_output_file)),
                    '-ff', self.force_field,
                    '-p', top_file]

        if self.split:
            self.cmd.append('--split')
        if self.scale_mass:
            self.cmd.append('--scale_mass')

        if self.gmx_lib:
            self.env_vars_dict['GMXLIB'] = self.gmx_lib

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        if self.container_path:
            unique_dir_output_file = str(Path(self.stage_io_dict.get("unique_dir")).joinpath(Path(unique_dir_output_file).name))

        # Remove paths from top file
        with open(Path(unique_dir_output_file)) as top_fh:
            top_lines = top_fh.readlines()
        with open(Path(unique_dir_output_file), 'w') as top_fh:
            for line in top_lines:
                top_fh.write(line.replace(str(Path(unique_dir_output_file).parent)+'/', ''))
        # Copy the not modified itp files
        for orig_itp_file in Path(top_dir).iterdir():
            fu.log(f'Check if {str(Path(unique_dir_output_file).parent.joinpath(Path(orig_itp_file).name))} exists', self.out_log, self.global_log)
            if not Path(unique_dir_output_file).parent.joinpath(Path(orig_itp_file).name).exists():
                shutil.copy(orig_itp_file, Path(unique_dir_output_file).parent)
                fu.log(f'Copying {str(orig_itp_file)} to: {str(Path(unique_dir_output_file).parent)}', self.out_log, self.global_log)

        # zip topology
        fu.log('Compressing topology to: %s' % self.io_dict["out"]["output_top_zip_path"], self.out_log, self.global_log)
        fu.zip_top(zip_file=self.io_dict["out"]["output_top_zip_path"], top_file=str(Path(unique_dir_output_file)), out_log=self.out_log)

        self.tmp_files.extend([self.stage_io_dict.get("unique_dir"), top_dir])
        # self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)
        return self.return_code


def pmxgentop(input_top_zip_path: str, output_top_zip_path: str, properties: dict = None, **kwargs) -> int:
    """Execute the :class:`Pmxgentop <pmx.pmxgentop.Pmxgentop>` class and
    execute the :meth:`launch() <pmx.pmxgentop.Pmxgentop.launch> method."""

    return Pmxgentop(input_top_zip_path=input_top_zip_path,
                     output_top_zip_path=output_top_zip_path,
                     properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Wrapper class for the PMX gentop module",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_top_zip_path', required=True, help="Path to the input topology zip file")
    required_args.add_argument('--output_top_zip_path', required=True, help="Path to the output topology zip file")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    pmxgentop(input_top_zip_path=args.input_top_zip_path,
              output_top_zip_path=args.output_top_zip_path,
              properties=properties)


if __name__ == '__main__':
    main()
