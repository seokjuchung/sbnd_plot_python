# example_mpl.py
#
# Demonstration of SBND plot style using Matplotlib.
# Requires: numpy, scipy

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import multivariate_normal
import sbnd_style as sbnd_style # Applies the style automatically

def gauss(x, A, mu, sigma):
    """A simple Gaussian function for fitting."""
    return A * np.exp(-(x - mu)**2 / (2. * sigma**2))

def gauss_hists(n_hists=len(sbnd_style.SBND_COLOR_CYCLE)):
    """Generates a list of Gaussian-distributed data arrays."""
    datasets = []
    for i in range(n_hists):
        mean = 2 * i - (n_hists - 1)
        data = np.random.normal(loc=mean, scale=1.0, size=1000 * (i + 1))
        datasets.append(data)
    return datasets

def one_d_hist_example():
    """Demonstrates a simple 1D histogram with data points."""
    fig, ax = plt.subplots()
    
    mc_data = np.random.normal(loc=0, scale=1, size=1000)
    data_data = np.random.normal(loc=0, scale=1, size=1000)

    # MC Histogram (as a hatched area)
    ax.hist(mc_data, bins=20, range=(-5, 5), density=False, histtype='step',
            linewidth=2, color=sbnd_style.OKABE_ITO_BLUE,
            label='MC', hatch='////', fill=True, ec=sbnd_style.OKABE_ITO_BLUE)

    # Data points with error bars
    counts, bin_edges = np.histogram(data_data, bins=20, range=(-5, 5))
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    ax.errorbar(bin_centers, counts, yerr=np.sqrt(counts), fmt='o',
                color='black', label='Data', capsize=0)
    
    ax.set_xlabel("x label")
    ax.set_ylabel("y label")
    ax.set_ylim(bottom=0)
    ax.legend()
    sbnd_style.wip(ax)
    
    fig.tight_layout()
    fig.savefig("example_mpl_hist1D.png")
    plt.close(fig)

def data_mc_example():
    """Demonstrates a data/MC comparison with a ratio plot."""
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True,
                                   gridspec_kw={'height_ratios': [3, 1]})
    
    # Generate data and bin it
    data = np.random.normal(loc=0, scale=1, size=1000)
    counts, bin_edges = np.histogram(data, bins=40, range=(-5, 5))
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    y_err = np.sqrt(counts)

    # --- Top Pad: Data and Fit ---
    popt, _ = curve_fit(gauss, bin_centers, counts, p0=[np.max(counts), 0, 1])
    fit_y = gauss(bin_centers, *popt)
    
    ax1.errorbar(bin_centers, counts, yerr=y_err, fmt='o', color='black', label='Data')
    ax1.plot(bin_centers, fit_y, color=sbnd_style.OKABE_ITO_VERMILION, label='Fit')
    ax1.set_ylabel("y label")
    ax1.legend()
    sbnd_style.preliminary(ax1)

    # --- Bottom Pad: Ratio Plot ---
    # Avoid division by zero
    ratio = np.divide(counts - fit_y, fit_y, out=np.zeros_like(fit_y), where=fit_y!=0)
    ratio_err = np.divide(y_err, fit_y, out=np.zeros_like(fit_y), where=fit_y!=0)
    ax2.errorbar(bin_centers, ratio, yerr=ratio_err, fmt='o', color='black')
    ax2.axhline(0, color=sbnd_style.OKABE_ITO_VERMILION, linestyle='-')
    ax2.set_xlabel("x label")
    ax2.set_ylabel("(Data-Fit)/Fit")
    ax2.set_ylim(-1, 1)

    fig.tight_layout()
    plt.subplots_adjust(hspace=0.1) # Reduce space between plots
    fig.savefig("example_mpl_datamc.png")
    plt.close(fig)

