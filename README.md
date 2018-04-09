# psistats2

psistats2 is a very basic, cross-platform tool to monitor your system's health. Out of the box it can report on several different types of information, as well as leveraging [lm-sensors](https://hwmon.wiki.kernel.org/lm_sensors "lm-sensors") (for Linux/Unix based systems) and [OpenHardwareMonitor](https://github.com/openhardwaremonitor/openhardwaremonitor "OpenHardwareMonitor") (for Windows based systems) to offer output from available hardware sensors.

This project is still in development.

## Features

1. Supports Linux, Unix, and Windows based systems. (not tested on OS X, your mileage may vary)
2. Different intervals for each report
3. Simple data points
4. Easily extensible

## Installation

psistats2 is still in development. These instructions are more for developers than end users.

```bash
$ git clone https://github.com/psistats/psistats2
$ virtualenv env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
(env) $ python psistats.py console
```

## Configuration
> TODO

You can edit psistats.conf to configure and tweak psistats2.

## Plugins

psistats2 is made up of two different types of plugins, reporters and outputters. Reporters generate reports and outputters send the reports to other places. psistats2 uses the framework [psireporter](https://github.com/alex-dow/psireporter "psireporter") to manage these plugins.

### Development
> TODO

### Reporting Plugins

| Plugin ID  | Description  |
| ------------ | ------------ |
| cpu_per_core  | Lists CPU usage percentages for each core  |
| cpu_total | Gives the total CPU usage as a percent, across all cores  |
| disk_usage | Gives the total and remaining disk space for each configured disk  | 
| ip_addr | Reports the IP addresses for each configured network interface  |
| memory  | Gives the total and remaining memory in bytes  |
| sensors | Reports the values of the configured sensors  |
| uptime | Reports the current uptime of the system in seconds  |

### Output Plugins

| Plugin ID | Description |
| ------------ | ------------ |
| stdio | Simply prints reports to stdout |
| logging | Logs each report based on the configuring in psistats.conf |
| amqp | Sends JSON reports to a RabbitMQ server |
| http | Posts JSON reports to an HTTP URL |

