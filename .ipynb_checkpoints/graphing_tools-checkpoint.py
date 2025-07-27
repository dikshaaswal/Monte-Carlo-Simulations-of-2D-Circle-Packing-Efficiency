import matplotlib.pyplot as plt
def plot_circles(sheet_width, sheet_length, allocated_circles):
    # Step 1: Plot the circles
    plt.figure(figsize=(5, 5))
    for _, row in allocated_circles.iterrows():
        x, y, r = row['x'], row['y'], row['radius']
        circle = plt.Circle((x, y), r, fill=True, edgecolor='black', linewidth=0.5)
        plt.gca().add_patch(circle)
    
    # Step 2: Adjust plot settings
    plt.xlim(0, sheet_width)
    plt.ylim(0, sheet_length)
    plt.gca().set_aspect('equal')
    plt.title('Allocated Circles')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def plot_distribution(min_diameter, max_diameter, df):
    # Step 2: Compute diameters from radius
    df['diameter'] = df['radius'] * 2
    
    # Step 3: Plot the histogram of diameters
    plt.figure(figsize=(10, 4))
    plt.hist(df['diameter'], bins=range(min_diameter, max_diameter), color='skyblue', edgecolor='black')  # bin size = 1
    plt.title('Histogram of Allocated Circle Diameters')
    plt.xlabel('Diameter')
    plt.ylabel('Frequency')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()