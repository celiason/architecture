from sklearn.neighbors import NearestNeighbors
from scipy.interpolate import griddata
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import matplotlib.pyplot as plt

def mytest():
    print('testing 1.2.3!!!')


# pts = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
# plt.plot(*zip(*pts), marker='o', color='r', ls='')
# nbrs = NearestNeighbors(radius=2)
# nbrs.fit(pts)
# nbrs.radius_neighbors()
# nbrs.radius_neighbors_graph().astype(int).toarray()


# Count up the number of distinct houses in a given radius and return a dataframe
# 1 degree of latitude = 111 km
# assuming homes are 10 meters apart, 10/111000 = 0.00009 degrees
def find_unique(df, radius=0.0002, plot=False, stratify=True):

    # Initialize NearestNeighbors with the specified radius
    nbrs = NearestNeighbors(radius=radius)

    # Fit the model using latitude and longitude values for homes
    nbrs.fit(df[['latitude', 'longitude']].values)

    # Function to calc. number of unique home types in a given radius
    def count_unique_preds_in_radius(row, stratify=stratify):
        indices = nbrs.radius_neighbors([row[['latitude', 'longitude']]], return_distance=False)[0]
        if stratify:
            unique_predictions = df.iloc[indices]['prediction'].unique()
        else:
            unique_predictions = df.iloc[indices]
        return len(unique_predictions)

    # Now we can apply the function to each row in the data frame
    out = df.apply(count_unique_preds_in_radius, stratify=stratify, axis=1)

    # Optional plot (e.g., to check whether radius is suitable)
    if plot:
        out.hist()

    return out.values

# Function to calculate the inverse Simpson's index
# 1 - sum(p_i^2)
# where p_i is the proportion of homes of style i in the block
def simpson_index(x):
    # Calculate normalized proportions
    proportions = x.value_counts(normalize=True)
    # Calculate inverse Simpson's index
    simpson = 1 - sum(proportions**2)
    return simpson

# Function to find blocks from a road shapefile
def get_blocks(shapefile, plot=False):

    import osmnx as ox
    import geopandas as gpd
    import matplotlib.pyplot as plt
    from shapely.ops import polygonize
    import momepy

    map_df = gpd.read_file(shapefile)

    # Convert from meters to lat/long
    map_df = map_df.to_crs(epsg=4326)

    # Convert the GeoDataFrame to a networkx graph
    G = momepy.gdf_to_nx(map_df, approach="primal")
    G_undirected = G.to_undirected()
    G_edges_as_gdf = ox.graph_to_gdfs(G_undirected, nodes=False, edges=True)
    block_faces = list(polygonize(G_edges_as_gdf['geometry']))
    blocks = gpd.GeoDataFrame(geometry=block_faces)

    # Get size of blocks
    blocks['size'] = blocks.area
    
    if plot:
        blocks.plot(column='size', edgecolor='k', linewidth=2, alpha=0.5, zorder=1, legend=True, figsize=(10,10))

    return blocks

# Function to check if a given house is in a block
def assign_block(pt, blocks):
    from shapely.geometry import Point
    pt = Point(pt)
    contains = blocks.contains(pt)
    return contains[contains].index[0]

# Plotting the map
def plot_arch_map(df,
                  cols={'bungalow': '#003f5c', 'victorian': '#7a5195', 'prairie': '#ef5675', 'foursquare': '#ffa600'},
                  plot_title='Architecture Diversity', file_name=None, radius=0.0002, cmap='bone', heatmap=True, road_col="white"):

    # Import roads shape files as a GeoDataFrame
    map_df = gpd.read_file('data/raw/roads/Street_Centerlines.shp')

    # Convert from meters to lat/long
    map_df = map_df.to_crs(epsg=4326)

    # Assuming x, y, and z are already defined
    x = df['longitude'].values
    y = df['latitude'].values
    z = df['unique_homes_in_radius'].values

    # Define grid (resolution = 100)
    grid_x, grid_y = np.mgrid[min(x):max(x):100j, min(y):max(y):100j]

    # Interpolate using griddata
    grid_z = griddata((x, y), z, (grid_x, grid_y), method='cubic')

    fig, ax = plt.subplots(1, figsize=(10,14))

    if heatmap:
        # Plot the interpolated data
        plt.imshow(grid_z.T, extent=(min(x), max(x), min(y), max(y)), origin='lower', cmap=cmap, vmin=0, vmax=df['unique_homes_in_radius'].max())
        # Add a color bar
        cbar = plt.colorbar(label='Number of unique homes in a 30m radius', shrink=0.25)

    # Map predictions to categorical color values
    colors = df['prediction'].map(cols)

    # Add roads
    map_df.plot(ax=ax, color=road_col, linewidth=0.5, alpha=0.5)

    # Scatter plot with categorical colors of predicted home types
    plt.scatter(x, y, c=colors, edgecolors='w', linewidths=0.25, s=8)

    # Set title, axis labels
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title(plot_title)

    # Add a legend
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=label) 
            for label, color in cols.items()]
    plt.legend(handles=handles, title="House type")

    # Turn off the axis
    plt.axis('off')

    # Change the plot limits
    # plt.ylim(min(y), max(y))
    plt.ylim(min(y), 41.88)

    # Set aspect ratio to be equal
    plt.gca().set_aspect('equal', adjustable='box')

    # Save the plot
    if file_name:
        plt.savefig(file_name, dpi=300, bbox_inches='tight')
