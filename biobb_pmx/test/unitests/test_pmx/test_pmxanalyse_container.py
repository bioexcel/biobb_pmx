# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmxbiobb.pmxanalyse import pmxanalyse
import pytest
import sys


class TestPmxanalyseDocker():
    def setup_class(self):
        fx.test_setup(self, 'pmxanalyse_docker')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_pmxanalyse_docker(self):
        pmxanalyse(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_result_path'])


@pytest.mark.skipif(sys.platform == 'darwin', reason="singularity not available on macOS")
class TestPmxanalyseSingularity:
    def setup_class(self):
        fx.test_setup(self, 'pmxanalyse_singularity')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_pmxanalyse_singularity(self):
        pmxanalyse(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_result_path'])
