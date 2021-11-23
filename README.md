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

Give `dynamic-beast` the path to a BEAST2 XML file and specify where to save the dynamic XML file (if `--outfile` is not specified XML will be printed to stdout).

```bash
dynamic-beast --outfile dynamic_hcv_coal.xml hcv_coal.xml
```

This will produce a `dynamic_hcv_coal.xml` file that can be used as standard in a BEAST analysis.

```bash
beast dynamic_hcv_coal.xml
```

To modify parameters at runtime use the `beast` definitions option `-D`.

```bash
# Change the chain length to 1000. 
beast -D 'mcmc.chainLength=1000' dynamic_hcv_coal.xml
``` 

Multiple definitions can be passed at the same time.

```bash
# Change the treelog and tracelog sampling freq to 10000. 
beast -D 'treelog.logEvery=10000,tracelog.logEvery=10000' dynamic_hcv_coal.xml
``` 

The full `id` of a parameter you'd like to set must be specified. 

```bash 
beast -D 'clockRate.c:hcv=7.9E-4' dynamic_hcv_coal.xml
```

### CoupledMCMC

MC3 options for the BEAST package [CoupledMCMC](https://github.com/nicfel/CoupledMCMC) can be added by using the `--mc3` option. This will add the default CoupledMCMC options which can then be configured at runtime with `-D`. 

```bash
# Create dynamic MC3 XML 
dynamic-beast --mc3 --outfile dynamic_mc3_hcv_coal.xml hcv_coal.xml
# Configure MC3 with BEAST
beast -D 'mcmc.chains=4' dynamic_mc3_hcv_coal.xml
```

### Path Sampling (Stepping Stone)

Path sampling options for the package [model-selection](https://github.com/BEAST2-Dev/model-selection) can be add by using the `--ps` option. This will add the default model-selection options (e.g. stepping stone) which can then be configured at runtime with `-D`. 

```bash
# Create dynamic Path Sampling XML 
dynamic-beast --ps --outfile dynamic_ps_hcv_coal.xml hcv_coal.xml
# Configure Path Sampling with BEAST
beast -D "ps.doNotRun=true,ps.rootdir=$(pwd)" dynamic_ps_hcv_coal.xml
```

### Auto apply optimisation suggestion

At the end of a analysis BEAST provides suggestions for optimising operators e.g. `Try setting scaleFactor to about 0.96`. See the end of the [example file](https://github.com/Wytamma/dynamic-beast/blob/master/data/Heterochronous_H3N2.out). A path to the output file can be provided to the `--optimise` flag and the suggestions will automatically be extracted and applied to the generated dynamic XML file. 

```bash
dynamic-beast --optimise hcv_coal.out --outfile dynamic_hcv_coal.xml hcv_coal.xml
```

## Explanation

The `dynamic-beast` tool replaces all the parameter values in the XML file with the `$(id.key=value)` format. The value variable is the default value that was initially specified in the XML file. However, the value can be redefined when running a BEAST analysis by making use of the [BEAST2 definitions option](https://www.beast2.org/2021/03/31/command-line-options.html#-d) (`-D`) that allows for user specified values. 

To ensure reproducibility you should recreate static XML files of runs using dynamic parameters, this can be achieved using the `-DFout` argument e.g., `beast -D 'clockRate.c:hcv=7.9E-4' -DFout static_hcv_coal.xml dynamic_hcv_coal.xml`. 
