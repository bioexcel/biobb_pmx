#!/usr/bin/env python3

"""Module containing the PMX merge_ff class and the command line interface."""

import glob
from typing import Optional

from biobb_common.generic.biobb_object import BiobbObject, launcher
from biobb_common.tools import file_utils as fu
from pmx import ligand_alchemy  # type: ignore


class Pmxmerge_ff(BiobbObject):
    """
    | biobb_pmx Pmxmerge_ff
    | Wrapper class for the `PMX merge_ff <https://github.com/deGrootLab/pmx>`_ module.
    | Merge ligand topology files.

    Args:
        input_topology_path (str): Path to the input ligand topologies as a zip file containing a list of itp files. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/itps_to_merge.zip>`_. Accepted formats: zip (edam:format_3987).
        output_topology_path (str): Path to the merged ligand topology file. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_mergedTopology.itp>`_. Accepted formats: itp (edam:format_3883).
        properties (dic):
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_pmx.pmxbiobb.pmxmerge_ff import pmxmerge_ff
            prop = {
                'remove_tmp' : True
            }
            pmxmerge_ff(input_topology_path='/path/to/myTopologies.zip',
                    output_topology_path='/path/to/myMergedTopology.itp',
                    properties=prop)

    Info:
        * wrapped_software:
            * name: PMX merge_ff
            * version: >=1.0.1
            * license: GNU
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(
        self,
        input_topology_path: str,
        output_topology_path: str,
        properties: Optional[dict] = None,
        **kwargs,
    ) -> None:
        super().__init__(**locals())

        # Properties specific for BB
        # None yet

    def stage_files(self) -> None:
        """The block does not use the sandbox: there are no files to stage."""

    def run(self) -> None:
        """Execute the :class:`Pmxmerge_ff <pmx.pmxmerge_ff.Pmxmerge_ff>` pmx.pmxmerge_ff.Pmxmerge_ff object."""

        # Creating temporary folder
        tmp_folder = self.create_tmp_dir(log=True)

        fu.unzip_list(
            self.io_dict["in"]["input_topology_path"],
            tmp_folder,
            out_log=self.out_log,
        )
        files = glob.glob(tmp_folder + "/*.itp")
        ffsIn_list = []
        for itp in files:
            ffsIn_list.append(itp)

        fu.log("Running merge_FF_files from pmx package...\n", self.out_log)
        ligand_alchemy._merge_FF_files(
            self.io_dict["out"]["output_topology_path"], ffsIn=ffsIn_list
        )
        # ffsIn=[self.io_dict["in"]["input_topology1_path"],self.io_dict["in"]["input_topology2_path"]] )

        fu.log("Exit code 0\n", self.out_log)

        # Run Biobb block
        # self.run_biobb()


pmxmerge_ff = launcher(Pmxmerge_ff)

if __name__ == "__main__":
    Pmxmerge_ff.main()
