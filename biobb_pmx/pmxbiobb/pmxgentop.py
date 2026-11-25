#!/usr/bin/env python3

"""Module containing the PMX gentop class and the command line interface."""

import os
import shutil
import sys
from pathlib import Path
from typing import Optional

from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools import file_utils as fu


class Pmxgentop(BiobbObject):
    """
    | biobb_pmx Pmxgentop
    | Wrapper class for the `PMX gentop <https://github.com/deGrootLab/pmx>`_ module.
    | Generate a topology file for a morphing simulation.

    Args:
        input_top_zip_path (str): Path the input GROMACS topology TOP and ITP files in zip format. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/blob/master/biobb_pmx/test/data/pmx/mut_gmx.top.zip>`_. Accepted formats: zip (edam:format_3987).
        output_top_zip_path (str): Path the output TOP topology in zip format. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_output_topology.zip>`_. Accepted formats: zip (edam:format_3987).
        properties (dic):
            * **force_field** (*str*) - ("amber99sb-star-ildn-mut") Force field to use. If **input_top_zip_path** is a top file, it's not necessary to specify the forcefield, as it will be determined automatically. If **input_top_zip_path** is an itp file, then it's needed.
            * **split** (*bool*) - (False) Write separate topologies for the vdW and charge transformations.
            * **scale_mass** (*bool*) - (False) Scale the masses of morphing atoms so that dummies have a mass of 1.
            * **gmx_lib** (*str*) - (None) Path to the GMXLIB folder in your computer. If not set, the mutff folder of the pmx package of the conda environment.
            * **binary_path** (*str*) - ("pmx") Path to the PMX command line interface.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.
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

    def __init__(
        self,
        input_top_zip_path: str,
        output_top_zip_path: str,
        properties: Optional[dict] = None,
        **kwargs,
    ) -> None:
        super().__init__(**locals())

        # Should not be copied inside container
        self.input_top_zip_path = self.io_dict["in"].pop("input_top_zip_path")

        # Properties common in all PMX BB
        if not self.gmx_lib and os.environ.get("CONDA_PREFIX", ""):
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
            self.gmx_lib = str(
                Path(os.environ.get("CONDA_PREFIX", "")).joinpath(
                    f"lib/python{python_version}/site-packages/pmx/data/mutff/"
                )
            )
            if self.container_path:
                self.gmx_lib = str(
                    Path("/usr/local/").joinpath(
                        "lib/python3.8/site-packages/pmx/data/mutff/"
                    )
                )

    def run(self) -> None:
        """Execute the :class:`Pmxgentop <pmx.pmxgentop.Pmxgentop>` pmx.pmxgentop.Pmxgentop object."""

        if self.container_path:
            working_dir = self.container_volume_path if self.container_volume_path else "/data"
        else:
            working_dir = self.stage_io_dict.get("unique_dir", "")

        # Check if executable exists
        if not self.container_path:
            if not Path(self.binary_path).is_file():
                if not shutil.which(self.binary_path):
                    raise FileNotFoundError(
                        "Executable %s not found. Check if it is installed in your system and correctly defined in the properties"
                        % self.binary_path
                    )

        # Unzip topology to topology_out
        top_file = str(
            Path(
                fu.unzip_top(zip_file=self.input_top_zip_path, out_log=self.out_log)
            ).resolve()
        )
        top_dir = str(Path(top_file).parent)

        # Copy extra files to sandbox: topology folder
        top_dir_in_sandbox = Path(self.stage_io_dict.get("unique_dir", "")).joinpath(
            Path(top_dir).name
        )
        shutil.copytree(top_dir, str(top_dir_in_sandbox))
        top_file = str(Path(Path(top_dir).name).joinpath(Path(top_file).name))

        output_file_name = fu.create_name(
            prefix=self.prefix, step=self.step, name=str(Path(top_file).name)
        )
        unique_dir_output_file = str(
            Path(self.stage_io_dict.get("unique_dir", "")).joinpath(output_file_name)
        )
        fu.log(f"unique_dir_output_file: {unique_dir_output_file}", self.out_log)

        self.cmd = [
            "cd",
            working_dir,
            ";",
            self.binary_path,
            "gentop",
            "-o",
            str(Path(output_file_name)),
            "-ff",
            self.force_field,
            "-p",
            top_file,
        ]

        if self.split:
            self.cmd.append("--split")
        if self.scale_mass:
            self.cmd.append("--scale_mass")

        if self.gmx_lib:
            self.env_vars_dict["GMXLIB"] = self.gmx_lib

        # Run Biobb block
        self.run_biobb()

        self.tmp_files.extend([top_dir])

        # Remove the sandbox paths from the output topology, add the itp files of the input topology that pmx did not change and zip it.
        # Remove paths from top file
        with open(Path(unique_dir_output_file)) as top_fh:
            top_lines = top_fh.readlines()
        with open(Path(unique_dir_output_file), "w") as top_fh:
            for line in top_lines:
                top_fh.write(
                    line.replace(str(Path(unique_dir_output_file).parent) + "/", "")
                )
        # Copy the not modified itp files
        for orig_itp_file in Path(top_dir).iterdir():
            fu.log(
                f"Check if {str(Path(unique_dir_output_file).parent.joinpath(Path(orig_itp_file).name))} exists",
                self.out_log,
                self.global_log,
            )
            if (
                not Path(unique_dir_output_file)
                .parent.joinpath(Path(orig_itp_file).name)
                .exists()
            ):
                shutil.copy(orig_itp_file, Path(unique_dir_output_file).parent)
                fu.log(
                    f"Copying {str(orig_itp_file)} to: {str(Path(unique_dir_output_file).parent)}",
                    self.out_log,
                    self.global_log,
                )

        # zip topology
        fu.log(
            "Compressing topology to: %s" % self.io_dict["out"]["output_top_zip_path"],
            self.out_log,
            self.global_log,
        )
        fu.zip_top(
            zip_file=self.sandbox_file("output_top_zip_path"),
            top_file=str(Path(unique_dir_output_file)),
            out_log=self.out_log,
            remove_original_files=self.remove_tmp
        )


def pmxgentop(
    input_top_zip_path: str,
    output_top_zip_path: str,
    properties: Optional[dict] = None,
    **kwargs,
) -> int:
    """Create the :class:`Pmxgentop <pmx.pmxgentop.Pmxgentop>` class and
    execute the :meth:`launch() <pmx.pmxgentop.Pmxgentop.launch> method."""
    return Pmxgentop(**dict(locals())).launch()


pmxgentop.__doc__ = Pmxgentop.__doc__
main = Pmxgentop.get_main(pmxgentop, "Wrapper class for the PMX gentop module")

if __name__ == "__main__":
    main()
