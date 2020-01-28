#!/usr/bin/env python3

"""Module containing the PMX gentop class and the command line interface."""
import argparse
import os
import shutil
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper


class Gentop:
    """Wrapper class for the `PMX gentop <https://github.com/deGrootLab/pmx>`_ module.

    Args:
        input_top_zip_path (str): Path the input GROMACS topology TOP and ITP files in zip format. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/topology.zip>`_. Accepted formats: zip.
        output_top_zip_path (str): Path the output TOP topology in zip format. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_output_topology.zip>`_. Accepted formats: zip.
        properties (dic):
            * **force_field** (*str*) - ("amber99sb-star-ildn-mut") Forcefield.
            * **split** (*bool*) - (False) Print a 3 to 1 letter residue list.
            * **scale_mass** (*bool*) - (False) Scale mass.
            * **dna** (*bool*) - (False) Generate hybrid residue for the DNA nucleotides.
            * **rna** (*bool*) - (False) Generate hybrid residue for the RNA nucleotides.
            * **output_top_name** (*str*) - ("gentop.top") Name of the output top file.
            * **keyword_list** (*str*) - (["Protein", "DNA"]) List of comma separated Keywords to match top and itp files.
            * **pmx_cli_path** (*str*) - ("cli.py") Path to the PMX Python2.7 client.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **container_path** (*string*) - (None)  Path to the binary executable of your container.
            * **container_image** (*string*) - ("gromacs/gromacs:latest") Container Image identifier.
            * **container_volume_path** (*string*) - ("/inout") Path to an internal directory in the container.
            * **container_working_dir** (*string*) - (None) Path to the internal CWD in the container.
            * **container_user_id** (*string*) - (None) User number id to be mapped inside the container.
            * **container_shell_path** (*string*) - ("/bin/bash") Path to the binary executable of the container shell.
    """

    def __init__(self, input_top_zip_path, output_top_zip_path, properties=None, **kwargs):
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
        self.keyword_list = list(properties.get('keyword_list', []))
        self.keyword_list = list(set(self.keyword_list + ["Protein", "DNA"]))
        # Properties common in all PMX BB
        self.gmxlib = properties.get('gmxlib', None)
        self.pmx_cli_path = properties.get('pmx_cli_path', 'cli.py')

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
    def launch(self):
        """Launches the execution of the PMX gentop module."""
        tmp_files = []

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # Check if executable is exists
        if not self.container_path:
            if not os.path.isfile(self.pmx_cli_path):
                if not shutil.which(self.pmx_cli_path):
                    raise FileNotFoundError('Executable %s not found. Check if it is installed in your system and correctly defined in the properties' % self.pmx_cli_path)

        # Restart if needed
        if self.restart:
            if fu.check_complete_files(self.io_dict["out"].values()):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log,
                       self.global_log)
                return 0

        # Unzip topology to topology_out
        top_file = fu.unzip_top(zip_file=self.input_top_zip_path, out_log=out_log)
        top_dir = os.path.dirname(top_file)
        # List of top and ipt files to apply pmx_gentop
        selected_list = set([os.path.basename(top_file)] + [top_itp_file for word in self.keyword_list for top_itp_file in os.listdir(top_dir) if word.lower() in top_itp_file.lower()])
        fu.log('Gentop will be executed on this list of files: ', out_log, self.global_log)
        fu.log(str(selected_list), out_log, self.global_log)
        tmp_files.append(top_dir)

        #  If using containers create unique dir and copy nothing there
        container_io_dict = fu.copy_to_container(self.container_path, self.container_volume_path, self.io_dict)

        if self.container_path:
            fu.log(f"Unique dir: {container_io_dict['unique_dir']}", out_log)
            fu.log(f"{container_io_dict['unique_dir']} files: {os.listdir(container_io_dict['unique_dir'])}", out_log)
            # Copy all files of the unzipped topology to unique dir
            fu.log(f"Copy all files of the unzipped original topology to unique dir:", out_log)
            for d_file in os.listdir(top_dir):
                shutil.copy2(os.path.join(top_dir, d_file), container_io_dict.get("unique_dir"))
                fu.log(f"    Copy: {os.path.join(top_dir, d_file)} to: {container_io_dict.get('unique_dir')}", out_log)

        # Loop through all selected files applying pmx_gentop
        fu.log(f"List of files where gentop will be applied: {selected_list}", out_log)

        for selected_file in selected_list:
            fu.log(f"Selected file: {selected_file}", out_log)
            unique_dir_output_file = fu.create_name(path=container_io_dict.get("unique_dir"), step=self.step, name=selected_file)
            fu.log(f"unique_dir_output_file: {unique_dir_output_file}", out_log)

            if self.container_path:
                fu.log("Change references for container:", out_log)
                unique_dir_output_file = os.path.join(self.container_volume_path, os.path.basename(unique_dir_output_file))
                fu.log(f"    unique_dir_output_file: {unique_dir_output_file}", out_log)

            cmd = [self.pmx_cli_path, 'gentop',
                   '-o', unique_dir_output_file,
                   '-ff', self.force_field]

            # Adding itp file command line
            if selected_file.endswith(".itp"):
                cmd.append('-itp')
                itp_file = os.path.join(top_dir, selected_file)
                if self.container_path:
                    itp_file = os.path.join(self.container_volume_path, selected_file)
                cmd.append(itp_file)

            # Adding top file to command line
            if selected_file.endswith(".top"):
                cmd.append('-p')
                topology_file = os.path.join(top_dir, selected_file)
                orig_topology_file = topology_file
                if self.container_path:
                    topology_file = os.path.join(self.container_volume_path, selected_file)
                cmd.append(topology_file)

            if self.split:
                cmd.append('-split')
            if self.scale_mass:
                cmd.append('-scale_mass')
            if self.dna:
                cmd.append('-dna')
            if self.rna:
                cmd.append('-rna')

            cmd = fu.create_cmd_line(cmd, container_path=self.container_path,
                                     host_volume=container_io_dict.get("unique_dir"),
                                     container_volume=self.container_volume_path,
                                     container_working_dir=self.container_working_dir,
                                     container_user_uid=self.container_user_id,
                                     container_shell_path=self.container_shell_path,
                                     container_image=self.container_image,
                                     out_log=out_log, global_log=self.global_log)

            returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

            # Replace original file for the modified one
            if self.container_path:
                shutil.copy2(os.path.join(container_io_dict.get("unique_dir"), os.path.basename(unique_dir_output_file)), os.path.join(top_dir, selected_file))
                fu.log(f"Replace (copy): {os.path.join(container_io_dict.get('unique_dir'), os.path.basename(unique_dir_output_file))} to: {os.path.join(top_dir, selected_file)}", out_log)

        fu.log("End of looping throug files", out_log)

        # zip topology
        fu.log('Compressing topology to: %s' % self.io_dict["out"]["output_top_zip_path"], out_log, self.global_log)
        fu.zip_top(zip_file=self.io_dict["out"]["output_top_zip_path"], top_file=orig_topology_file, out_log=out_log)

        tmp_files.append(top_dir)
        tmp_files.append(container_io_dict.get("unique_dir"))
        if self.remove_tmp:
            fu.rm_file_list(tmp_files, out_log=out_log)

        return returncode


def main():
    parser = argparse.ArgumentParser(description="Run PMX mutate module", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")
    parser.add_argument('--system', required=False, help="Common name for workflow properties set")
    parser.add_argument('--step', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/configuration.html")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_top_zip_path', required=True, help="Path to the input topology zip file")
    required_args.add_argument('--output_top_zip_path', required=True, help="Path to the output topology zip file")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config, system=args.system).get_prop_dic()
    if args.step:
        properties = properties[args.step]

    # Specific call of each building block
    Gentop(input_top_zip_path=args.input_top_zip_path, output_top_zip_path=args.output_top_zip_path, properties=properties).launch()


if __name__ == '__main__':
    main()
