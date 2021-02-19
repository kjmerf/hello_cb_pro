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
