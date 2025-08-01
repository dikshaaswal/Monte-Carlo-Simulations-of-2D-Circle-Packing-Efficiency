# Function to sample from a truncated normal distribution
# Step 1: Generate initial diameters from normal distribution (no truncation yet)
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from collections import defaultdict

# Generate diameters from normal distribution and round to nearest int( because bin size = 1)
def generate_diameters(n, mean_diameter, std_diameter):
    np.random.seed(42)
    return np.random.normal(loc=mean_diameter, scale=std_diameter, size=n).astype(int)

# Check if a new circle overlaps with any existing circle
def is_overlapping(new_circle, existing_circles):
    x1, y1, r1 = new_circle
    for x2, y2, r2 in existing_circles:
        dist_sq = (x1 - x2)**2 + (y1 - y2)**2
        min_dist = (r1 + r2)**2
        if dist_sq < min_dist:
            return True
    return False

def place_circles_bc1(truncated_diameters, total_skips, max_attempts, sheet_width, sheet_height):
    allocated_circles = []
    attempts_dict = defaultdict(int)
    np.random.seed(42)
    total_tries = 0
    while total_tries < total_skips:
        diameter = np.random.choice(truncated_diameters)
        attempts = 0
        
        while attempts < max_attempts:  
          radius = diameter / 2
          x = int(np.random.uniform(radius, sheet_width - radius))
          y = int(np.random.uniform(radius, sheet_height - radius))
          new_circle = (x, y, radius)
          if not is_overlapping(new_circle, allocated_circles):
              allocated_circles.append(new_circle)
              attempts_dict[attempts] += 1 
              break
               
          attempts += 1
        if attempts == max_attempts:
          total_tries += 1
          print(f"❌ Skipped a circle after {max_attempts} attempts. Skip count: {total_tries}")

    return allocated_circles, attempts_dict



def place_circles_bc1_kdtree(truncated_diameters, total_skips, max_attempts, sheet_width, sheet_height):
    allocated_circles = []  # ← same as original
    centers = []            # (x, y) coordinates for KDTree
    radii = []              # to keep corresponding radii
    attempts_dict = defaultdict(int)
    
    np.random.seed(42)
    total_tries = 0
    tree = None  # KDTree object, starts empty

    while total_tries < total_skips:
        diameter = np.random.choice(truncated_diameters)
        attempts = 0

        while attempts < max_attempts:
            radius = diameter / 2
            x = np.random.uniform(radius, sheet_width - radius)
            y = np.random.uniform(radius, sheet_height - radius)
            new_center = [x, y]

            #Optimized Overlap Check
            if tree:
                # Query neighbors only within possible overlapping distance
                possible_idx = tree.query_ball_point(new_center, r=radius+(truncated_diameters.max())/2)
                overlap = False
                for idx in possible_idx:
                    x2, y2 = centers[idx]
                    r2 = radii[idx]
                    dist_sq = (x2 - x)**2 + (y2 - y)**2
                    if dist_sq < (radius + r2)**2:
                        overlap = True
                        break
                if overlap:
                    attempts += 1
                    continue

            # No overlap or first circle
            allocated_circles.append((x, y, radius))
            centers.append(new_center)
            radii.append(radius)
            tree = cKDTree(centers)  # 🛠 Rebuild tree after adding new circle
            attempts_dict[attempts] += 1
            break

        if attempts == max_attempts:
            total_tries += 1
            print(f"❌ Skipped a circle after {max_attempts} attempts. Skip count: {total_tries}")

    return allocated_circles, attempts_dict

###new condition for stopping criteria 
def place_circles_1(truncated_diameters,  max_attempts, sheet_width, sheet_height):
    allocated_circles = []
    attempts_dict = defaultdict(int)
    np.random.seed(42)
    total_tries = 0
    while True:
        diameter = np.random.choice(truncated_diameters)
        attempts = 0
        
        while attempts < max_attempts:  
          radius = diameter / 2
          x = int(np.random.uniform(radius, sheet_width - radius))
          y = int(np.random.uniform(radius, sheet_height - radius))
          new_circle = (x, y, radius)
          if not is_overlapping(new_circle, allocated_circles):
              allocated_circles.append(new_circle)
              attempts_dict[attempts] += 1 
              break
               
          attempts += 1
            
        if attempts == max_attempts:            
            total_tries += 1
            # return allocated_circles, attempts_dict, total_tries
            print(f"❌ Skipped a circle after {max_attempts} attempts. Skip count: {total_tries}")
        if (total_tries*100)/len(allocated_circles) > 1:
            return allocated_circles, attempts_dict, total_tries
        
        
    return allocated_circles, attempts_dict, total_tries

###new condition for stopping criteria  and grid bin size = 0.1
def place_circles_2(truncated_diameters,  max_attempts, sheet_width, sheet_height):
    print("new condition for stopping criteria  and grid bin size = 0.1")
    allocated_circles = []
    attempts_dict = defaultdict(int)
    np.random.seed(42)
    total_tries = 0
    while True:
        diameter = np.random.choice(truncated_diameters)
        attempts = 0
        
        while attempts < max_attempts:  
            radius = diameter / 2
            x = round(np.random.uniform(radius, sheet_width - radius), 1)
            y = round(np.random.uniform(radius, sheet_height - radius), 1)
            new_circle = (x, y, radius)
            if not is_overlapping(new_circle, allocated_circles):
              allocated_circles.append(new_circle)
              attempts_dict[attempts] += 1 
              break
               
            attempts += 1

        if attempts == max_attempts:            
            total_tries += 1
            # return allocated_circles, attempts_dict, total_tries
            print(f"❌ Skipped a circle after {max_attempts} attempts. Skip count: {total_tries}")
        if (total_tries*100)/len(allocated_circles) > 1:
            return allocated_circles, attempts_dict, total_tries
        
        
    return allocated_circles, attempts_dict, total_tries
    
    
def save_circles(df, filename):
    circle_df = pd.DataFrame(df, columns=['x', 'y', 'radius'])
    circle_df.to_csv(filename, index=False)


def save_attempts(df, filename):
    attempts_df = pd.DataFrame(list(df.items()), columns=['attempts', 'count'])
    attempts_df.sort_values(by='attempts', inplace=True)
    attempts_df.to_csv(filename, index=False)


def calculate_packing_efficiency(sheet_width, sheet_height, allocated_circles):

    # Step 1: Compute total sheet area
    sheet_area = sheet_width * sheet_height
    
    # Step 2: Compute total circle area
    allocated_circles['circle_area'] = np.pi * (allocated_circles['radius'] ** 2)
    total_circle_area = allocated_circles['circle_area'].sum()
    
    # Step 3: Compute packing efficiency
    packing_efficiency = total_circle_area / sheet_area
    return packing_efficiency
    


