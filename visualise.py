import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import os

# names = ['bingan_kwta', 'kwta', 'naive']

def dict2array(results):
    runs = len(results)
    tasks = len(results[0])
    array = np.zeros((runs, tasks, tasks))
    for run, dict_run in results.items():
        for e, (key, val) in enumerate(reversed(dict_run.items())):
            for e1, (k, v) in enumerate(reversed(val.items())):
                array[int(run), tasks - int(e1)-1, tasks -int(e)-1] = round(v, 1)
    return np.transpose((array),axes=(0,2,1))

def grid_plot(ax, array, exp_name):
    avg_array = np.around(np.mean(array, axis = 0), 1)
    num_tasks = array.shape[1]
    ax.imshow(avg_array, vmin=0, vmax=100)
    for i in range(len(avg_array)):
        for j in range(avg_array.shape[1]):
            if j >= i:
                ax.text(j,i, avg_array[i,j], va='center', ha='center', c='w', fontsize=90/num_tasks)
    ax.set_yticks(np.arange(num_tasks))
    ax.set_ylabel('Number of tasks')
    ax.set_xticks(np.arange(num_tasks))
    ax.set_xlabel('Tasks finished')
    ax.set_title(f"{exp_name} -- {np.round(np.mean(array[:, :, -1], axis=(0,1)), 2)} -- std {np.round(np.std(np.mean(array[:, :, -1], axis=1), axis=0), 2)}")

def acc_over_time_plot(ax, array):
    num_tasks = array.shape[1]
    acc_over_time = np.sum(array, axis=1)/np.arange(1, num_tasks+1)
    mean, std = np.mean(acc_over_time, axis=0), np.std(acc_over_time, axis=0) 
    ax.fill_between(np.arange(1, num_tasks+1), mean-std, mean + std, alpha=0.3)
    ax.plot(np.arange(1, num_tasks+1), mean)


def plot_final_results(names,rpath = 'results/'):
    fig = plt.figure(figsize=(13, 5*len(names)))
    gs = GridSpec(len(names), 3)

    for e, name in enumerate(names):
        acc_dict = np.load(f"{rpath}{name}/acc_val.npy", allow_pickle=True).item()
        arr = dict2array(acc_dict)
        ax1 = fig.add_subplot(gs[e, 0])
        ax2 = fig.add_subplot(gs[e, 1:])
        grid_plot(ax1, arr, name)
        acc_over_time_plot(ax2, arr)

    # plt.show()
    plt.savefig(rpath+names[0]+"/results_visualisation")

# names = ['FashionMNIST_test']
# plot_final_results(['CIFAR_10'])
    