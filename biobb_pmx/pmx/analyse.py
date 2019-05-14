#!/usr/bin/env python3

"""Module containing the PMX analyse class and the command line interface."""
import argparse
import os
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper


class Analyse():
    """Wrapper class for the PMX analyse (https://github.com/dseeliger/pmx/wiki) module.

    Args:
        input_A_xvg_zip_path (str): Path the zip file containing the dgdl.xvg files of the A state.
        input_B_xvg_zip_path (str): Path the zip file containing the dgdl.xvg files of the B state.
        output_result_path (str): Path to the TXT results file.
        output_work_plot_path (str): Path to the PNG plot results file.
        properties (dic):
            | - **method** (*str*) - ("CGI BAR JARZ"): Choose one or more estimators to use from the available ones: CGI, BAR, JARZ.
            | - **temperature** (*float*) - (298.15): Temperature in Kelvin.
            | - **nboots** (*int*) - (0): Number of bootstrap samples.
            | - **nblocks** (*int*) - (1): Number of blocks to divide the data into for an estimate of the standard error.
            | - **integ_only** (*bool*) - (False): Whether to do integration only.
            | - **reverseB** (*bool*) - (False): Whether to reverse the work values for the backward (B->A) transformation.
            | - **skip** (*int*) - (1): Skip files.
            | - **slice** (*int*) - (All): Subset of trajectories to analyze.
            | - **index** (*bool*) - (All): Zero-based index of files to analyze.
            | - **prec** (*int*) - (2): The decimal precision of the screen/file output.
            | - **units** (*str*) - ("KJ"): The units of the output. Choose from "kJ", "kcal", "kT".
            | - **no_ks** (*bool*) - (False): Whether to do a Kolmogorov-Smirnov test to check whether the Gaussian assumption for CGI holds.
            | - **nbins** (*int*) - (10): Number of histograms bins for the plot.
            | - **dpi** (*int*) - (300): Resolution of the plot.
            | - **pmx_cli_path** (*str*) - ("cli.py"): Path to the PMX Python2.7 client.
    """

    def __init__(self, input_A_xvg_zip_path, input_B_xvg_zip_path, output_result_path, output_work_plot_path, properties=None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.input_A_xvg_zip_path = input_A_xvg_zip_path
        self.input_B_xvg_zip_path = input_B_xvg_zip_path
        self.output_result_path = output_result_path
        self.output_work_plot_path = output_work_plot_path

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

        # Properties common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')

        # Check the properties
        fu.check_properties(self, properties)

    def launch(self):
        """Launches the execution of the PMX gentop module."""
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step, can_write_console=self.can_write_console_log)


        list_A = fu.unzip_list(self.input_A_xvg_zip_path, fu.create_unique_dir(), out_log)
        list_B = fu.unzip_list(self.input_B_xvg_zip_path, fu.create_unique_dir(), out_log)

        cmd = [self.pmx_cli_path, 'analyse',
               '-fA', " ".join(list_A),
               '-fB', " ".join(list_B),
               '-o', self.output_result_path,
               '--work_plot', self.output_work_plot_path]

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

        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()
        return returncode

def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description="Run PMX mutate module", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")
    parser.add_argument('--system', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")
    parser.add_argument('--step', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_A_xvg_zip_path', required=True, help="Path the zip file containing the dgdl.xvg files of the A state")
    required_args.add_argument('--input_B_xvg_zip_path', required=True, help="Path the zip file containing the dgdl.xvg files of the B state")
    required_args.add_argument('--output_result_path', required=True, help="Path to the TXT results file")
    required_args.add_argument('--output_work_plot_path', required=True, help="Path to the PNG plot results file")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config, system=args.system).get_prop_dic()
    if args.step:
        properties = properties[args.step]

    #Specific call of each building block
    Analyse(input_A_xvg_zip_path=args.input_A_xvg_zip_path, input_B_xvg_zip_path=args.input_B_xvg_zip_path, output_result_path=args.output_result_path, output_work_plot_path=args.output_work_plot_path, properties=properties).launch()

if __name__ == '__main__':
    main()
