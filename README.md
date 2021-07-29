# Dynamic BEAST

[![PyPi](https://img.shields.io/pypi/v/dynamic-beast.svg)](https://pypi.org/project/dynamic-beast/)
[![tests](https://github.com/Wytamma/dynamic-beast/actions/workflows/test.yml/badge.svg)](https://github.com/Wytamma/dynamic-beast/actions/workflows/test.yml)
[![cov](https://codecov.io/gh/Wytamma/dynamic-beast/branch/master/graph/badge.svg)](https://codecov.io/gh/Wytamma/dynamic-beast)

This command line tool can be used to create a dynamic version of [BEAST2](http://www.beast2.org/) XML files. This dynamic XML file can be used to set BEAST parameters at runtime, which can be useful for testing different configurations or quickly modifying parameters without having to edit the XML file. 

## Install
Install `dynamic-beast` with pip (requires python -V >= 3.6.2).

```
pip install dynamic-beast
```

## Usage

Give `dynamic-beast` the path to a BEAST2 XML file and specify where to save the dynamic XML file (if outfile is not specified XML will be printed to screen).

```
dynamic-beast --outfile dynamic_BEAST.xml BEAST.xml
```

This will produce a `dynamic_BEAST.xml` file that can be used as standard in a BEAST analysis.

```
beast dynamic_BEAST.xml
```

To modify parameters at runtime use the `beast` definitions option `-D`.

```bash
# change the chain length to 1000. 
beast -D 'mcmc.chainLength=1000' dynamic_BEAST.xml
``` 

Multiple definitions can be passed at the same time.

```bash
# change the treelog and tracelog sampling freq to 10000. 
beast -D 'treelog.logEvery=10000,tracelog.logEvery=10000' dynamic_BEAST.xml
``` 

## Explanation

The `dynamic-beast` tool replaces all the parameter values in the XML file with the `$(id.key=value)` format. The value variable is the default value that was initially specified in the XML file. However, the value can be redefined when running a BEAST analysis by making use of the [BEAST2 definitions option](https://www.beast2.org/2021/03/31/command-line-options.html#-d) (`-D`) that allows for user specified values. 

To ensure reproducibility you should recreate static XML files of runs using dynamic parameters, this can be achieved using the `-DFout` argument e.g., `beast -D ‘clockRate=0.0002’ -DFout static_BEAST.xml dynamic_BEAST.xml`. 
