# import pandas as pd

# url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRPXb95bJwkasGpfTh8FHjhmegHyVqbVl446N08hm1BvThmDCxpxzjdZFB5FsAHxTf_46W_oGbGPB-m/pub?gid=274270331&single=true&output=csv"

# df = pd.read_csv(url)
# df.iloc[:,0] = pd.to_datetime(df.iloc[:,0])
# print(df.head())


from pyppeteer import chromium_downloader

chromium_downloader.download_chromium()
print("Chromium download complete!")
