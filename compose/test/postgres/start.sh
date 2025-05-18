#! /usr/bin/env bash

psql -d nebusfinance_test_db -U debug -c "CREATE EXTENSION postgis;"
