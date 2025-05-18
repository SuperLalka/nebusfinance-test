#! /usr/bin/env bash

psql -d nebusfinance_db -U debug -c "CREATE EXTENSION postgis;"
