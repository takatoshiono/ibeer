#!/bin/sh
./tools/bulkload_client.py --filename data/status.csv --kind Status --url http://localhost:8080/test/load/status --cookie='dev_appserver_login="test@example.com:True"'
./tools/bulkload_client.py --filename data/total_amount.csv --kind TotalAmount --url http://localhost:8080/test/load/total_amount --cookie='dev_appserver_login="test@example.com:True"'
