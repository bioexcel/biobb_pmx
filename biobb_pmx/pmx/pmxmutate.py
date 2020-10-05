#!/usr/bin/env python3

"""Module containing the PMX mutate class and the command line interface."""
import os
from pathlib import Path
import re
import shutil
import argparse
from typing import Mapping
from Bio.PDB.Polypeptide import three_to_one
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper


class Pmxmutate:
    """Wrapper class for the `PMX mutate <https://github.com/deGrootLab/pmx>`_ module.

    Args:
        input_structure_path (str): Path to the input structure file. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/frame99.pdb>`_. Accepted formats: pdb, gro.
        output_structure_path (str): Path to the output structure file. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_output_structure.pdb>`_. Accepted formats: pdb, gro.
        input_b_structure_path (str) (Optional): Path to the mutated input structure file. File type: input. Accepted formats: pdb, gro.
        properties (dic):
            * **mutation_list** (*str*) ("Val2Ala") Mutation list in the format "Chain:WT_AA_ThreeLeterCode Resnum MUT_AA_ThreeLeterCode" (no spaces between the elements) separated by commas. If no chain is provided as chain code all the chains in the pdb file will be mutated. ie: "A:ALA15CYS"
            * **force_field** (*str*) - ("amber99sb-star-ildn-mut") Forcefield.
            * **resinfo** (*bool*) - (False) Print a 3 to 1 letter residue list.
            * **dna** (*bool*) - (False) Generate hybrid residue for the DNA nucleotides.
            * **rna** (*bool*) - (False) Generate hybrid residue for the RNA nucleotides.
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

    def __init__(self, input_structure_path: str, output_structure_path: str, input_b_structure_path: str = None,
                 properties: Mapping = None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            "in": {"input_structure_path": input_structure_path, "input_b_structure_path": input_b_structure_path},
            "out": {"output_structure_path": output_structure_path}
        }

        # Properties specific for BB
        self.force_field = properties.get('force_field', "amber99sb-star-ildn-mut")
        self.resinfo = properties.get('resinfo', False)
        self.mutation_list = properties.get('mutation_list', 'Val2Ala')
        self.dna = properties.get('dna', False)
        self.rna = properties.get('rna', False)

        # Properties common in all PMX BB
        self.gmxlib = properties.get('gmxlib', None)
        self.pmx_path = properties.get('pmx_path', 'pmx')

        # container Specific
        self.container_path = properties.get('container_path')
        self.container_image = properties.get('container_image', 'gromacs/gromacs:latest')
        self.container_volume_path = properties.get('container_volume_path', '/data')
        self.container_working_dir = properties.get('container_working_dir')
        self.container_user_id = properties.get('container_user_id')
        self.container_shell_path = properties.get('container_shell_path', '/bin/bash')

        # Properties common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')
        self.remove_tmp = properties.get('remove_tmp', True)
        self.restart = properties.get('restart', False)

        # Check the properties
        fu.check_properties(self, properties)

    @launchlogger
    def launch(self) -> int:
        print(self.mutation_list)
        """Launches the execution of the PMX mutate module."""
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

        # Generate mutations file
        try:
            # Check if self.mutation_list is a string
            self.mutation_list = self.mutation_list.replace(" ", "").split(',')
        except AttributeError:
            pass
        unique_dir = str(Path(fu.create_unique_dir()).resolve())
        self.io_dict["in"]["mutations"] = str(Path(unique_dir).joinpath('mutations.txt'))
        pattern = re.compile(r"(?P<chain>[a-zA-Z])*:*(?P<wt>[a-zA-Z]{3})(?P<resnum>\d+)(?P<mt>[a-zA-Z]{3})")
        with open(self.io_dict["in"]["mutations"], 'w') as mut_file:
            for mut in self.mutation_list:
                mut_dict = pattern.match(mut.strip()).groupdict()
                if mut_dict.get('chain'):
                    mut_file.write(mut_dict.get('chain')+' ')
                mut_file.write(mut_dict.get('resnum')+' ')
                mut_file.write(three_to_one(mut_dict.get('mt').upper()))
                mut_file.write('\n')

        container_io_dict = fu.copy_to_container(self.container_path, self.container_volume_path, self.io_dict)

        cmd = [self.pmx_path, 'mutate',
               '-f', container_io_dict["in"]["input_structure_path"],
               '-o', container_io_dict["out"]["output_structure_path"],
               '-ff', self.force_field,
               '--script', container_io_dict["in"]["mutations"]]

        if container_io_dict["in"].get("input_b_structure_path"):
            cmd.append('-fB')
            cmd.append(container_io_dict["in"]["input_b_structure_path"])
        if self.resinfo:
            cmd.append('-resinfo')
        if self.dna:
            cmd.append('-dna')
        if self.rna:
            cmd.append('-rna')
        new_env = None
        if self.gmxlib:
            new_env = os.environ.copy()
            new_env['GMXLIB'] = self.gmxlib

        cmd = fu.create_cmd_line(cmd, container_path=self.container_path,
                                 host_volume=container_io_dict.get("unique_dir"),
                                 container_volume=self.container_volume_path,
                                 container_working_dir=self.container_working_dir,
                                 container_user_uid=self.container_user_id,
                                 container_shell_path=self.container_shell_path,
                                 container_image=self.container_image,
                                 out_log=out_log, global_log=self.global_log)

        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log, new_env).launch()
        fu.copy_to_host(self.container_path, container_io_dict, self.io_dict)

        #tmp_files.append(container_io_dict.get("unique_dir"))
        tmp_files.append(unique_dir)
        if self.remove_tmp:
            fu.rm_file_list(tmp_files, out_log=out_log)

        return returncode


def main():
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
    Pmxmutate(input_structure_path=args.input_structure_path, output_structure_path=args.output_structure_path,
              input_b_structure_path=args.input_b_structure_path, properties=properties).launch()


if __name__ == '__main__':
    main()
