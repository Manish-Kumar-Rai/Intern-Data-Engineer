import numpy as np
from scipy import stats
from math import sqrt
from numpy.linalg import lstsq

def series_stats(series):
    arr = np.array(series, dtype=float)
    return {
        "mean": float(np.nanmean(arr)),
        "std": float(np.nanstd(arr, ddof=1)) if arr.size>1 else 0.0,
        "median": float(np.nanmedian(arr)),
        "q1": float(np.nanpercentile(arr,25)),
        "q3": float(np.nanpercentile(arr,75)),
        "iqr": float(np.nanpercentile(arr,75) - np.nanpercentile(arr,25))
    }

def anomalies_iqr(series, k=1.5):
    s = np.array(series, dtype=float)
    q1, q3 = np.nanpercentile(s, [25,75])
    iqr = q3 - q1
    lo, hi = q1 - k*iqr, q3 + k*iqr
    return [{"i":int(i),"v":float(v)} for i,v in enumerate(s) if (v<lo or v>hi)]

def anomalies_zscore(series, thresh=3.0):
    s = np.array(series, dtype=float)
    if len(s)<=1: return []
    z = (s - np.nanmean(s))/np.nanstd(s, ddof=1)
    return [{"i":int(i),"v":float(s[i]), "z":float(z[i])} for i in range(len(s)) if abs(z[i])>thresh]

def moving_average(arr, w):
    a = np.array(arr, dtype=float)
    res = np.convolve(np.nan_to_num(a), np.ones(w),'full')[:len(a)]
    counts = np.convolve(~np.isnan(a), np.ones(w),'full')[:len(a)]
    with np.errstate(invalid='ignore'):
        return res / counts

def anomalies_ma_pct(series, window=7, pct=0.3):
    s = np.array(series, dtype=float)
    ma = moving_average(s, window)
    res=[]
    for i,v in enumerate(s):
        if np.isnan(ma[i]) or ma[i]==0: continue
        if abs(v - ma[i]) / abs(ma[i]) > pct:
            res.append({"i":i,"v":float(v),"ma":float(ma[i])})
    return res

def grubbs_test(series, alpha=0.05):
    s = list(series)
    n_total = len(s)
    indices = list(range(n_total))
    outliers=[]
    while len(s) > 2:
        arr = np.array(s, dtype=float)
        mean = arr.mean()
        sd = arr.std(ddof=1)
        if sd == 0: break
        deviations = np.abs(arr-mean)
        max_idx = int(np.argmax(deviations))
        G = deviations[max_idx] / sd
        n = len(arr)
        t = stats.t.ppf(1 - alpha/(2*n), n-2)
        Gcrit = ((n-1)/sqrt(n)) * sqrt(t*t / (n-2 + t*t))
        if G > Gcrit:
            outliers.append({"i": indices[max_idx], "v": float(arr[max_idx]), "G": float(G)})
            s.pop(max_idx)
            indices.pop(max_idx)
        else:
            break
    return outliers


def poly_fit(xs, ys, degree=1):
    x = np.vander(xs, N=degree+1, increasing=True)
    coeffs, *_ = lstsq(x, ys, rcond=None)
    return coeffs.tolist()

def poly_predict(coeffs, xs):
    xs = np.array(xs)
    deg = len(coeffs)-1
    vals = sum(coeffs[i] * xs**i for i in range(deg+1))
    return vals.tolist()
