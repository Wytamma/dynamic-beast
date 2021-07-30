from dynamic_beast import __version__, app
from typer.testing import CliRunner
import xml.etree.ElementTree as ET


def test_version():
    assert __version__ == "1.2.0"


runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["data/hcv_coal.xml"])
    assert result.exit_code == 0
    parsed = ET.fromstring(str(result.stdout))
    expected = ET.parse("data/dynamic_hcv_coal.xml")
    assert ET.tostring(parsed) == ET.tostring(expected.getroot())
