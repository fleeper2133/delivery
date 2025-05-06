#!/usr/bin/env bash
sudo -u postgres psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
    DROP DATABASE IF EXISTS delivery_db;
    DROP DATABASE IF EXISTS test_delivery_db;
    DROP USER IF EXISTS delivery_user;
    DROP USER IF EXISTS test_delivery_db;
EOSQL
