# AWOS (Automated Weather Observing System) Generator

Query the current weather from AviationWeather.gov and generate a fake AWOS report.

## Building and running
- Build: `docker build -t rorpage/awos .`
- Run: `docker run -e ICAO=KPDX rorpage/awos > output.mp3`

The environment variable for which airport (ICAO code) isn't required and defaults to `KIND`.
