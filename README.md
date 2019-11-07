# cronpi
A small tool for deploying crontab into a Linux System By using Python3.
> Install crontabs into the system if it's not installed.
This will override if the crontab with same command already exists in crontab

## Install
```bash
pip install cronpi
```

## Usage
Putting mouse over the function will show the detail information of that function. 
It shows 
1. description of the function
2. argument type and description
3. use cases

![title](https://raw.githubusercontent.com/dakc/cronpi/master/usage.png)

## functions
cronpi has following functions.
1. deploy_daily
2. deploy_monthly
3. deploy_yearly
4. deploy_minutely
5. deploy_by_weekday
6. deploy

From 1~5 the name of the function denote what they do. 6th deploy function will deploy the command which we write while editing crontab.

```python
cronpi.deploy("* * * * * sh /run/some/commands.sh")
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

## Below are the use cases for Running job Daily
### 1. Run daily at 0:00
```python
cronpi.deploy_daily("sh /some/command.sh")
```

### 2. Run daily at 5:00AM
```python
cronpi.deploy_daily("sh /some/command.sh", 5)
```

### 3. Run daily at 5:30AM
```python
cronpi.deploy_daily("sh /some/command.sh", 5, 30)
```


*For others put the mouse over the function and see detail.*


## Note
Only support in unix-like system, eg. Linux/Mac

## License
[MIT](./LICENSE)