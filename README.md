# iCHIP

iCHIP is a python library which characterises MOS transistors and outputs
the parameters needed for Inversion Co-efficient style design [1][2].

## Installation

There are several options for installing iCHIP. The current preferred
method is to use pip to install from the git re. This ensures that the 
dependencies are also installed.

```bash
pip install git+https://github.com/sobremesa87/iCHIP.git
```

Alternatively, you can just clone the repo

```bash
git clone https://github.com/sobremesa87/iCHIP.git
```

In this case, you will need to install the dependencies yourself. Note that one of its dependencies is the
spyci raw file loading package [3]. However, the packaged version of
spyci does not work with the ngspice files used to test iCHIP. Therefore,
until the packaged version is updated, a version of spyci available on
git must be used [4]. The requirements.txt file contained in this repo
installs the correct version. Therefore, be sure to install required packages
using the requirements file as shown below rather than individually. This 
will ensure that the correct version of spyci is used.

```bash
pip install -r requirements.txt
```

Alternatively, that dependency can as installed as shown.

```bash
pip install git+https://github.com/sobremesa87/spyci.git
```

## Usage

Usage requires a file representing an Ids vs. Vgs sweep and an
Ids vs. Vds sweep for each transistor type you would like to 
characterise. Example raw files are in the tests/test_data folder 
and are taken from simulations on the open source skywater process [5].
See the wiki for more details. 

Code is mostly in the "MOS" object in the "characterisation.py" file. This
can be imported into other code, to be used as the basis for design 
calculations, or the characterisation.py file can be run directly as a
script. In this mode, when properly configured, the script outputs an
HTML file summarising the IC parameters, which can be used as a basis for
hand calculations. It also plots several graphs, allowing the user to check
that the results are well conditioned.

## Contributing
Issue reports and pull requests correcting bugs or adding features are
greatly welcomed. Before submitting a pull request, please ensure that
you pass all the existing tests, and have added a test for your new
feature if necessary.

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

## References
[1] C. Enz, F. Chicco and A. Pezzotta, "Nanoscale MOSFET Modeling: Part 1: The Simplified EKV Model for the Design of Low-Power Analog Circuits," in IEEE Solid-State Circuits Magazine, vol. 9, no. 3, pp. 26-35, Summer 2017, doi: 10.1109/MSSC.2017.2712318.  
[2] C. Enz, F. Chicco and A. Pezzotta, "Nanoscale MOSFET Modeling: Part 2: Using the Inversion Coefficient as the Primary Design Parameter," in IEEE Solid-State Circuits Magazine, vol. 9, no. 4, pp. 73-81, Fall 2017, doi: 10.1109/MSSC.2017.2745838.  
[3] https://github.com/gmagno/spyci  
[4] https://github.com/sobremesa87/spyci  
[5] https://github.com/google/skywater-pdk  
