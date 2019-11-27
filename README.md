[![Build Status](https://travis-ci.org/hexhex/hexlite.svg?branch=master)](https://travis-ci.org/hexhex/hexlite)
[![codebeat badge](https://codebeat.co/badges/5493bd59-f87f-470c-9069-86d4c14dd374)](https://codebeat.co/projects/github-com-hexhex-hexlite-master)
[![Anaconda-Server Badge](https://anaconda.org/peterschueller/hexlite/badges/installer/conda.svg)](https://conda.anaconda.org/peterschueller)

# Hexlite - Solver for a fragment of HEX

This is a solver for a fragment of the HEX language and for Python-based plugins
which is based on Python interfaces of Clingo and does not contain any C++ code itself.

The intention is to provide a lightweight system for an easy start with HEX.

The vision is that HEXLite can use existing Python plugins and runs based on
the Clingo python interface, without realizing the full power of HEX.

The system is currently under development and only works for certain programs:
* External atoms with only constant inputs are evaluated during grounding in Gringo
* External atoms with predicate input(s) and no constant outputs are evaluated during solving in a clasp Propagator
* External atoms with predicate input(s) and constant outputs that have a domain predicate can also be evaluated
* Liberal Safety is not implemented
* Properties of external atoms are not used
* If it has a finite grounding, it will terminate, otherwise, it will not - as usual with Gringo
* FLP Check is implemented explicitly and does not work with strong negation and weak constraints
* FLP Check can be deactivated

A manuscript about the system is under preparation.

In case of bugs please report an issue here: https://github.com/hexhex/hexlite/issues

* License: GPL (3.0)
* Author: Peter Schüller <schueller.p@gmail.com>
* Available at PyPi: https://pypi.python.org/pypi/hexlite
* Installation with Conda:

  The easiest way to install `hexlite` is Conda.
  
  First you need to install the `clingo` dependency:

  ```$ conda install -c potassco clingo```

  Then you install hexlite:

  ```$ conda install -c peterschueller hexlite```

  (If you wonder why we do not automatically install clingo as a dependency:
  certain conda restrictions prevent that `clingo` is automatically installed
  unless the potassco channel is **manually** added by the user.)

  Then you test hexlite:

  ```$ hexlite -h```

* Installation with pip:

  This will download, build, and locally install Python-enabled `clingo` modules.

  * If you do not have it: install `python-pip`: for example under Ubuntu via
    
    ```$ sudo apt-get install python-pip```

  * Install hexlite:

    ```$ pip install hexlite --user```

  * Setup Python to use the "Userinstall" environment that allows you
    to install Python programs without overwriting system packages:

    Add the following to your `.profile` or `.bashrc` file:

```
export PYTHONUSERBASE=~/.local/
export PATH=$PATH:~/.local/bin
```

  * Run hexlite the first time. This will help to download and build pyclingo unless it is already usable via `import clingo`:

    ```$ hexlite```

    The first run of hexlite might ask you to enter the sudo password
    to install several packages.
    (You can do this manually. Simply abort and later run `hexlite` again.)

  * Ubuntu 16.04 is tested
  * Debian 8.6 (jessie) is tested
  * Ubuntu 14.04 can not work without manual installation of cmake 3.1 or higher (for buildling clingo)

# Running Hexlite on Examples in the Repository

* If ``hexlite`` by itself shows the help, you can run it on some examples in the repository.

* Hexlite needs to know where to find plugins and what is the name of the Python modules of these plugins

	* The path for plugins is given as argument ``--pluginpath <path>``.

	  This argument can be given multiple times. You can use absolute or relative paths.

	* The python modules to load are given as argument ``--plugin <module> [<argument1> <argument2>]``.
	
	  Multiple plugins can be loaded.
          Each plugin can have arguments.

	  !ATTENTION!:
	  If you specify the HEX input file after ``--plugin <module>``, it becomes the argument of the plugin.
	  In this case, you need to
	
	  * specify the HEX input files _before_ the other arguments
	  or
	  * indicate end of the argument list with the ``--`` option.

* To run one of the examples in the ``tests/`` directory you can use one of the following methods to call hexlite:

```
$ hexlite --pluginpath ./plugins/ --plugin testplugin -- tests/extatom3.hex
$ hexlite tests/extatom3.hex --pluginpath ./plugins/ --plugin testplugin
$ hexlite --pluginpath=./plugins/ --plugin=testplugin tests/extatom3.hex
```

# Developer Readme

* For developing hexlite without uploading to anaconda repository:

  * Install clingo with conda, but but do **not** install hexlite with conda.

  ```$ conda install -c potassco clingo```

  * checkout hexlite with git

  ```$ git clone git@github.com:hexhex/hexlite.git```

  * install `hexlite` in develop mode into your user-defined Python space:

  ```$ python3 setup.py develop --user```

  * If you want to remove this development installation:

```
$ python3 setup.py develop --uninstall --user
$ rm ~/.local/bin/hexlite
```

  (Installed scripts are not automatically uninstalled.)

* For building and uploading a new version to pip and conda (Note: conda requires to upload to pip first)
  
  * Update version in `setup.py`.

  * Build pypi source package

  `$ python setup.py sdist`

	* Verify that dist/ contains the right archives with the right content (no wheels etc.)

	* Upload to pypi

	`$ twine upload dist/*`

  * Update version in `meta.yaml`.

  * Build for anaconda cloud
  
  First, some conda packages need to be installed via `conda install conda-build conda-verify anaconda`.

  `$ conda build .`

	(get upload command from last lines of output)

  If conda is installed on an encrypted /home/ or similar, this will abort with a permission error.
  You can make it work by creating a new directory on an unencrypted `/tmp/`, for example `/tmp/conda-build`,
  and run conda build as follows:

  `$ conda build --croot /tmp/conda-build/ .`

  * Verify that archive to upload contains the right content (and no backup files, experimental results, etc...)

	`$ anaconda upload <path-from-conda-build>`

* Roadmap

  - implement a python plugin
    that has hardcoded the java plugin interface
    that has hardcoded the loading of the string java plugin
  - implement and test the plugin interface
  - implement proper java plugin loading in the python plugin
  - cleanly separate python hexlite core and python-java api as a plugin
  - make it deployable via conda and pip

* Jpype

  - the current release of jpype is 0.7 which does not contain a fix we need for this project
  - therefore we need to build jpype manually (e.g., within conda)
  - because of a bug in current conda we need to disable the conda-internal linker to build jpype

    $ git clone https://github.com/jpype-project/jpype.git
    $ cd jpype
    $ python setup.py sdist
    $ conda activate <your-environment>
    $ mv <your-conda-environment>/compiler_compat/ld <your-conda-environment>/compiler_compat/ld_rename_to_ld
    $ pip install dist/* --global-option=--disable-numpy
    $ mv <your-conda-environment>/compiler_compat/ld_rename_to_ld <your-conda-environment>/compiler_compat/ld

  - once jpype in conda contains the fix (in 0.7.1):

    $ conda install -c conda-forge jpype1  