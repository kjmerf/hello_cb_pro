update ods.candles o
set low = l.low
  , high = l.high
  , open = l.open
  , close = l.close
  , volume = l.volume
  , created_time = l.created_time
from (
	select *
		, row_number() over (partition by product_id, time order by created_time desc) as rn
	from landing.candles
	) l
where l.product_id = o.product_id
  and l.time = o.time
  and l.created_time > o.created_time
  and l.rn = 1;

insert into ods.candles
select l.product_id
  , l.time
  , l.low
  , l.high
  , l.open
  , l.close
  , l.volume
  , l.created_time
from (
	select *
		, row_number() over (partition by product_id, time order by created_time desc) as rn
	from landing.candles
	) l
left join ods.candles o on l.product_id = o.product_id and l.time = o.time
where o.product_id is null
  and l.rn = 1;
