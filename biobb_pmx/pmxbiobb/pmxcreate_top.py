#!/usr/bin/env python3

"""Module containing the PMX create_top class and the command line interface."""

import os
import shutil
import sys
from pathlib import Path, PurePath
from typing import Optional

from biobb_common.generic.biobb_object import BiobbObject, launcher
from biobb_common.tools import file_utils as fu


class Pmxcreate_top(BiobbObject):
    """
    | biobb_pmx Pmxcreate_top
    | Wrapper class for the `PMX create_top <https://github.com/deGrootLab/pmx>`_ module.
    | Create a complete ligand topology file from two input topology files.

    Args:
        input_topology1_path (str): Path to the input topology file 1. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/topo1.itp>`_. Accepted formats: itp (edam:format_3883).
        input_topology2_path (str): Path to the input topology file 2. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/topo2.itp>`_. Accepted formats: itp (edam:format_3883).
        output_topology_path (str): Path to the complete ligand topology file. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_hybridTopo.zip>`_. Accepted formats: zip (edam:format_3987).
        properties (dic):
            * **force_field** (*str*) - ("amber99sb-star-ildn-mut.ff") Force-field to be included in the generated topology.
            * **water** (*str*) - ("tip3p") Water model to be included in the generated topology.
            * **system_name** (*str*) - ("Pmx topology") System name to be included in the generated topology.
            * **mols** (*list*) - ([['Protein',1],['Ligand',1]]) Molecules to be included in the generated topology.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

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

    def __init__(
        self,
        input_topology1_path: str,
        input_topology2_path: str,
        output_topology_path: str,
        properties: Optional[dict] = None,
        **kwargs,
    ) -> None:
        super().__init__(**locals())

        # Properties common in all PMX BB
        self.gmx_lib = self.properties.get("gmx_lib", None)
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
                        "lib/python3.7/site-packages/pmx/data/mutff/"
                    )
                )

    def stage_files(self) -> None:
        """The block does not use the sandbox: there are no files to stage."""

    def run(self) -> None:
        """Execute the :class:`Pmxcreate_top <pmx.pmxcreate_top.Pmxcreate_top>` pmx.pmxcreate_top.Pmxcreate_top object."""
        fu.log("Running create_top from pmx package...\n", self.out_log)

        # Creating temporary folder
        tmp_folder = self.create_tmp_dir(log=True)

        itp = os.path.basename(
            os.path.normpath(self.io_dict["in"]["input_topology1_path"])
        )
        fu.log("Creating %s itp file in temporary folder" % itp, self.out_log)
        itp_local = str(PurePath(tmp_folder).joinpath(itp))
        shutil.copyfile(self.io_dict["in"]["input_topology1_path"], itp_local)

        itp2 = os.path.basename(
            os.path.normpath(self.io_dict["in"]["input_topology2_path"])
        )
        fu.log("Creating %s itp file in temporary folder" % itp2, self.out_log)
        itp2_local = str(PurePath(tmp_folder).joinpath(itp2))
        shutil.copyfile(self.io_dict["in"]["input_topology2_path"], itp2_local)

        top_local = str(PurePath(tmp_folder).joinpath("topology.top"))

        # _create_top function, taken from the pmx AZ tutorial:
        # https://github.com/deGrootLab/pmx/blob/develop/tutorials/AZtutorial.py
        fp = open(top_local, "w")
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
        fp.write("[ system ]\n")
        fp.write("{0}\n\n".format(self.system_name))
        # molecules
        fp.write("[ molecules ]\n")
        for mol in self.mols:
            fp.write("%s %s\n" % (mol[0], mol[1]))
        fp.close()

        # zip topology
        current_cwd = os.getcwd()
        top_final = str(
            PurePath(current_cwd).joinpath(self.io_dict["out"]["output_topology_path"])
        )

        os.chdir(tmp_folder)
        fu.log("Compressing topology to: %s" % top_final, self.out_log, self.global_log)
        fu.zip_top(zip_file=top_final, top_file="topology.top", out_log=self.out_log, remove_original_files=self.remove_tmp)
        os.chdir(current_cwd)

        fu.log("Exit code 0\n", self.out_log)

        # Run Biobb block
        # self.run_biobb()


pmxcreate_top = launcher(Pmxcreate_top)

if __name__ == "__main__":
    Pmxcreate_top.main()
