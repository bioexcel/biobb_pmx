#!/usr/bin/env python3

"""Module containing the PMX mutate class and the command line interface."""

from typing import Optional

from biobb_common.generic.biobb_object import BiobbObject, launcher

from biobb_pmx.pmxbiobb.common import MUTATION_DICT, check_binary, create_mutations_file, set_gmxlib


class Pmxmutate(BiobbObject):
    """
    | biobb_pmx Pmxmutate
    | Wrapper class for the `PMX mutate <https://github.com/deGrootLab/pmx>`_ module.
    | Mutate residues in a protein structure.

    Args:
        input_structure_path (str): Path to the input structure file. File type: input. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/frame99.pdb>`_. Accepted formats: pdb (edam:format_1476), gro (edam:format_2033).
        output_structure_path (str): Path to the output structure file. File type: output. `Sample file <https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_output_structure.pdb>`_. Accepted formats: pdb (edam:format_1476), gro (edam:format_2033).
        input_b_structure_path (str) (Optional): Path to the mutated input structure file. File type: input. Accepted formats: pdb (edam:format_1476), gro (edam:format_2033).
        properties (dic):
            * **mutation_list** (*str*) - ("2Ala") Mutation list in the format "Chain:Resnum MUT_AA_Code" or "Chain:Resnum MUT_NA_Code"  (no spaces between the elements) separated by commas. If no chain is provided as chain code all the chains in the pdb file will be mutated. ie: "A:15CYS". Possible MUT_AA_Code: 'ALA', 'ARG', 'ASN', 'ASP', 'ASPH', 'ASPP', 'ASH', 'CYS', 'CYS2', 'CYN', 'CYX', 'CYM', 'CYSH', 'GLU', 'GLUH', 'GLUP', 'GLH', 'GLN', 'GLY', 'HIS', 'HIE', 'HISE', 'HSE', 'HIP', 'HSP', 'HISH', 'HID', 'HSD', 'ILE', 'LEU', 'LYS', 'LYSH', 'LYP', 'LYN', 'LSN', 'MET', 'PHE', 'PRO', 'SER', 'SP1', 'SP2', 'THR', 'TRP', 'TYR', 'VAL'. Possible MUT_NA_Codes: 'A', 'T', 'C', 'G', 'U'.
            * **force_field** (*str*) - ("amber99sb-star-ildn-mut") Forcefield to use.
            * **resinfo** (*bool*) - (False) Show the list of 3-letter -> 1-letter residues.
            * **gmx_lib** (*str*) - (None) Path to the GMXLIB folder in your computer. If not set, the mutff folder of the pmx package of the Python environment (in a container, of the image).
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

            from biobb_pmx.pmxbiobb.pmxmutate import pmxmutate
            prop = {
                'mutation_list': '2Ala, 3Val',
                'gmx_lib': '/path/to/myGMXLIB/',
                'force_field': 'amber99sb-star-ildn-mut'
            }
            pmxmutate(input_structure_path='/path/to/myStructure.pdb',
                    output_structure_path='/path/to/newStructure.pdb',
                    input_b_structure_path='/path/to/myStructureB.pdb'
                    properties=prop)

    Info:
        * wrapped_software:
            * name: PMX mutate
            * version: >=1.0.1
            * license: GNU
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(
        self,
        input_structure_path: str,
        output_structure_path: str,
        input_b_structure_path: Optional[str] = None,
        properties: Optional[dict] = None,
        **kwargs,
    ) -> None:
        super().__init__(**locals())

    def prepare(self) -> None:
        """Check that the pmx executable is installed and write the mutations file of the
        mutation_list property, staged with the inputs."""
        check_binary(self.binary_path, self.container_path)
        self.io_dict["in"]["input_mutations_path"] = create_mutations_file(
            input_mutations_path=self.create_tmp_file(".txt"),
            mutation_list=self.mutation_list,
            mutation_dict=MUTATION_DICT,
        )

    def run(self) -> None:
        """Execute the :class:`Pmxmutate <pmx.pmxmutate.Pmxmutate>` pmx.pmxmutate.Pmxmutate object."""

        self.cmd = [
            self.binary_path,
            "mutate",
            "-f",
            self.stage_io_dict["in"]["input_structure_path"],
            "-o",
            self.stage_io_dict["out"]["output_structure_path"],
            "-ff",
            self.force_field,
            "--script",
            self.stage_io_dict["in"]["input_mutations_path"],
        ]

        if self.stage_io_dict["in"].get("input_b_structure_path"):
            self.cmd.append("-fB")
            self.cmd.append(self.stage_io_dict["in"]["input_b_structure_path"])
        if self.resinfo:
            self.cmd.append("-resinfo")

        set_gmxlib(self)

        # Run Biobb block
        self.run_biobb()


pmxmutate = launcher(Pmxmutate)

if __name__ == "__main__":
    Pmxmutate.main()
