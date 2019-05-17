import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
import os
from os.path import join

def surv_curve(T, E, list, df):
    kmf = KaplanMeierFitter()
    fig = plt.figure(figsize=(15,20))

    for c, num in zip(list, range(1, df['name'].nunique())):
        ix = df['name'] == c
        ax = fig.add_subplot(6,4,num)
        kmf.fit(T[ix], E[ix], label=c)
        kmf.plot(ax=ax, legend=False)
        ax.set_title(c)
        ax.set_xlabel('runhour')
        ax.axhline(y=0.5, color='r', linestyle='dashed')
    
    plt.tight_layout()
    plt.show()

def surv_curve_wg(value):
    from scripts.transform_dataset import transurv

    history = join(os.path.dirname(os.getcwd()), 'Survival Analysis', 'datasets', 'filling_event.csv')
    machine = join(os.path.dirname(os.getcwd()), 'Survival Analysis', 'datasets', 'machine.csv')
    ttf = transurv(hist_url=history, mach_url=machine)
    
    ttf_ad = ttf[ttf['name'] == value]
    T = ttf_ad['runhour_cum']
    E = ttf_ad['event']

    fail_name = ttf_ad['fail_type'].unique()

    kmf = KaplanMeierFitter()
    fig = plt.figure(figsize=(15,20))

    for c, num in zip(fail_name, range(1, ttf_ad['fail_type'].nunique())):
        ix = ttf_ad['fail_type'] == c
        ax = fig.add_subplot(5,3, num)
        kmf.fit(T[ix], E[ix], label=c)
        kmf.plot(ax=ax, legend=False)
        ax.set_title(c)
        ax.set_xlabel('runhour')
        ax.axhline(y=0.5, color='r', linestyle='dashed')
    
    plt.tight_layout()
    plt.show()