# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmxbiobb.pmxgentop import pmxgentop
import pytest
import sys


class TestPmxgentopDocker:
    def setup_class(self):
        fx.test_setup(self, 'pmxgentop_docker')

    def teardown_class(self):
        pass
        # fx.test_teardown(self)

    def test_pmxgentop_docker(self):
        pmxgentop(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_top_zip_path'])
        assert fx.equal(self.paths['output_top_zip_path'], self.paths['ref_output_top_zip_path'])


@pytest.mark.skipif(sys.platform == 'darwin', reason="singularity not available on macOS")
class TestPmxgentopSingularity:
    def setup_class(self):
        fx.test_setup(self, 'pmxgentop_singularity')

    def teardown_class(self):
        pass
        # fx.test_teardown(self)

    def test_pmxgentop_singularity(self):
        pmxgentop(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_top_zip_path'])
        #assert fx.equal(self.paths['output_top_zip_path'], self.paths['ref_output_top_zip_path'])
