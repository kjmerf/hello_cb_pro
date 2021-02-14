library(dplyr)
library(lubridate)
library(qcc)
library(urca)
library(forecast)

df <- read.csv('/tmp/bitcoin.csv')
df$hour <- hour(ymd_hms(df$iso_time))
df$date <- date(ymd_hms(df$iso_time))

daily <- df %>% filter(hour == 17)
plot(close ~ date, data = daily)
T <- nrow(daily)

auto.arima(log(daily$close))


log_diffs <- log(daily$close[2:T]) - log(daily$close[1:(T-1)])
plot(log_diffs)
acf(log_diffs)



diff_df <- data.frame(dt = daily$date[2:T], t = 2:T, log_diff = log_diffs)
summary(ur.df(y=diff_df$log_diff, type = "drift", lags=1))




# Try taking out the 4 largest points
diff_df %>% arrange(desc(abs(log_diff))) %>% head()
#diff_df <- diff_df %>% filter(!(t %in% c(143, 144, 196, 178)))

auto.arima(diff_df$log_diff)
qcc(diff_df$log_diff, type = 'xbar.one')

mean(diff_df$log_diff)
exp(mean(diff_df$log_diff)) ^ T

loess_level <- loess(log_diff ~ t, data = diff_df)
diff_df$level_hat <- predict(loess_level)
plot(log_diff ~ t, data = diff_df)
points(level_hat ~ t, data = diff_df, cex=.5, col = 'blue')

diff_df$sq_dev <- (diff_df$log_diff - diff_df$level_hat) ^ 2
loess_var <- loess(sq_dev ~ t, data = diff_df)
diff_df$var_hat <- predict(loess_var)

plot(sq_dev ~ t, data = diff_df)
points(var_hat ~ t, data = diff_df, cex=.5, col = 'blue')

plot(level_hat ~ dt, data = diff_df)




