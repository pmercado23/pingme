# PingMe

This is a script that runs a ping sweep across a defined network range. 

# Requirements

- Docker
- Python 3.9

# Local Install

To install locally, simply run

```shell
$ python3 -m pip install -r requirements.txt
```

This will install the required packages.

# Docker

This app has been dockerized.

## Build

To run a build, make sure docker is running and run the command `docker build -t pingme .`

This will use the defined def located in the Dockerfile.

```shell
$ docker build - t pingme .
[+] Building 73.7s(11 / 11) FINISHED
= > [internal] load build definition from Dockerfile
= > = > transferring dockerfile: 37B
= > [internal] load .dockerignore2B
= > [internal] load metadata for docker.io / library / ubuntu: 20.04
= > [internal] load build context
= > = > transferring context: 3.60kB
= > CACHED[1 / 6] FROM docker.io / library / ubuntu: 20.04 @ sha256: 450e066588f42ebe1551f3b1a535034b6aa46cd936fe7f2c6b0d72997ec61dbd
= > [2 / 6] COPY . .
= > [3 / 6] RUN apt - get update & & apt - get install - y software - properties - common gcc & &     add - apt - repository - y ppa: deadsnakes / ppa
= > [4 / 6] RUN apt - get update & & apt - get install - y python3.9 python3 - distutils python3 - pip python3 - apt iputils - ping
= > [5 / 6] COPY requirements.txt .
= > [6 / 6] RUN pip install - r requirements.txt
= > exporting to image
= > = > exporting layers
= > = > writing image sha256: f4ab08d3f884d3b6817892df99ad0d4884f0342ab4affd7038bf18e34c6d0af3
= > = > naming to docker.io / library / pingme

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
$
```

## Run

To run the docker image, first you must setup a network, then you can run the image as needed.

```shell
$ docker network create myping
$ docker network ls
NETWORK ID     NAME      DRIVER    SCOPE
973a331ff318   bridge    bridge    local
421df7ea69bb   host      host      local
b7278232143f   myping    bridge    local <---network created here
```

Then you can run the docker image with the network selected along with any flags added.

Example:

```shell
$ docker run --rm --name=app --network=myping pingme --networks '192.0.1.0/31' '192.0.2.0/28' '192.168.0.0/29' --skip 12 --retries 1
Running...
*********
{'down': ['192.0.1.0',
          '192.0.1.1',
          '192.0.2.1',
          '192.0.2.10',
          '192.0.2.11',
          '192.0.2.13',
          '192.0.2.14',
          '192.0.2.2',
          '192.0.2.3',
          '192.0.2.4',
          '192.0.2.5',
          '192.0.2.6',
          '192.0.2.7',
          '192.0.2.8',
          '192.0.2.9',
          '192.168.0.2',
          '192.168.0.3',
          '192.168.0.4',
          '192.168.0.5',
          '192.168.0.6'],
 'skipped': ['192.0.1.12', '192.0.2.12', '192.168.0.12'],
 'up': ['192.168.0.1']}
*********
Finished!
```

# Usage

Example usage for running a ping sweep across a range of addresses.

```shell
$ python3 ping_me.py --networks '192.168.0.180/31' --skip 12 --retries 1 -v

Running...
INFO: root: Running with retries: 1
INFO: root: Skipping hosts: ['192.168.0.12']
*********
{'down': ['192.168.0.181'],
 'skipped': ['192.168.0.12'],
 'up': ['192.168.0.180']}
*********
Finished!
```

- `--networks` is required to set a range of networks, this can be a single or a list of network ranges. This requires the format `x.x.x.x / x` .

`--networks '192.0.1.0/31'`

`--networks '192.0.1.0/31' '192.0.2.0/28' '192.168.0.0/'`

- `--retries` will define the number of time the ping is sent to a address on a fail attempt. Default is 2.

- `--skip 12` will skip all addresses in the network ranges given, i.e.

given: `--networks '192.0.1.0/31' '192.0.2.0/28' '192.168.0.0/29' - -skip 23` still skip `192.0.1.23`, `192.0.2.23` and `192.168.0.23`

- `-v` produces a more verbose output.

You can run the script with the -h command for more info.

```shell
$ python3 ping_me.py -h

usage: ProgramName[-h][--networks NETWORKS[NETWORKS ...]][--retries RETRIES][--skip SKIP][-v]

What the program does

optional arguments:
    -h, --help            show this help message and exit
    --networks NETWORKS[NETWORKS ...]
    --retries RETRIES     define number of retries for a ping. default is 2
    --skip SKIP           Address to skip, this will skip in all networks provided, default is None
    -v, --verbose         increase output verbosity

Text at the bottom of help
$
```

# Test

To run tests, simply run `python3 -m unittest`

```shell
$ python3 -m unittest
.........
----------------------------------------------------------------------
Ran 9 tests in 45.227s

OK
$
```

Tests can be found under `test.py`

# PEP8

This script is PEP8 formatted. to run formatter on the files, simply run:

```shell
$ autopep8 --in-place --aggressive --aggressive ping_me.py
$ autopep8 --in-place --aggressive --aggressive test.py
```

This will make format changes to each files defined.
