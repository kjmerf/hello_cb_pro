create schema if not exists landing;
create schema if not exists ods;
create table if not exists landing.candles
(
  product_id char(30),
  time int,
  low numeric,
  high numeric,
  open numeric,
  close numeric,
  volume numeric,
  created_time int
);
create table if not exists ods.candles
(
  product_id char(30),
  time int,
  low numeric,
  high numeric,
  open numeric,
  close numeric,
  volume numeric,
  created_time int
);
create unique index if not exists ods_candles_idx on ods.candles(product_id, time);

create table if not exists ods.balances
(
  profile_id char(36),
  as_of_time int,
  available numeric,
  balance numeric,
  currency char(3),
  created_time int
);

create table if not exists ods.transactions
(
  profile_id char(36),
  side varchar(4),
  usd numeric,
  btc numeric,
  fee numeric,
  created_time int
);

create table if not exists landing.ticker
(
  type char(100),
  trade_id bigint,
  sequence bigint,
  time timestamp,
  product_id char(30),
  price numeric,
  side char(30),
  last_size numeric,
  best_bid numeric,
  best_ask numeric,
  created_time timestamp
);
