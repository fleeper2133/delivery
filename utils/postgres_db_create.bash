#!/usr/bin/env bash
sudo -u postgres psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
    CREATE DATABASE delivery_db;
    CREATE USER delivery_user WITH PASSWORD 'password';
    ALTER ROLE delivery_user SET client_encoding TO 'utf8';
    ALTER ROLE delivery_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE delivery_user SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE delivery_db TO delivery_user;
    ALTER USER delivery_user CREATEDB;
EOSQL
