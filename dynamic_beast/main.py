import typer
import re
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom

app = typer.Typer()


def make_dynamic(element, key):
    _id = element.get("id")
    if key is None:
        value = element.text
        s = f"{_id}={value}"
        element.text = f"$({s})"
    else:
        value = element.get(key)
        if "$" in value:
            # Don't replace defaults that are already set
            # value = value.replace("$", "\$")
            return None
        if "=" in value:
            # https://github.com/CompEvol/beast2/blob/4d95f0095d20a6999d2757299c629bfbbf14b94b/src/beast/util/XMLParser.java#L372
            # the way that defaults are passed means you can't use '=' in there values...
            # https://github.com/CompEvol/beast2/pull/991
            return None
        s = f"{_id}.{key}={value}"
        element.set(key, f"$({s})")


def make_all_dynamic(element):
    for key in filter(lambda k: k != "id", element.keys()):
        make_dynamic(element, key)
    if element.tag == "parameter":
        make_dynamic(element, None)

def add_mc3_options(run):
    #<run id="mcmc" spec="beast.coupledMCMC.CoupledMCMC" chainLength="10000000" chains="4" target="0.234" logHeatedChains="true" deltaTemperature="0.1" optimise="true" resampleEvery="1000" >
    mc3_options = {
        'spec': 'beast.coupledMCMC.CoupledMCMC', 
        'chains': '2', 
        'target': '0.234', 
        'logHeatedChains': 'false', 
        'resampleEvery': '100', 
        'tempDir': '',
        'deltaTemperature': '0.1',
        # 'maxTemperature': '',  # cannot be set to '' 
        'optimise': 'true',
        'optimiseDelay': '100',
        'preSchedule': 'true'
        }
    for option in mc3_options:
        run.set(option, mc3_options[option])

@app.command()
def main(
    beast_xml: Path,
    outfile: Path = typer.Option(None, help="Path to save the dynamic BEAST XML file."),
    mc3: bool = typer.Option(False, help="Add default MC3 options to XML file."),
):
    """
    Dynamic BEAST XML
    """
    tree = ET.parse(beast_xml)
    root = tree.getroot()
    run = root.find("run")
    if mc3:
        add_mc3_options(run)
    for el in run.iter():
        if "idref" in el.keys():
            continue
        make_all_dynamic(el)
    if outfile:
        tree.write(outfile)
    else:
        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(newl="")
        typer.echo(xmlstr)
