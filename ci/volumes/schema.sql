-- Grant all privileges on all tables in the public schema to a user
-- GRANT ALL PRIVILEGES ON DATABASE app_db TO postgres;

drop table if exists "account";
create table "account"
(
    pk            serial,
    sk            uuid unique not null,
    creation_date timestamp with time zone default current_timestamp,
    username      text        not null,
    email         text        not null,
    password      text        not null,
    token         uuid
);

drop table if exists "message";
create table "message"
(
    pk            serial,
    sk            text unique not null,
    thread_id     text,
    creation_date timestamp with time zone default current_timestamp,
    posted_on     text        not null,
    author        text        not null,
    content       text        not null
);

-- Optionally, grant other privileges like SELECT, INSERT, UPDATE, DELETE, etc.
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO <username>;

drop table if exists "dataset";
create table "dataset"
(
    --pk              serial,
    buid            text unique not null,
    dataset_uid     text unique not null,
    dataset_id      text unique not null,
    title           text        not null,
    description     text        not null,
    publisher       text                ,
    created         text                ,
    updated         text                
    --created         timestamp with time zone default current_timestamp,
    --updated         timestamp with time zone default current_timestamp
);