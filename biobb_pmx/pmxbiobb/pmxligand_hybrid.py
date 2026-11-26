#!/usr/bin/env python3

"""Module containing the PMX ligand_hybrid class and the command line interface."""

from typing import Optional

from biobb_common.generic.biobb_object import BiobbObject, launcher
from biobb_pmx.pmxbiobb.common import check_binary


class Pmxligand_hybrid(BiobbObject):
    """
    | biobb_pmx Pmxligand_hybrid
    | Wrapper class for the `PMX ligand_hybrid <https://github.com/deGrootLab/pmx>`_ module.
    | Create a hybrid topology and structure based on two ligand structures.

    Args:
        input_structure1_path (str): Path to the input ligand structure file 1. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/lig1.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_structure2_path (str): Path to the input ligand structure file 2. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/lig2.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_topology1_path (str): Path to the input ligand topology file 1. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/topoLig1.itp>`_. Accepted formats: itp (edam:format_3883).
        input_topology2_path (str): Path to the input ligand topology file 2. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/topoLig2.itp>`_. Accepted formats: itp (edam:format_3883).
        input_pairs_path (str) (Optional): Path to the input atom pair mapping. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/myPairs1.dat>`_. Accepted formats: dat (edam:format_1637), txt (edam:format_2330).
        input_scaffold1_path (str) (Optional): Path to the index of atoms to consider for the ligand structure 1. File type: input. Accepted formats: ndx (edam:format_2033).
        input_scaffold2_path (str) (Optional): Path to the index of atoms to consider for the ligand structure 2. File type: input. Accepted formats: ndx (edam:format_2033).
        output_log_path (str): Path to the log file. File type: output. Accepted formats: log (edam:format_2330), txt (edam:format_2330), out (edam:format_2330).
        output_structure1_path (str): Path to the output hybrid structure based on the ligand 1. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_hybridStructure1.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_structure2_path (str): Path to the output hybrid structure based on the ligand 2. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_hybridStructure2.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_topology_path (str): Path to the output hybrid topology. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_hybridTopology.itp>`_. Accepted formats: itp (edam:format_3883).
        output_atomtypes_path (str): Path to the atom types for the output hybrid topology. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_hybridAtomTypes.itp>`_. Accepted formats: itp (edam:format_3883).

        properties (dic):
            * **fit** (*bool*) - (False) Fit ligand structure 1 onto ligand structure 2 (Only used if input_pairs_path is provided).
            * **split** (*bool*) - (False) Split the topology into separate transitions.
            * **scDUMm** (*float*) - (None) Scale dummy masses using the counterpart atoms. If not set, the tool uses its own default.
            * **scDUMa** (*float*) - (None) Scale bonded dummy angle parameters. If not set, the tool uses its own default.
            * **scDUMd** (*float*) - (None) Scale bonded dummy dihedral parameters. If not set, the tool uses its own default.
            * **deAng** (*bool*) - (False) Decouple angles composed of 1 dummy and 2 non-dummies.
            * **distance** (*float*) - (None) Distance (nm) between atoms to consider them morphable for alignment approach (Only used if input_pairs_path is not provided). If not set, the tool uses its own default.
            * **binary_path** (*str*) - ("pmx") Path to the PMX command line interface.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.
            * **container_path** (*str*) - (None)  Path to the binary executable of your container.
            * **container_image** (*str*) - (None) Container Image identifier.
            * **container_volume_path** (*str*) - ("/inout") Path to an internal directory in the container.
            * **container_user_id** (*str*) - (None) User number id to be mapped inside the container.
            * **container_shell_path** (*str*) - ("/bin/bash") Path to the binary executable of the container shell.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_pmx.pmxbiobb.pmxligand_hybrid import pmxligand_hybrid
            prop = {
                'fit' : True,
                'distance': 0.05
            }
            pmxligand_hybrid(input_structure1_path='/path/to/myStructure1.pdb',
                    input_structure2_path='/path/to/myStructure2.pdb',
                    input_topology1_path='/path/to/myTopology1.pdb',
                    input_topology2_path='/path/to/myTopology2.pdb',
                    input_pairs_path='/path/to/myPairs.dat',
                    output_log_path='/path/to/myLog.log',
                    output_structure1_path='/path/to/myStructureOutput1.pdb',
                    output_structure2_path='/path/to/myStructureOutput2.pdb',
                    output_topology_path='/path/to/myTopologyOutput.pdb',
                    output_atomtypes_path='/path/to/myAtomTypesOutput.pdb',
                    properties=prop)

    Info:
        * wrapped_software:
            * name: PMX ligand_hybrid
            * version: >=1.0.1
            * license: GNU
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(
        self,
        input_structure1_path: str,
        input_structure2_path: str,
        input_topology1_path: str,
        input_topology2_path: str,
        output_log_path: str,
        output_structure1_path: str,
        output_structure2_path: str,
        output_topology_path: str,
        output_atomtypes_path: str,
        input_scaffold1_path: Optional[str] = None,
        input_scaffold2_path: Optional[str] = None,
        input_pairs_path: Optional[str] = None,
        properties: Optional[dict] = None,
        **kwargs,
    ) -> None:
        super().__init__(**locals())

    def prepare(self) -> None:
        """Check that the pmx executable is installed."""
        check_binary(self.binary_path, self.container_path)

    def run(self) -> None:
        """Execute the :class:`Pmxmutate <pmx.pmxmutate.Pmxmutate>` pmx.pmxmutate.Pmxmutate object."""

        self.cmd = [
            self.binary_path,
            "ligandHybrid",
            "-i1",
            self.stage_io_dict["in"]["input_structure1_path"],
            "-i2",
            self.stage_io_dict["in"]["input_structure2_path"],
            "-itp1",
            self.stage_io_dict["in"]["input_topology1_path"],
            "-itp2",
            self.stage_io_dict["in"]["input_topology2_path"],
            "-oA",
            self.stage_io_dict["out"]["output_structure1_path"],
            "-oB",
            self.stage_io_dict["out"]["output_structure2_path"],
            "-oitp",
            self.stage_io_dict["out"]["output_topology_path"],
            "-offitp",
            self.stage_io_dict["out"]["output_atomtypes_path"],
            "-log",
            self.stage_io_dict["out"]["output_log_path"],
        ]

        if self.stage_io_dict["in"].get("input_pairs_path"):
            self.cmd.append("-pairs")
            self.cmd.append(self.stage_io_dict["in"]["input_pairs_path"])

        if self.stage_io_dict["in"].get("input_scaffold1_path"):
            self.cmd.append("-n1")
            self.cmd.append(self.stage_io_dict["in"]["input_scaffold1_path"])

        if self.stage_io_dict["in"].get("input_scaffold2_path"):
            self.cmd.append("-n2")
            self.cmd.append(self.stage_io_dict["in"]["input_scaffold2_path"])

        if self.fit:
            self.cmd.append("--fit")
        if self.split:
            self.cmd.append("--split")
        if self.deAng:
            self.cmd.append("--deAng")
        if self.distance:
            self.cmd.append("--d")
            self.cmd.append(str(self.distance))
        if self.scDUMm:
            self.cmd.append("--scDUMm")
            self.cmd.append(str(self.scDUMm))
        if self.scDUMa:
            self.cmd.append("--scDUMa")
            self.cmd.append(str(self.scDUMa))
        if self.scDUMd:
            self.cmd.append("--scDUMd")
            self.cmd.append(str(self.scDUMd))

        # Run Biobb block
        self.run_biobb()


pmxligand_hybrid = launcher(Pmxligand_hybrid)

if __name__ == "__main__":
    Pmxligand_hybrid.main()
