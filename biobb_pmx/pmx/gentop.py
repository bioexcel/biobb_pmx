#!/usr/bin/env python3

"""Module containing the PMX gentop class and the command line interface."""
import argparse
import os
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper


class Gentop():
    """Wrapper class for the PMX gentop (https://github.com/dseeliger/pmx/wiki) module.

    Args:
        input_top_zip_path (str): Path the input GROMACS topology TOP and ITP files in zip format.
        output_top_zip_path (str): Path the output TOP topology in zip format.
        output_log_path (str): Path to the PMX log path.
        properties (dic):
            | - **force_field** (*str*) - ("amber99sb-star-ildn-mut"): Forcefield.
            | - **split** (*bool*) - (False) Print a 3 to 1 letter residue list.
            | - **scale_mass** (*bool*) - (False) Scale mass.
            | - **dna** (*bool*) - (False) Generate hybrid residue for the DNA nucleotides.
            | - **rna** (*bool*) - (False) Generate hybrid residue for the RNA nucleotides.
            | - **output_top_name** (*str*) - ("gentop.top") Name of the output top file.
            | - **keyword_list** (*str*) - ("Protein", "DNA") List of comma separated Keywords to match top and itp files.
            | - **pmx_cli_path** (*str*) - ("cli.py") Path to the PMX Python2.7 client.
    """

    def __init__(self, input_top_zip_path, output_top_zip_path, output_log_path, properties=None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.input_top_zip_path = input_top_zip_path
        self.output_top_zip_path = output_top_zip_path
        self.output_log_path = output_log_path

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

        # Check the properties
        fu.check_properties(self, properties)

    def launch(self):
        """Launches the execution of the PMX gentop module."""
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step, can_write_console=self.can_write_console_log)

        # Unzip topology to topology_out
        top_file = fu.unzip_top(zip_file=self.input_top_zip_path, out_log=out_log)
        top_dir = os.path.dirname(top_file)
        selected_list = set([os.path.basename(top_file)] + [top_itp_file for word in self.keyword_list for top_itp_file in os.listdir(top_dir) if word.lower() in top_itp_file.lower() ])

        for selected_file in selected_list:
            output_path = fu.create_name(prefix=self.prefix, step=self.step, name=selected_file)
            cmd = [self.pmx_cli_path, 'gentop',
                   '-o', output_path,
                   '-ff', self.force_field,
                   '-log', self.output_log_path]

            if selected_file.endswith(".itp"):
                cmd.append('-itp')
                cmd.append(os.path.join(top_dir, selected_file))
            if selected_file.endswith(".top"):
                output_top_file = output_path
                cmd.append('-p')
                cmd.append(os.path.join(top_dir, selected_file))
            if self.split:
                cmd.append('-split')
            if self.scale_mass:
                cmd.append('-scale_mass')
            if self.dna:
                cmd.append('-dna')
            if self.rna:
                cmd.append('-rna')
            new_env = None
            if self.gmxlib:
                new_env = os.environ.copy()
                new_env['GMXLIB'] = self.gmxlib

            returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log, new_env).launch()

        # zip topology
        fu.log('Compressing topology to: %s' % self.output_top_zip_path, out_log, self.global_log)
        fu.zip_top(zip_file=self.output_top_zip_path, top_file=output_top_file, out_log=out_log)
        tmp_files = [output_top_file]
        removed_files = [f for f in tmp_files if fu.rm(f)]
        fu.log('Removed: %s' % str(removed_files), out_log, self.global_log)

        return returncode

def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description="Run PMX mutate module", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")
    parser.add_argument('--system', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")
    parser.add_argument('--step', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_top_zip_path', required=True, help="Path to the input topology zip file")
    required_args.add_argument('--output_top_zip_path', required=True, help="Path to the output topology zip file")
    required_args.add_argument('--output_log_path', required=True, help="Path to the PMX log path")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config, system=args.system).get_prop_dic()
    if args.step:
        properties = properties[args.step]

    #Specific call of each building block
    Gentop(input_top_zip_path=args.input_top_zip_path, output_top_zip_path=args.output_top_zip_path, output_log_path=args.output_log_path, properties=properties).launch()

if __name__ == '__main__':
    main()
