import pandas as pd
import re

def transurv(hist_url, mach_url):
    # read csv
    history = pd.read_csv(hist_url)
    machine = pd.read_csv(mach_url, sep=';')
    # drop irrelevant value in history
    history = history[['nama_detail', 'nomor_wo_repair', 'status_wo', 'waktu_pengajuan_servis', 'nama_kerusakan', 'deskripsi_bebas', 'jenis_failure', 'penyebab_masalah', 'penyelesaian']]
    history = history[history['nama_detail'].str.contains('Filling')]
    history = history[history['nama_kerusakan'].str.contains('FFT', flags=re.IGNORECASE, regex=True) == False]
    history = history[history['nama_kerusakan'].str.contains('PMO', flags=re.IGNORECASE, regex=True) == False]
    history = history[history['nama_kerusakan'].str.contains('PdM', flags=re.IGNORECASE, regex=True) == False]
    history = history[history['nama_kerusakan'].str.contains('inspeksi', flags=re.IGNORECASE, regex=True) == False]
    history = history[history['deskripsi_bebas'].str.contains('FFT', flags=re.IGNORECASE, regex=True) == False]
    history = history[history['deskripsi_bebas'].str.contains('PMO', flags=re.IGNORECASE, regex=True) == False]
    history = history[history['penyebab_masalah'].str.contains('FFT', flags=re.IGNORECASE, regex=True) == False]
    history = history[history['nama_kerusakan'] != 'Maintenance']
    history = history[history['nama_kerusakan'].str.contains('roject', flags=re.IGNORECASE, regex=True) == False]
    history = history[history['deskripsi_bebas'].str.contains('roject', flags=re.IGNORECASE, regex=True) == False]
    history['waktu_pengajuan_servis'] = pd.to_datetime(history['waktu_pengajuan_servis'])
    history = history.sort_values(['nama_detail', 'waktu_pengajuan_servis'], ascending=True)
    history.reset_index(drop=True, inplace=True)
    history = pd.concat([history['nama_detail'], history['waktu_pengajuan_servis'].dt.date, history['jenis_failure']], axis=1, keys=['id', 'date', 'fail_type'])
    history.loc[:, 'event'] = 1
    history.loc[:, 'date'] = pd.to_datetime(history.loc[:, 'date'])
    # save to check
    writer = pd.ExcelWriter('output/history.xlsx')
    history.to_excel(writer, 'history')
    writer.save()
    # machine-datasets
    machine.loc[:, 'date'] = pd.to_datetime(machine.loc[:, 'date'])
    # merge to create time-to-failure
    ttf = pd.merge(machine, history, on=['id', 'date'], how='left')
    ttf = ttf[['id', 'name', 'date', 'runhour', 'event', 'fail_type']]
    ttf.loc[:, 'event'] = ttf.loc[:, 'event'].fillna(0)
    ttf.loc[:, 'event'] = ttf.loc[:, 'event'].astype(int)
    # filter
    group = ttf.groupby('name')[['runhour']].sum().reset_index()
    group = group[group['runhour'] != 0].copy()
    ttf_ = pd.DataFrame(columns=['id', 'name', 'date', 'runhour', 'event', 'fail_type'])
    for i in group['name']:
        subs = ttf[ttf['name'] == i].copy()
        ttf_ = ttf_.append(subs)
    ttf_.reset_index(inplace=True, drop=True)
    ttf = ttf_.copy()
    # runhour cummulative
    nevent = 0
    for i in range(1, len(ttf.index)):
        if ttf.loc[i, 'id'] != ttf.loc[i-1, 'id']:
            nevent = 0
        else:
            nevent = nevent + ttf.loc[i, 'event']
            if (nevent == 1) & (ttf.loc[i, 'event'] == 1):
                cum = 0
                ttf.at[i, 'runhour_cum'] = cum
            elif (nevent != 0) & (ttf.loc[i, 'event'] == 0):
                cum = cum + ttf.loc[i, 'runhour']
                ttf.at[i, 'runhour_cum'] = cum
            elif (nevent > 1) & (ttf.loc[i, 'event'] == 1):
                cum = cum + ttf.loc[i, 'runhour']
                ttf.at[i, 'runhour_cum'] = cum
                cum = 0
    # to get last line for each id
    for i in range(0, len(ttf.index)-1):
        if ttf.loc[i, 'id'] != ttf.loc[i+1, 'id']:
            ttf.at[i, 'remark'] = 1
    ttf.loc[len(ttf.index)-1, 'remark'] = 1
    ttf = ttf[(ttf['event'] == 1) | (ttf['remark'] == 1)]
    ttf = ttf[['id', 'name', 'runhour_cum', 'event', 'fail_type']]
    ttf = ttf[ttf['runhour_cum'] != 0]
    ttf.loc[:, 'runhour_cum'] = ttf.loc[:, 'runhour_cum'].fillna(0)
    ttf.loc[:, 'runhour_cum'] = ttf.loc[:, 'runhour_cum'] / 60.0
    ttf.reset_index(drop=True, inplace=True)
    ttf.loc[:, 'event'] = ttf.loc[:, 'event'].astype(int)
    ttf.loc[:, 'fail_type'] = ttf.loc[:, 'fail_type'].fillna('nofail')
    return ttf