-- Grant all privileges on all tables in the public schema to a user
-- makGRANT ALL PRIVILEGES ON DATABASE app_db TO postgres;

drop table if exists "account";
create table "account"
(
    id            serial,
    uuid          uuid unique not null,
    creation_date timestamp with time zone default current_timestamp,
    username      text not null,
    first_name    text not null,
    last_name     text not null,
    email         text not null,
    password      text not null,
    token         text
);

-- Optionally, grant other privileges like SELECT, INSERT, UPDATE, DELETE, etc.
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO <username>;
