#!/usr/bin/env python3

"""Module containing the PMX gentop class and the command line interface."""
import os
import argparse
import shutil
from pathlib import Path
from typing import Mapping
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper


class Pmxgentop:
    """Wrapper class for the `PMX gentop <https://github.com/deGrootLab/pmx>`_ module.

    Args:
        input_top_zip_path (str): Path the input GROMACS topology TOP and ITP files in zip format. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/topology.zip>`_. Accepted formats: zip.
        output_top_zip_path (str): Path the output TOP topology in zip format. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_output_topology.zip>`_. Accepted formats: zip.
        properties (dic):
            * **force_field** (*str*) - ("amber99sb-star-ildn-mut") Forcefield.
            * **split** (*bool*) - (False) Print a 3 to 1 letter residue list.
            * **scale_mass** (*bool*) - (False) Scale mass.
            * **output_top_name** (*str*) - ("gentop.top") Name of the output top file.
            * **pmx_path** (*str*) - ("pmx") Path to the PMX command line interface.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **container_path** (*str*) - (None)  Path to the binary executable of your container.
            * **container_image** (*str*) - ("gromacs/gromacs:latest") Container Image identifier.
            * **container_volume_path** (*str*) - ("/inout") Path to an internal directory in the container.
            * **container_working_dir** (*str*) - (None) Path to the internal CWD in the container.
            * **container_user_id** (*str*) - (None) User number id to be mapped inside the container.
            * **container_shell_path** (*str*) - ("/bin/bash") Path to the binary executable of the container shell.
    """

    def __init__(self, input_top_zip_path: str, output_top_zip_path: str, properties: Mapping = None, **kwargs) -> None:
        properties = properties or {}

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
        # self.search_itp = properties.get('search_itp', False)
        self.scale_mass = properties.get('scale_mass', False)
        self.dna = properties.get('dna', False)
        self.rna = properties.get('rna', False)
        # Properties common in all PMX BB
        self.gmx_lib = properties.get('gmx_lib', None)
        self.pmx_path = properties.get('pmx_path', 'pmx')

        # Properties common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')
        self.remove_tmp = properties.get('remove_tmp', True)
        self.restart = properties.get('restart', False)

        # container Specific
        self.container_path = properties.get('container_path')
        self.container_image = properties.get('container_image', 'gromacs/gromacs:latest')
        self.container_volume_path = properties.get('container_volume_path', '/inout')
        self.container_working_dir = properties.get('container_working_dir')
        self.container_user_id = properties.get('container_user_id')
        self.container_shell_path = properties.get('container_shell_path', '/bin/bash')

        # Check the properties
        fu.check_properties(self, properties)

    @launchlogger
    def launch(self) -> int:
        """Launches the execution of the PMX gentop module."""
        tmp_files = []

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # Check if executable is exists
        if not self.container_path:
            if not Path(self.pmx_path).is_file():
                if not shutil.which(self.pmx_path):
                    raise FileNotFoundError('Executable %s not found. Check if it is installed in your system and correctly defined in the properties' % self.pmx_path)

        # Restart if needed
        if self.restart:
            if fu.check_complete_files(self.io_dict["out"].values()):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log,
                       self.global_log)
                return 0

        # Unzip topology to topology_out
        top_file = fu.unzip_top(zip_file=self.input_top_zip_path, out_log=out_log)
        top_dir = str(Path(top_file).parent)
        tmp_files.append(top_dir)
        fu.log(f"top_file: {top_file}", out_log)

        #  If using containers create unique dir and copy nothing there
        container_io_dict = fu.copy_to_container(self.container_path, self.container_volume_path, self.io_dict)

        if self.container_path:
            fu.log(f"Unique dir: {container_io_dict['unique_dir']}", out_log)
            fu.log(f"{container_io_dict['unique_dir']} files: {os.listdir(container_io_dict['unique_dir'])}", out_log)
            # Copy all files of the unzipped topology to unique dir
            fu.log(f"Copy all files of the unzipped original topology to unique dir:", out_log)
            shutil.copytree(top_dir, Path(container_io_dict.get("unique_dir")).joinpath(Path(top_dir).name))
            top_file = str(Path(self.container_volume_path).joinpath(Path(top_dir).name, Path(top_file).name))

        output_file_name = fu.create_name(prefix=self.prefix, step=self.step, name=str(Path(top_file).name))
        unique_dir_output_file = str(Path(fu.create_unique_dir()).joinpath(output_file_name))
        fu.log(f"unique_dir_output_file: {unique_dir_output_file}", out_log)

        if self.container_path:
            fu.log("Change references for container:", out_log)
            unique_dir_output_file = str(Path(self.container_volume_path).joinpath(Path(output_file_name)))
            fu.log(f"    unique_dir_output_file: {unique_dir_output_file}", out_log)

        cmd = [self.pmx_path, 'gentop',
               '-o', str(Path(unique_dir_output_file)),
               '-ff', self.force_field,
               '-p', top_file]

        if self.split:
            cmd.append('--split')
        if self.scale_mass:
            cmd.append('--scale_mass')

        new_env = None
        if self.gmx_lib:
            new_env = os.environ.copy()
            new_env['GMXLIB'] = self.gmx_lib

        cmd = fu.create_cmd_line(cmd, container_path=self.container_path,
                                 host_volume=container_io_dict.get("unique_dir"),
                                 container_volume=self.container_volume_path,
                                 container_working_dir=self.container_working_dir,
                                 container_user_uid=self.container_user_id,
                                 container_shell_path=self.container_shell_path,
                                 container_image=self.container_image,
                                 out_log=out_log, global_log=self.global_log)

        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log, new_env).launch()

        if self.container_path:
            unique_dir_output_file = str(Path(container_io_dict.get("unique_dir")).joinpath(Path(unique_dir_output_file).name))

        # Remove paths from top file
        with open(Path(unique_dir_output_file)) as top_fh:
            top_lines = top_fh.readlines()
        with open(Path(unique_dir_output_file), 'w') as top_fh:
            for line in top_lines:
                top_fh.write(line.replace(str(Path(unique_dir_output_file).parent)+'/', ''))
        # Copy the not modified itp files
        for orig_itp_file in Path(top_dir).iterdir():
            fu.log(f'Check if {str(Path(unique_dir_output_file).parent.joinpath(Path(orig_itp_file).name))} exists', out_log, self.global_log)
            if not Path(unique_dir_output_file).parent.joinpath(Path(orig_itp_file).name).exists():
                shutil.copy(orig_itp_file, Path(unique_dir_output_file).parent)
                fu.log(f'Copying {str(orig_itp_file)} to: {str(Path(unique_dir_output_file).parent)}', out_log, self.global_log)

        # zip topology
        fu.log('Compressing topology to: %s' % self.io_dict["out"]["output_top_zip_path"], out_log, self.global_log)
        fu.zip_top(zip_file=self.io_dict["out"]["output_top_zip_path"], top_file=str(Path(unique_dir_output_file)), out_log=out_log)

        tmp_files.append(top_dir)
        tmp_files.append(container_io_dict.get("unique_dir"))
        if self.remove_tmp:
            fu.rm_file_list(tmp_files, out_log=out_log)

        return returncode


def main():
    parser = argparse.ArgumentParser(description="Run PMX mutate module",
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
    Pmxgentop(input_top_zip_path=args.input_top_zip_path, output_top_zip_path=args.output_top_zip_path,
              properties=properties).launch()


if __name__ == '__main__':
    main()
