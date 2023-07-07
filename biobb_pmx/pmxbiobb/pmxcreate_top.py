#!/usr/bin/env python3

"""Module containing the PMX create_top class and the command line interface."""
import os
import sys
from pathlib import Path, PurePath
import shutil
import argparse
from typing import Mapping
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger


class Pmxcreate_top(BiobbObject):
    """
    | biobb_pmx Pmxcreate_top
    | Wrapper class for the `PMX create_top <https://github.com/deGrootLab/pmx>`_ module.

    Args:
        input_topology1_path (str): Path to the input topology file 1. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand.itp>`_. Accepted formats: itp (edam:format_3883).
        input_topology2_path (str): Path to the input topology file 2. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand.itp>`_. Accepted formats: itp (edam:format_3883).
        output_topology_path (str): Path to the complete ligand topology file. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/ligand_top.zip>`_. Accepted formats: zip (edam:format_3987).

        properties (dic):
            * **force_field** (*str*) - ("amber99sb-star-ildn-mut.ff") Force-field to be included in the generated topology.
            * **water** (*str*) - ("tip3p") Water model to be included in the generated topology.
            * **system_name** (*str*) - ("Pmx topology") System name to be included in the generated topology.
            * **mols** (*list*) - ([['Protein',1],['Ligand',1]]) Molecules to be included in the generated topology.
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

            from biobb_pmx.pmxbiobb.pmxcreate_top import pmxcreate_top
            prop = {
                'remove_tmp' : True
            }
            pmxcreate_top(input_topology1_path='/path/to/myTopology1.itp',
                    input_topology2_path='/path/to/myTopology2.itp',
                    output_topology_path='/path/to/myMergedTopology.zip',
                    properties=prop)

    Info:
        * wrapped_software:
            * name: PMX create_top
            * version: >=1.0.1
            * license: GNU
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_topology1_path: str, input_topology2_path: str, output_topology_path: str,
                 properties: Mapping = None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {"input_topology1_path": input_topology1_path, "input_topology2_path": input_topology2_path},
            "out": {"output_topology_path": output_topology_path}
        }

        # Properties specific for BB
        self.force_field = properties.get('force_field', "amber99sb-star-ildn-mut.ff")
        self.water = properties.get('water', "tip3p")
        self.system_name = properties.get('system_name', "Pmx topology")
        self.mols = properties.get('mols', [['Protein', 1], ['Ligand', 1]])

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
        """Execute the :class:`Pmxcreate_top <pmx.pmxcreate_top.Pmxcreate_top>` pmx.pmxcreate_top.Pmxcreate_top object."""
#        os.chdir("/Users/hospital/BioBB/Notebooks_dev/biobb_wf_pmx_tutorial_ligands/biobb_wf_pmx_tutorial/notebooks")
        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        self.out_log.info('Running create_top from pmx package...\n')

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir()
        self.out_log.info('Creating %s temporary folder' % self.tmp_folder)

        itp = os.path.basename(os.path.normpath(self.stage_io_dict["in"]["input_topology1_path"]))
        self.out_log.info('Creating %s itp file in temporary folder' % itp)
        itp_local = str(PurePath(self.tmp_folder).joinpath(itp))
        shutil.copyfile(self.io_dict['in']['input_topology1_path'], itp_local)

        itp2 = os.path.basename(os.path.normpath(self.stage_io_dict["in"]["input_topology2_path"]))
        self.out_log.info('Creating %s itp file in temporary folder' % itp2)
        itp2_local = str(PurePath(self.tmp_folder).joinpath(itp2))
        shutil.copyfile(self.io_dict['in']['input_topology2_path'], itp2_local)

        top_local = str(PurePath(self.tmp_folder).joinpath("topology.top"))

        # _create_top function, taken from the pmx AZ tutorial:
        # https://github.com/deGrootLab/pmx/blob/develop/tutorials/AZtutorial.py
        fp = open(top_local, 'w')
        # BioBB signature
        fp.write("; Topology generated by the BioBB pmxcreate_top building block\n\n")
        # ff itp
        fp.write('#include "%s/forcefield.itp"\n\n' % self.force_field)
        # additional itp
        # for i in self.itps:
        #    fp.write('#include "%s"\n' % i)
        fp.write('#include "%s"\n' % itp)
        fp.write('#include "%s"\n\n' % itp2)
        # water itp
        fp.write('#include "%s/%s.itp"\n' % (self.force_field, self.water))
        # ions
        fp.write('#include "%s/ions.itp"\n\n' % self.force_field)
        # system
        fp.write('[ system ]\n')
        fp.write('{0}\n\n'.format(self.system_name))
        # molecules
        fp.write('[ molecules ]\n')
        for mol in self.mols:
            fp.write('%s %s\n' % (mol[0], mol[1]))
        fp.close()

        # zip topology
        current_cwd = os.getcwd()
        top_final = str(PurePath(current_cwd).joinpath(self.io_dict["out"]["output_topology_path"]))

        os.chdir(self.tmp_folder)
        fu.log('Compressing topology to: %s' % top_final, self.out_log, self.global_log)
        fu.zip_top(zip_file=top_final, top_file="topology.top", out_log=self.out_log)
        os.chdir(current_cwd)

        self.out_log.info('Exit code 0\n')

        # Run Biobb block
        # self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        self.tmp_files.append(self.stage_io_dict.get("unique_dir"))
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)
        return self.return_code


def pmxcreate_top(input_topology1_path: str, input_topology2_path: str, output_topology_path: str,
                  properties: dict = None, **kwargs) -> int:
    """Execute the :class:`Pmxcreate_top <pmx.pmxcreate_top.Pmxcreate_top>` class and
    execute the :meth:`launch() <pmx.pmxmcreate_top.Pmxmcreate_top.launch> method."""

    return Pmxcreate_top(input_topology1_path=input_topology1_path, input_topology2_path=input_topology2_path,
                         output_topology_path=output_topology_path,
                         properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Run PMX create_top module",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_topology1_path', required=True, help="Path to the input topology file 1")
    required_args.add_argument('--input_topology2_path', required=True, help="Path to the input topology file 2")
    required_args.add_argument('--output_topology_path', required=True, help="Path to the complete ligand topology file")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    pmxcreate_top(input_topology1_path=args.input_topology1_path, input_topology2_path=args.input_topology2_path,
                  output_topology_path=args.output_topology_path,
                  properties=properties)


if __name__ == '__main__':
    main()
