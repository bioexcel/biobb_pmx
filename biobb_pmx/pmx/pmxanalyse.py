#!/usr/bin/env python3

"""Module containing the PMX analyse class and the command line interface."""
import argparse
from pathlib import Path
import shutil
from typing import Mapping
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper


class Pmxanalyse:
    """
    | biobb_pmx Pmxanalyse
    | Wrapper class for the `PMX analyse <https://github.com/deGrootLab/pmx>`_ module.
   
    Args:
        input_a_xvg_zip_path (str): Path the zip file containing the dgdl.xvg files of the A state. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/xvg_A.zip>`_. Accepted formats: zip (edam:format_3987).
        input_b_xvg_zip_path (str): Path the zip file containing the dgdl.xvg files of the B state. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/xvg_B.zip>`_. Accepted formats: zip (edam:format_3987).
        output_result_path (str): Path to the TXT results file. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_result.txt>`_. Accepted formats: txt (edam:format_2330).
        output_work_plot_path (str): Path to the PNG plot results file. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_plot.png>`_. Accepted formats: png (edam:format_3603).
        properties (dic):
            * **method** (*str*) - ("CGI BAR JARZ") Choose one or more estimators to use. Values: CGI (Crooks Gaussian Intersection), BAR (Bennet Acceptance Ratio), JARZ (Jarzynski's estimator).
            * **temperature** (*float*) - (298.15) [0~1000|0.05] Temperature in Kelvin.
            * **nboots** (*int*) - (0) [0~1000|1] Number of bootstrap samples to use for the bootstrap estimate of the standard errors.
            * **nblocks** (*int*) - (1) [0~1000|1] Number of blocks to divide the data into for an estimate of the standard error.
            * **integ_only** (*bool*) - (False) Whether to do integration only.
            * **reverseB** (*bool*) - (False) Whether to reverse the work values for the backward (B->A) transformation.
            * **skip** (*int*) - (1) [0~1000|1] Skip files.
            * **slice** (*str*) - (None) Subset of trajectories to analyze. Provide list slice, e.g. "10 50" will result in selecting dhdl_files[10:50].
            * **rand** (*int*) - (None) [0~1000|1] Take a random subset of trajectories. Default is None (do not take random subset).
            * **index** (*str*) - (None) Zero-based index of files to analyze (e.g. "0 10 20 50 60"). It keeps the dhdl.xvg files according to their position in the list, sorted according to the filenames.
            * **prec** (*int*) - (2) [0~100|1] The decimal precision of the screen/file output.
            * **units** (*str*) - ("kJ") The units of the output. Values: kJ (Kilojoules), kcal (Kilocalories), kT (the product of the Boltzmann constant k and the temperature).
            * **no_ks** (*bool*) - (False) Whether to do a Kolmogorov-Smirnov test to check whether the Gaussian assumption for CGI holds.
            * **nbins** (*int*) - (20) [0~1000|1] Number of histograms bins for the plot.
            * **dpi** (*int*) - (300) [72~2048|1] Resolution of the plot.
            * **pmx_path** (*str*) - ("pmx") Path to the PMX command line interface.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **container_path** (*str*) - (None)  Path to the binary executable of your container.
            * **container_image** (*str*) - ("gromacs/gromacs:latest") Container Image identifier.
            * **container_volume_path** (*str*) - ("/data") Path to an internal directory in the container.
            * **container_working_dir** (*str*) - (None) Path to the internal CWD in the container.
            * **container_user_id** (*str*) - (None) User number id to be mapped inside the container.
            * **container_shell_path** (*str*) - ("/bin/bash") Path to the binary executable of the container shell.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_pmx.pmx.pmxanalyse import pmxanalyse
            prop = { 
                'method': 'CGI BAR JARZ', 
                'temperature': 298.15, 
                'dpi': 600 
            }
            pmxanalyse(input_a_xvg_zip_path='/path/to/myAStateFiles.zip', 
                       input_b_xvg_zip_path='/path/to/myBStateFiles.zip',
                       output_result_path='/path/to/newResults.txt',
                       output_work_plot_path='/path/to/newResults.png',
                       properties=prop)

    Info:
        * wrapped_software:
            * name: PMX analyse
            * version: >=1.0.1
            * license: GNU
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_a_xvg_zip_path: str, input_b_xvg_zip_path: str, output_result_path: str, output_work_plot_path: str, 
                properties: Mapping = None, **kwargs) -> None:
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
        self.method = properties.get('method', "CGI BAR JARZ")
        self.temperature = properties.get('temperature', 298.15)
        self.nboots = properties.get('nboots', 0)
        self.nblocks = properties.get('nblocks', 1)
        self.integ_only = properties.get('integ_only', False)
        self.reverseB = properties.get('reverseB', False)
        self.skip = properties.get('skip', 1)
        self.slice = properties.get('slice', None)
        self.rand = properties.get('rand', None)
        self.index = properties.get('index', None)
        self.prec = properties.get('prec', 2)
        self.units = properties.get('units', "kJ")
        self.no_ks = properties.get('no_ks', False)
        self.nbins = properties.get('nbins', 20)
        self.dpi = properties.get('dpi', 300)

        # Properties common in all PMX BB
        self.pmx_path = properties.get('pmx_path', 'pmx')

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
    def launch(self) -> int:
        """Execute the :class:`Pmxanalyse <pmx.pmxanalyse.Pmxanalyse>` pmx.pmxanalyse.Pmxanalyse object."""
        tmp_files = []

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # Check if executable is exists
        if not self.container_path:
            if not Path(self.pmx_path).is_file():
                if not shutil.which(self.pmx_path):
                    raise FileNotFoundError(
                        'Executable %s not found. Check if it is installed in your system and correctly defined in the properties' % self.pmx_path)

        # Restart if needed
        if self.restart:
            if fu.check_complete_files(self.io_dict["out"].values()):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        list_a_dir = fu.create_unique_dir()
        list_b_dir = fu.create_unique_dir()
        list_a = list(filter(lambda f: Path(f).exists() and Path(f).stat().st_size > 10, fu.unzip_list(self.input_a_xvg_zip_path, list_a_dir, out_log)))
        list_b = list(filter(lambda f: Path(f).exists() and Path(f).stat().st_size > 10, fu.unzip_list(self.input_b_xvg_zip_path, list_b_dir, out_log)))
        string_a = " ".join(list_a)
        string_b = " ".join(list_b)

        container_io_dict = fu.copy_to_container(self.container_path, self.container_volume_path, self.io_dict)

        if self.container_path:
            shutil.copytree(list_a_dir, Path(container_io_dict.get("unique_dir")).joinpath(Path(list_a_dir).name))
            shutil.copytree(list_b_dir, Path(container_io_dict.get("unique_dir")).joinpath(Path(list_b_dir).name))
            container_volume = " " + self.container_volume_path + "/"
            string_a = self.container_volume_path + "/" + container_volume.join(list_a)
            string_b = self.container_volume_path + "/" + container_volume.join(list_b)

        cmd = [self.pmx_path, 'analyse',
               '-fA', string_a,
               '-fB', string_b,
               '-o', container_io_dict["out"]["output_result_path"],
               '-w', container_io_dict["out"]["output_work_plot_path"]]

        if self.method:
            cmd.append('-m')
            cmd.append(self.method)
        if self.temperature:
            cmd.append('-t')
            cmd.append(str(self.temperature))
        if self.nboots:
            cmd.append('-b')
            cmd.append(str(self.nboots))
        if self.nblocks:
            cmd.append('-n')
            cmd.append(str(self.nblocks))
        if self.integ_only:
            cmd.append('--integ_only')
        if self.reverseB:
            cmd.append('--reverseB')
        if self.skip:
            cmd.append('--skip')
            cmd.append(str(self.skip))
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
            cmd.append(str(self.prec))
        if self.units:
            cmd.append('--units')
            cmd.append(self.units)
        if self.no_ks:
            cmd.append('--no_ks')
        if self.nbins:
            cmd.append('--nbins')
            cmd.append(str(self.nbins))
        if self.dpi:
            cmd.append('--dpi')
            cmd.append(str(self.dpi))

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


def pmxanalyse(input_a_xvg_zip_path: str, input_b_xvg_zip_path: str,
               output_result_path: str, output_work_plot_path: str,
               properties: dict = None, **kwargs) -> int:
    """Execute the :class:`Pmxanalyse <pmx.pmxanalyse.Pmxanalyse>` class and
    execute the :meth:`launch() <pmx.pmxanalyse.Pmxanalyse.launch> method."""

    return Pmxanalyse(input_a_xvg_zip_path=input_a_xvg_zip_path, 
                      input_b_xvg_zip_path=input_b_xvg_zip_path,
                      output_result_path=output_result_path,
                      output_work_plot_path=output_work_plot_path,
                      properties=properties).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Wrapper class for the PMX analyse module.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False,
                        help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_a_xvg_zip_path', required=True,
                               help="Path the zip file containing the dgdl.xvg files of the A state. Accepted formats: zip.")
    required_args.add_argument('--input_b_xvg_zip_path', required=True,
                               help="Path the zip file containing the dgdl.xvg files of the B state. Accepted formats: zip.")
    required_args.add_argument('--output_result_path', required=True, help="Path to the TXT results file. Accepted formats: txt.")
    required_args.add_argument('--output_work_plot_path', required=True, help="Path to the PNG plot results file. Accepted formats: png.")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    pmxanalyse(input_a_xvg_zip_path=args.input_a_xvg_zip_path,
               input_b_xvg_zip_path=args.input_b_xvg_zip_path,
               output_result_path=args.output_result_path,
               output_work_plot_path=args.output_work_plot_path,
               properties=properties)


if __name__ == '__main__':
    main()
