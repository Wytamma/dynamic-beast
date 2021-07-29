from dynamic_beast import __version__, app
from typer.testing import CliRunner
import xml.etree.ElementTree as ET


def test_version():
    assert __version__ == "1.1.2"


runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["data/BEAST.xml"])
    assert result.exit_code == 0
    parsed = ET.fromstring(str(result.stdout))
    expected = ET.parse("data/dynamic_BEAST.xml")
    assert ET.tostring(parsed) == ET.tostring(expected.getroot())
