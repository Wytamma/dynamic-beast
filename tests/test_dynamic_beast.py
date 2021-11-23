from dynamic_beast import __version__, app
from typer.testing import CliRunner
import xml.etree.ElementTree as ET


def test_version():
    assert __version__ == "1.3.0"


runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["data/hcv_coal.xml"])
    assert result.exit_code == 0
    parsed = ET.fromstring(str(result.stdout))
    expected = ET.parse("data/dynamic_hcv_coal.xml")
    assert ET.tostring(parsed) == ET.tostring(expected.getroot())


def test_MC3():
    result = runner.invoke(app, ["--mc3", "data/hcv_bdsky.xml"])
    assert result.exit_code == 0
    parsed = ET.fromstring(str(result.stdout))
    expected = ET.parse("data/dynamic_mc3_hcv_bdsky.xml")
    assert ET.tostring(parsed) == ET.tostring(expected.getroot())


def test_PS():
    result = runner.invoke(app, ["--ps", "data/hcv_coal.xml"])
    assert result.exit_code == 0
    parsed = ET.fromstring(str(result.stdout))
    expected = ET.parse("data/dynamic_ps_hcv_coal.xml")
    assert ET.tostring(parsed) == ET.tostring(expected.getroot())


def test_optimise():
    result = runner.invoke(
        app,
        ["--optimise", "data/Heterochronous_H3N2.out", "data/Heterochronous_H3N2.xml"],
    )
    assert result.exit_code == 0
    parsed = ET.fromstring(str(result.stdout))
    expected = ET.parse("data/Heterochronous_H3N2_optimised.xml")
    assert ET.tostring(parsed) == ET.tostring(expected.getroot())
