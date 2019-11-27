#!/usr/bin/env python3

"""Module containing the PMX analyse class and the command line interface."""
import argparse
import os
import shutil
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper


class Analyse:
    """Wrapper class for the PMX analyse (https://github.com/dseeliger/pmx/wiki) module.

    Args:
        input_A_xvg_zip_path (str): Path the zip file containing the dgdl.xvg files of the A state.
        input_B_xvg_zip_path (str): Path the zip file containing the dgdl.xvg files of the B state.
        output_result_path (str): Path to the TXT results file.
        output_work_plot_path (str): Path to the PNG plot results file.
        properties (dic):
            * **method** (*str*) - ("CGI BAR JARZ"): Choose one or more estimators to use from the available ones: CGI, BAR, JARZ.
            * **temperature** (*float*) - (298.15): Temperature in Kelvin.
            * **nboots** (*int*) - (0): Number of bootstrap samples.
            * **nblocks** (*int*) - (1): Number of blocks to divide the data into for an estimate of the standard error.
            * **integ_only** (*bool*) - (False): Whether to do integration only.
            * **reverseB** (*bool*) - (False): Whether to reverse the work values for the backward (B->A) transformation.
            * **skip** (*int*) - (1): Skip files.
            * **slice** (*int*) - (All): Subset of trajectories to analyze.
            * **index** (*bool*) - (All): Zero-based index of files to analyze.
            * **prec** (*int*) - (2): The decimal precision of the screen/file output.
            * **units** (*str*) - ("KJ"): The units of the output. Choose from "kJ", "kcal", "kT".
            * **no_ks** (*bool*) - (False): Whether to do a Kolmogorov-Smirnov test to check whether the Gaussian assumption for CGI holds.
            * **nbins** (*int*) - (10): Number of histograms bins for the plot.
            * **dpi** (*int*) - (300): Resolution of the plot.
            * **pmx_cli_path** (*str*) - ("cli.py"): Path to the PMX Python2.7 client.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **container_path** (*string*) - (None)  Path to the binary executable of your container.
            * **container_image** (*string*) - ("gromacs/gromacs:latest") Container Image identifier.
            * **container_volume_path** (*string*) - ("/data") Path to an internal directory in the container.
            * **container_working_dir** (*string*) - (None) Path to the internal CWD in the container.
            * **container_user_id** (*string*) - (None) User number id to be mapped inside the container.
            * **container_shell_path** (*string*) - ("/bin/bash") Path to the binary executable of the container shell.
    """

    def __init__(self, input_a_xvg_zip_path, input_b_xvg_zip_path, output_result_path, output_work_plot_path,
                 properties=None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            "in": {},
            "out": {"output_result_path": output_result_path, "output_work_plot_path": output_work_plot_path}
        }
        # Should not be copied inside container
        self.input_a_xvg_zip_path = input_a_xvg_zip_path
        self.input_b_xvg_zip_path = input_b_xvg_zip_path

        # Properties specific for BB
        self.method = properties.get('method', None)
        self.temperature = properties.get('temperature', None)
        self.nboots = properties.get('nboots', None)
        self.nblocks = properties.get('nblocks', None)
        self.integ_only = properties.get('integ_only', None)
        self.reverseB = properties.get('reverseB', None)
        self.skip = properties.get('skip', None)
        self.slice = properties.get('slice', None)
        self.rand = properties.get('rand', None)
        self.index = properties.get('index', None)
        self.prec = properties.get('prec', None)
        self.units = properties.get('units', None)
        self.no_ks = properties.get('no_ks', None)
        self.nbins = properties.get('nbins', None)
        self.dpi = properties.get('dpi', None)

        # Properties common in all PMX BB
        self.pmx_cli_path = properties.get('pmx_cli_path', 'cli.py')

        # container Specific
        self.container_path = properties.get('container_path')
        self.container_image = properties.get('container_image', 'gromacs/gromacs:latest')
        self.container_volume_path = properties.get('container_volume_path', '/inout')
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
                    raise FileNotFoundError(
                        'Executable %s not found. Check if it is installed in your system and correctly defined in the properties' % self.pmx_cli_path)

        # Restart if needed
        if self.restart:
            if fu.check_complete_files(self.io_dict["out"].values()):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        list_a_dir = fu.create_unique_dir()
        list_b_dir = fu.create_unique_dir()
        list_a = fu.unzip_list(self.input_a_xvg_zip_path, list_a_dir, out_log)
        list_b = fu.unzip_list(self.input_b_xvg_zip_path, list_b_dir, out_log)
        string_a = " ".join(list_a)
        string_b = " ".join(list_b)

        container_io_dict = fu.copy_to_container(self.container_path, self.container_volume_path, self.io_dict)

        if self.container_path:
            shutil.copytree(list_a_dir, os.path.join(container_io_dict.get("unique_dir"), os.path.basename(list_a_dir)))
            shutil.copytree(list_b_dir, os.path.join(container_io_dict.get("unique_dir"), os.path.basename(list_b_dir)))
            container_volume = " " + self.container_volume_path + "/"
            string_a = self.container_volume_path + "/" + container_volume.join(list_a)
            string_b = self.container_volume_path + "/" + container_volume.join(list_b)

        cmd = [self.pmx_cli_path, 'analyse',
               '-fA', string_a,
               '-fB', string_b,
               '-o', container_io_dict["out"]["output_result_path"],
               '--work_plot', container_io_dict["out"]["output_work_plot_path"]]

        if self.method:
            cmd.append('-m')
            cmd.append(self.method)
        if self.temperature:
            cmd.append('-t')
            cmd.append(self.temperature)
        if self.nboots:
            cmd.append('-b')
            cmd.append(self.nboots)
        if self.nblocks:
            cmd.append('-n')
            cmd.append(self.nblocks)
        if self.integ_only:
            cmd.append('--integ_only')
        if self.reverseB:
            cmd.append('--reverseB')
        if self.skip:
            cmd.append('--skip')
            cmd.append(self.skip)
        if self.slice:
            cmd.append('--slice')
            cmd.append(self.slice)
        if self.rand:
            cmd.append('--rand')
        if self.index:
            cmd.append('--index')
            cmd.append(self.index)
        if self.prec:
            cmd.append('--prec')
            cmd.append(self.prec)
        if self.units:
            cmd.append('--units')
            cmd.append(self.units)
        if self.no_ks:
            cmd.append('--no_ks')
        if self.nbins:
            cmd.append('--nbins')
            cmd.append(self.nbins)
        if self.dpi:
            cmd.append('--dpi')
            cmd.append(self.dpi)

        cmd = fu.create_cmd_line(cmd, container_path=self.container_path,
                                 host_volume=container_io_dict.get("unique_dir"),
                                 container_volume=self.container_volume_path,
                                 container_working_dir=self.container_working_dir,
                                 container_user_uid=self.container_user_id,
                                 container_shell_path=self.container_shell_path,
                                 container_image=self.container_image,
                                 out_log=out_log, global_log=self.global_log)
        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()
        fu.copy_to_host(self.container_path, container_io_dict, self.io_dict)

        tmp_files.append(container_io_dict.get("unique_dir"))
        tmp_files.append(list_a_dir)
        tmp_files.append(list_b_dir)
        if self.remove_tmp:
            fu.rm_file_list(tmp_files, out_log=out_log)

        return returncode


def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description="Run PMX mutate module", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")
    parser.add_argument('--system', required=False, help="Common name for workflow properties set")
    parser.add_argument('--step', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/configuration.html")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_A_xvg_zip_path', required=True,
                               help="Path the zip file containing the dgdl.xvg files of the A state")
    required_args.add_argument('--input_B_xvg_zip_path', required=True,
                               help="Path the zip file containing the dgdl.xvg files of the B state")
    required_args.add_argument('--output_result_path', required=True, help="Path to the TXT results file")
    required_args.add_argument('--output_work_plot_path', required=True, help="Path to the PNG plot results file")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config, system=args.system).get_prop_dic()
    if args.step:
        properties = properties[args.step]

    # Specific call of each building block
    Analyse(input_A_xvg_zip_path=args.input_A_xvg_zip_path, input_B_xvg_zip_path=args.input_B_xvg_zip_path,
            output_result_path=args.output_result_path, output_work_plot_path=args.output_work_plot_path,
            properties=properties).launch()


if __name__ == '__main__':
    main()
