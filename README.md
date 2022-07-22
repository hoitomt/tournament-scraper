# Tournament scraper

## Build image

```
docker build -t tournament-scraper:latest .
```

## Development

1. Run the container `./run.sh`
1. Do development from within the container

## Example Commands

- Get events with a filter

```json
{
    "StateRegion":"Wisconsin",
    "StartDateString":"4/1/2022",
    "EndDateString":"7/5/2022",
    "Gender":"2",
    "EventType":"Tournament",
    "SearchToken":"",
    "InviteType":"-1",
    "Page":1,
    "sportType":"1"
}
```

```shell
# Returns JSON
curl -XPOST \
-H "Content-Type: application/json" \
-H "Accept: application/json" \
-H "X-Requested-With: XMLHttpRequest" \
"https://basketball.exposureevents.com/youth-basketball-events" -d @payload.json
```
