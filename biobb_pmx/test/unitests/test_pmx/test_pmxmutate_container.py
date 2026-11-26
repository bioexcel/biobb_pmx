# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmxbiobb.pmxmutate import pmxmutate
import pytest
import sys


class TestPmxmutateDocker:
    def setup_class(self):
        fx.test_setup(self, 'pmxmutate_docker')

    def teardown_class(self):
        # pass
        fx.test_teardown(self)

    def test_pmxmutate_docker(self):
        pmxmutate(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_structure_path'])
        assert fx.equal(self.paths['output_structure_path'], self.paths['ref_output_structure_path'])


class TestPmxmutateDockerGmxlib:
    """No gmx_lib: GMXLIB is the mutff folder of the pmx package of the image."""
    def setup_class(self):
        fx.test_setup(self, 'pmxmutate_docker_gmxlib')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_pmxmutate_docker_gmxlib(self):
        pmxmutate(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_structure_path'])
        assert fx.equal(self.paths['output_structure_path'], self.paths['ref_output_structure_path'])


@pytest.mark.skipif(sys.platform == 'darwin', reason="singularity not available on macOS")
class TestPmxmutateSingularity:
    def setup_class(self):
        fx.test_setup(self, 'pmxmutate_singularity')

    def teardown_class(self):
        # pass
        fx.test_teardown(self)

    def test_pmxmutate_singularity(self):
        pmxmutate(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_structure_path'])
        assert fx.equal(self.paths['output_structure_path'], self.paths['ref_output_structure_path'])
