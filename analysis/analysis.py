import pandas as pd
df = pd.read_json("/tmp/cb_pro.json", lines=True)
df.to_csv("/tmp/bitcoin.csv", index=True)
