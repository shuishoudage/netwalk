## Project Netwalk

This project is part of my social media analysis course project. In this project several graph theory related algorithms are implemented. For centrality analysis, classic pagerank algorithm and brandes algorithms are implemented.


### System requirements

This project using external library `numpy` to manipulate matrix operations. Therefore, install numpy is mandatory to run this project properly.

If you want to run testing cases, a library called [parameterized](https://pypi.org/project/parameterized/) is required to be installed.

`conda` is recommended to use as an environment management tool. However, built-in `virtualenv` command can be used as well. If you use `conda`, run following command to create the environment first
```bash
conda env create --file env.yaml
```

if you use `virtualenv`, after create your environment, install packages by pip3
```bash
pip3 install -r requirements.txt
```

### Run application

The driver file for this application is `main.py`. Any other objects are encapsulated into package called `netwalk` :). Therefore, if you want to use any other algorithms, you can import into your application as well.