import colorsys
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

# https://stackoverflow.com/questions/876853/generating-color-ranges-in-python
def get_N_HexCol(N=5):
    HSV_tuples = [(x * 1.0 / N, 0.5, 0.5) for x in range(N)]
    hex_out = []
    for rgb in HSV_tuples:
        rgb = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(*rgb))
        hex_out.append('#%02x%02x%02x' % tuple(rgb))
    return hex_out

def get_cluster(X, nclust):
    silhouette_avg = [] 
    clabels = []
    for num_clusters in range(2,nclust):
        km = KMeans(n_clusters=num_clusters,
                    n_init=10,                        # number of iterations with different seeds
                    random_state=1                    # fixes the seed 
                   )
        cluster_labels = km.fit_predict(X)
        clabels.append(cluster_labels)
        # The silhouette_score gives the average value for all the samples.
        # This gives a perspective into the density and separation of the formed
        # clusters
        silhouette_avg.append(silhouette_score(X, cluster_labels))
    return {'silhouette_avg': silhouette_avg, 'cluster_labels': clabels }

def get_caccuracy(clusters, gnps, metac, method='mean'):
    caccuracy = []
    for clabel in clusters['cluster_labels']:
        gnps['clabel'] = clabel 
        g = gnps.groupby(['clabel']) 
        if method=='mean':
            caccuracy.append(g.apply(lambda a: max(Counter(a[metac]).values())/len(a) ).mean())
        elif method=='median':
            caccuracy.append(g.apply(lambda a: max(Counter(a[metac]).values())/len(a) ).median())
        gnps.drop(['clabel'], axis=1, inplace=True) 
    daccurary = {}
    daccurary['maxSilhoutte'] = max(clusters['silhouette_avg']) 
    daccurary['maxSilhoutteN'] = np.where(np.array(clusters['silhouette_avg'])==daccurary['maxSilhoutte'])[0][0]+2
    daccurary['maxCaccuracy'] = max(caccuracy) 
    maxCaccuracyPos = np.where(np.array(caccuracy)==daccurary['maxCaccuracy'])[0][0]
    daccurary['maxCaccuracySilhoutte'] = clusters['silhouette_avg'][maxCaccuracyPos]
    daccurary['maxCaccuracyN'] = maxCaccuracyPos+2
    return daccurary 

def plot_silhouette(X, n_clusters, silhouette_avg, lpar, show=True):
    # Create a subplot with 1 row and 2 columns
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(18, 7)
    # The 1st subplot is the silhouette plot
    # The silhouette coefficient can range from -1, 1 but in this example all
    # lie within [-0.1, 1]
    ax1.set_xlim([-0.1, 1])
    # The (n_clusters+1)*10 is for inserting blank space between silhouette
    # plots of individual clusters, to demarcate them clearly.
    ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])
    # Initialize the clusterer with n_clusters value and a random generator
    # seed of 10 for reproducibility.
    clusterer = KMeans(n_clusters=n_clusters, random_state=10)
    cluster_labels = clusterer.fit_predict(X)
    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed
    # clusters
    # Compute the silhouette scores for each sample
    sample_silhouette_values = silhouette_samples(X, cluster_labels)
    y_lower = 10
    for i in range(n_clusters):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = \
            sample_silhouette_values[cluster_labels == i]
        ith_cluster_silhouette_values.sort()
        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i
        color = cm.nipy_spectral(float(i) / n_clusters)
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)
        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples
    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")
    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")
    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])
    # 2nd Plot showing the actual clusters formed
    colors = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)
    ax2.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7,
                c=colors, edgecolor='k')
    # Labeling the clusters
    centers = clusterer.cluster_centers_
    # Draw white circles at cluster centers
    ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
                c="white", alpha=1, s=200, edgecolor='k')
    for i, c in enumerate(centers):
        ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
                    s=50, edgecolor='k')
    ax2.set_title("The visualization of the clustered data.")
    ax2.set_xlabel("Feature space for the 1st feature")
    ax2.set_ylabel("Feature space for the 2nd feature")
    plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
                  "with n_clusters = %d" % n_clusters + '\n'+
		  "n_iter=%d, perplexity=%d, learning_rate=%d" % lpar),
                 fontsize=14, fontweight='bold')
    if show:
        plt.show()
    else:
        return [fig, ax1, ax2]