def two_d_example():
    """Demonstrates a 2D histogram with contours."""
    fig, ax = plt.subplots()
    
    # Generate 2D correlated Gaussian data
    mean = [0, 0]
    cov = [[2, -1.5], [-1.5, 3]]
    data = np.random.multivariate_normal(mean, cov, size=500000)
    
    # Create the 2D histogram
    counts, xedges, yedges = np.histogram2d(data[:, 0], data[:, 1],
                                            bins=(100, 120), range=[[-5, 5], [-5, 7]])
    
    # Use pcolormesh for display
    im = ax.pcolormesh(xedges, yedges, counts.T, cmap=sbnd_style.SEA_PALETTE, rasterized=True)
    fig.colorbar(im, ax=ax, label='Counts')
    
    # Add contours
    total = np.sum(counts)
    sorted_counts = np.sort(counts.flatten())[::-1]
    cum_counts = np.cumsum(sorted_counts)
    levels_dict = {
        '1σ (68%)': sorted_counts[np.searchsorted(cum_counts, 0.682 * total)],
        '2σ (95%)': sorted_counts[np.searchsorted(cum_counts, 0.954 * total)],
        '3σ (99%)': sorted_counts[np.searchsorted(cum_counts, 0.997 * total)],
    }
    
    # FIX: Sort levels to be increasing, and match colors/styles
    contour_levels = sorted(list(levels_dict.values()))
    contour_colors = [sbnd_style.OKABE_ITO_YELLOW, sbnd_style.OKABE_ITO_ORANGE, sbnd_style.OKABE_ITO_RED_PURPLE]
    contour_styles = ['dotted', 'dashed', 'solid']
    
    ax.contour(counts.T, extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
               levels=contour_levels,
               colors=contour_colors,
               linestyles=contour_styles)

    ax.set_xlabel("x label")
    ax.set_ylabel("y label")
    sbnd_style.official(ax)
    
    fig.tight_layout()
    fig.savefig("example_mpl_hist2D.png")
    plt.close(fig)

def cov_example():
    """Demonstrates a symmetric (covariance) matrix plot."""
    fig, ax = plt.subplots()
    
    # Create a symmetric matrix
    dim = 10
    rng = np.random.default_rng(0)
    cov_matrix = np.eye(dim)
    off_diag = rng.normal(loc=0, scale=0.2, size=(dim, dim))
    off_diag = (off_diag + off_diag.T) / 2
    np.fill_diagonal(off_diag, 0)
    cov_matrix += off_diag
    cov_matrix = np.clip(cov_matrix, -1, 1)

    im = ax.imshow(cov_matrix, cmap=sbnd_style.SYMMETRIC_PALETTE, vmin=-1, vmax=1)
    fig.colorbar(im, ax=ax, label='Correlation')
    ax.set_xlabel("index i")
    ax.set_ylabel("index j")
    sbnd_style.preliminary(ax)
    
    fig.tight_layout()
    fig.savefig("example_mpl_histcov.png")
    plt.close(fig)

def stacked_example(datasets):
    """Demonstrates a stacked histogram plot."""
    fig, ax = plt.subplots()
    
    labels = [f"Hist #{i+1}" for i in range(len(datasets))]
    
    # FIX: Use a slice that results in 8 colors for 8 datasets.
    # This now includes the first color (black) from the style's color cycle.
    colors = sbnd_style.SBND_COLOR_CYCLE[:len(datasets)]

    ax.hist(datasets, bins=50, range=(-15, 15), stacked=True,
            label=labels, color=colors)

    ax.set_xlabel("x label")
    ax.set_ylabel("y label")
    ax.legend(loc='upper right')
    sbnd_style.wip(ax)

    fig.tight_layout()
    fig.savefig("example_mpl_histstacked.png")
    plt.close(fig)
    
def overlay_example(datasets):
    """Demonstrates an overlay of multiple histograms."""
    fig, ax = plt.subplots()
    
    for i, data in enumerate(datasets):
        ax.hist(data, bins=50, range=(-15, 15), histtype='step',
                linewidth=2.5, label=f"Hist #{i+1}")

    ax.set_xlabel("x label")
    ax.set_ylabel("y label")
    ax.legend(loc='upper right')
    sbnd_style.wip(ax)
    
    fig.tight_layout()
    fig.savefig("example_mpl_histoverlay.png")
    plt.close(fig)

def main():
    """Main function to generate all example plots."""
    print("🎨 Generating Matplotlib plots with SBND style...")
    one_d_hist_example()
    data_mc_example()
    two_d_example()
    cov_example()

    datasets = gauss_hists()
    stacked_example(datasets)
    overlay_example(datasets)
    print("✅ All plots saved as .png files.")

if __name__ == "__main__":
    main()