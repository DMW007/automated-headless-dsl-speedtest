# Automated headless DSL-Speedtests
Tired of slow internet connections? And also tired of doing manual speed tests day per day to analyze and proof your slow connection? Automate it! You just need a Linux PC or server with Python or Docker, and 2 Minutes of your time to measure internet speed!

[![](https://u-img.net/img/6277Zo.png)](https://u-img.net/img/6277Zo.png)

## Motivation
Slow internet connections are a wide spread and annoying problem. Especially when the speed is very low and/or used by multiple people. Most ISPs require you to make multiple speed tests on different days, at different times and so on, in order to exclude that it's a temprorary problem. Doing it manually is also annoying, because you have to start the test, wait until it's finished and document the result - multiple times. 

Another common issue is that some ISPs overloading their network. This may wouldn't be noticeable during the day, where no high usage is present because most of the people are at work. But at rush hours, e.g. in the evening, when most people stream largely videos, download updates and other stuff, it could slow down the thoughput massively. Such overselling is also hard to not so easy to prove, since you need to figure out when this happens and when not.

So why should we spend our time by doing such things manually? Its a waste of time and the manual data is of limited signification. Wouldn't it be better to execute speed tests automatically in a definied interval, having compareable data to see how good is our connection during the whole day? 

## Getting started
### General requirements
- A clon of this repo on the target machine
- Python 3
- Alternatively Docker

It's tested on Linux (Ubuntu/Debian), bot not on Windows. You could try it as well, if Python 3 is installed. 

### Docker
Per default, the included `docker-compose.yml` includes both cron and web container, which collects speed tests results every 15min. The web container runs on port 8081. You could adjust this to your environments and needs. For example, add labels to run it behind Traefik or any other reverse proxy.

```bash
docker-compose up --build -d
```

It takes a few seconds for the first speed test to complete. You could also see this in a log entry (`docker-compose logs -f`). The web ui should be avaliable on http://localhost:8081

### Manual
Install the required pip packages as shown in the Dockerfile: 

```bash
pip install speedtest-cli Jinja2 tzlocal python-dateutil
```

Make sure `python3` is linked to Python 3 or change the binary in `src/cron.sh`. Now execute our cron script to collect data:

```bash
cd src
INTERVAL_MIN=15 bash ./cron.sh
```

Of course, it makes sense to add this as a cron on linux, to have it running in the background - especially on headless servers. 

To start the webserver for the GUI, just execute

```bash
python3 src/web/web.py
```

## How it works
This project is split into two parts: 

### `speedtest.py`
The speedtest script executes [`speedtest-cli`](https://github.com/sivel/speedtest-cli), which itself is a CLI tool to run automated speed tests from [https://www.speedtest.net/](speedtest.net). It executes the test and gave us the determined download and upload speed with ping. Additionally, it store all three of them in a sqlite database for later analysis.

### `web.py`
To have a comfortable way of getting our collected data by `speedtest.py`, I build a small web ui. It shows you a graph with all collected download/upload speeds and the ping (see screenshot at the top of this readme). Detailled values could be taken from the table above. 

## Credits
This project uses several great open source project itself, which are the following: 

- [ApexCharts](https://apexcharts.com/)
- [Jinja2](https://jinja.palletsprojects.com/)
- [jQuery](https://jquery.com/)
- [Bootstrap](https://getbootstrap.com/)
- [SQLite](https://sqlite.org/index.html)
- [Python](https://www.python.org/)
- [speedtest-cli](https://github.com/sivel/speedtest-cli)