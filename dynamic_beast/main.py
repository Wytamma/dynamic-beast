import typer
import re
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom

app = typer.Typer()


def make_dynamic(element, key):
    id = element.get("id").split(".")[0]
    if key is None:
        value = element.text
        s = f"{id}={value}"
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
        s = f"{id}.{key}={value}"
        element.set(key, f"$({s})")


def make_all_dynamic(element):
    for key in filter(lambda k: k != "id", element.keys()):
        make_dynamic(element, key)
    if element.tag == "parameter":
        make_dynamic(element, None)


@app.command()
def main(
    beast_xml: Path,
    outfile: Path = typer.Option(None, help="Path to save the dynamic BEAST XML file."),
):
    """
    Dynamic BEAST XML
    """
    tree = ET.parse(beast_xml)
    root = tree.getroot()
    run = root.find("run")
    for el in run.iter():
        if "idref" in el.keys():
            continue
        make_all_dynamic(el)
    if outfile:
        tree.write(outfile)
    else:
        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(newl="")
        typer.echo(xmlstr)
