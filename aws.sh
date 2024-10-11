#!/bin/bash
LOG_GROUP_NAME=/aws/ecs/scp-alpha-ecs
POLL_INTERVAL=10

declare -A LOG_STREAM_TOKENS

# Function to fetch log events for a specific log stream
fetch_log_events() {
  local LOG_STREAM_NAME=$1
  local NEXT_TOKEN=${LOG_STREAM_TOKENS[$LOG_STREAM_NAME]}

  if [ -z "$NEXT_TOKEN" ]; then
    NEXT_TOKEN="null"
  fi

  while true; do
    if [ "$NEXT_TOKEN" = "null" ]; then
      RESPONSE=$(aws logs   get-log-events --log-group-name "$LOG_GROUP_NAME" --log-stream-name "$LOG_STREAM_NAME" --limit 10 --profile sohail --region us-east-1)
    else
      RESPONSE=$(aws logs  get-log-events --log-group-name "$LOG_GROUP_NAME" --log-stream-name "$LOG_STREAM_NAME" --next-token "$NEXT_TOKEN" --limit 10 --profile sohail --region us-east-1)
    fi

    echo "$RESPONSE" | jq -r --arg STREAM_NAME "$LOG_STREAM_NAME" '.events[] | "\($STREAM_NAME): \(.message)"'

    NEW_TOKEN=$(echo "$RESPONSE" | jq -r '.nextForwardToken')

    # Break if no new log events
    if [ "$NEXT_TOKEN" = "$NEW_TOKEN" ]; then
      break
    fi

    NEXT_TOKEN=$NEW_TOKEN

    sleep 1
  done
}

trap "echo 'Ctrl+C detected. Gracefully exiting...'; exit 0" INT
while true; do
  echo "Polling for new log streams"
# Fetch the list of log streams
LOG_STREAMS=$(aws logs describe-log-streams --region us-east-1 --profile sohail --log-group-name /aws/ecs/scp-alpha-ecs | jq -r '.logStreams[].logStreamName')

# Tail logs from all streams in parallel
  for LOG_STREAM in $LOG_STREAMS; do
    fetch_log_events "$LOG_STREAM" &
  done

  wait
  sleep $POLL_INTERVAL
done
