#!/usr/bin/env python3

"""Module containing the PMX mutate class and the command line interface."""
import os
import re
import argparse
from  Bio.PDB.Polypeptide import three_to_one
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper


class Mutate():
    """Wrapper class for the PMX mutate (https://github.com/dseeliger/pmx/wiki) module.

    Args:
        input_structure_path (str): Path to the input structure file.
        output_structure_path (str): Path to the output structure file.
        input_b_structure_path (str)[Optional]: Path to the mutated input structure file.
        properties (dic):
            | - **mutation_list** (*str*): ("Val2Ala") Mutation list in the format "Chain:WT_AA_ThreeLeterCode Resnum MUT_AA_ThreeLeterCode" (no spaces between the elements) separated by commas. If no chain is provided as chain code all the chains in the pdb file will be mutated. ie: "A:ALA15CYS"
            | - **force_field** (*str*) - ("amber99sb-star-ildn-mut"): Forcefield.
            | - **resinfo** (*bool*) - (False) Print a 3 to 1 letter residue list.
            | - **dna** (*bool*) - (False) Generate hybrid residue for the DNA nucleotides.
            | - **rna** (*bool*) - (False) Generate hybrid residue for the RNA nucleotides.
            | - **pmx_cli_path** (*str*) - ("cli.py") Path to the PMX Python2.7 client.
    """

    def __init__(self, input_structure_path, output_structure_path, input_b_structure_path=None, properties=None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.input_structure_path = input_structure_path
        self.output_structure_path = output_structure_path
        # Optional files
        self.input_b_structure_path = input_b_structure_path

        # Properties specific for BB
        self.force_field = properties.get('force_field', "amber99sb-star-ildn-mut.ff")
        self.resinfo = properties.get('resinfo', False)
        self.mutation_list = list(properties.get('mutation_list', 'Val2Ala').replace(" ","").split(','))
        self.dna = properties.get('dna', False)
        self.rna = properties.get('rna', False)

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
        """Launches the execution of the PMX mutate module."""
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step, can_write_console=self.can_write_console_log)

        #Check if executable is exists
        if not os.path.isfile(self.pmx_cli_path):
            raise FileNotFoundError('Executable %s not found. Check if it is installed in your system and correctly defined in the properties' % self.pmx_cli_path)


        #Generate mutations file
        mutations_file = os.path.join(fu.create_unique_dir(), 'mutations.txt')
        pattern = re.compile((r"(?P<chain>[a-zA-Z])*:*(?P<wt>[a-zA-Z]{3})(?P<resnum>\d+)(?P<mt>[a-zA-Z]{3})"))
        with open(mutations_file, 'w') as mut_file:
            for mut in self.mutation_list:
                mut_dict = pattern.match(mut).groupdict()
                if mut_dict.get('chain'):
                    mut_file.write(mut_dict.get('chain')+' ')
                mut_file.write(mut_dict.get('resnum')+' ')
                mut_file.write(three_to_one(mut_dict.get('mt').upper()))
                mut_file.write('\n')


        cmd = [self.pmx_cli_path, 'mutate',
               '-f', self.input_structure_path,
               '-o', self.output_structure_path,
               '-ff', self.force_field,
               '-script', mutations_file]

        if self.input_b_structure_path:
            cmd.append('-fB')
            cmd.append(self.input_b_structure_path)
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
        command = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log, new_env)
        return command.launch()

def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description="Run PMX mutate module", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")
    parser.add_argument('--system', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")
    parser.add_argument('--step', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_structure_path', required=True, help="Path to the input structure file")
    required_args.add_argument('--output_structure_path', required=True, help="Path to the output structure file")
    required_args.add_argument('--input_mutations_path', required=True, help="Path to the input text file containing the mutations")
    parser.add_argument('--input_b_structure_path', required=False, help="Path to the mutated input structure file")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config, system=args.system).get_prop_dic()
    if args.step:
        properties = properties[args.step]

    #Specific call of each building block
    Mutate(input_structure_path=args.input_structure_path, output_structure_path=args.output_structure_path, input_mutations_path=args.input_mutations_path, input_b_structure_path=args.input_b_structure_path, properties=properties).launch()

if __name__ == '__main__':
    main()
