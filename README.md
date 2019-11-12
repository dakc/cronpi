[![Build Status](https://travis-ci.com/dakc/cronpi.svg?branch=master)](https://travis-ci.com/dakc/cronpi)
[![pypi](https://img.shields.io/pypi/dm/cronpi)](https://pypi.org/project/cronpi/) 
[![GitHub license](https://img.shields.io/github/license/dakc/majidai.svg?style=popout)](https://raw.githubusercontent.com/dakc/cronpi/master/LICENSE) 

# cronpi
A small tool for deploying crontab jobs into a unix-like system, eg. Linux/Mac from python.
> cronpi makes jobs more ***human readable*** and works on both 2.X and 3.X version.


## Installation
```bash
pip install cronpi
```

## Usage
cronpi has following functions

| SN  |      Name       |                                    Description                                    |
| --- | --------------- | --------------------------------------------------------------------------------- |
| 1.  | run_by_date     | job that runs just once by setting date in format YYYY-MM-DD HH:mm                |
| 2.  | run_every_day   | job that runs every day at given time HH:mm                                       |
| 3.  | run_every_week  | job that runs every week at the given time of given weekdays                      |
| 4.  | run_every_month | job that runs every month at the given time of given days of a month              |
| 5.  | run_every_year  | job that runs  at the given time of given days of given months                    |
| 6.  | run_custom      | command will be exactly similar to single line which we write during "crontab -e" |

Each functions take two parameters
###### &lt;command to execute&gt;, &lt;isOverwrite=bool&gt;?

|  parameter  |  type  |                                       description                                        |
| ----------- | ------ | ---------------------------------------------------------------------------------------- |
| command     | string | This command will be executed as scheduled                                               |
| isOverwrite | bool   | It is optional and default value is false, which means cronpi will always insert new job |

>cronpi will always install a new cron job if only command is passed as parameter or isOverwrite is set to False.
If command passed as first parameter already exists in cronjon and "isOverwrite=True" is passed as second parameter ,then it will update the time of running the job instead of adding new job.
```python
cronpi.XXXX("/some/command", isOverwrite=True)
```

#### Use Case 1 - Run once
1. Run a job at 20th october 2020 at 5:30PM
```python
cronpi.run_by_date("/some/command").on("2020-10-20 5:30pm")
```

#### Use Case 2 - Run every day
1. Run a job daily at 5:30PM
```python
cronpi.run_every_day("/some/command").on("5:30pm")
```

#### Use Case 3 - Run every week
1. Run a job at every sunday at 5:30PM
```python
cronpi.run_every_week("/some/command").on("sunday", time="17:30")
```

2. Run a job at every saturday and sunday at 5:30PM
```python
cronpi.run_every_week("/some/command").on(["sat", "sun"], time="5:30PM")
```

#### Use Case 4 - Run every month
1. Run a job at every 10th of a month at 5:30PM
```python
cronpi.run_every_month("/some/command").on(10, time="17:30")
```

2. Run a job at every 10th and 20th of a month at 5:30PM
```python
cronpi.run_every_month("/some/command").on([10,20], time="17:30")
```


#### Use Case 5 - Run every year
1. Run a job at every 10th january at 5:30am
```python
cronpi.run_every_year("/some/command").on("january", day=10, time="5:30am")
```

2. Run a job at every 10th of january, april and october at 5:30AM
```python
cronpi.run_every_year("/some/command").on(["jan", "oct"], day=10, time="5:30")
```

#### Use Case 6 - run like crontab
Add a job to crontab by passing the command that we input to "crontab -e" command. 
1. Run a job that runs at every minute
```python
cronpi.run_custom("* * * * * /some/command")
```

```bash
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of the month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday;
# │ │ │ │ │                                   7 is also Sunday on some systems)
# │ │ │ │ │
# │ │ │ │ │
# * * * * * command to execut
```

#### Helper Function - Get list of current jobs
cronpi has a helper function named "get_job_list" which will retrive the the job items in list.
```python
cronpi.get_job_list()
```



## Release information
### Nov 12th, 2019 (ver@2.0.0)
* restructured the library format so that it is more human readable.
```python
    cronpi.run_every_month("/some/command")
        .on([10,20], time="1:30AM")
```

### Nov 7th, 2019 (ver@1.0.0)
* released first version