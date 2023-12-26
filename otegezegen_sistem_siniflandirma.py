import pandas as pd
import matplotlib.pyplot as plt

def classify_all_planetary_systems(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Initialize counters for different system types
    ordered_count = 0
    mixed_count = 0
    anti_ordered_count = 0
    similar_count = 0
    single_planet_count = 0  # Initialize count for single planet systems

    # Iterate through unique host names
    for host_name in df['star_name'].unique():
        # Filter rows for the current host_name
        system_data = df[df['star_name'] == host_name]

        # Sort the planets by radius
        sorted_planets = system_data.sort_values(by='radius')

        # Check the ordering of radii
        if any(sorted_planets['radius'].diff().dropna() > 0):
            ordered_count += 1
        elif any(sorted_planets['radius'].diff().dropna() < 0):
            anti_ordered_count += 1
        elif sorted_planets['radius'].nunique() == 1:
            if len(sorted_planets) == 1:
                single_planet_count += 1  # Count as single planet system
            else:
                similar_count += 1
        else:
            mixed_count += 1

    # Create a data frame for the counts
    counts_df = pd.DataFrame({
        'System Type': ['Ordered', 'Anti-ordered', 'Similar', 'Mixed', 'Single Planet'],
        'Count': [ordered_count, anti_ordered_count, similar_count, mixed_count, single_planet_count]
    })

    # Create a column graph
    counts_df.plot(kind='bar', x='System Type', y='Count', legend=False)
    plt.title('Distribution of Planetary System Types')
    plt.xlabel('System Type')
    plt.ylabel('Count')
    plt.show()

    return counts_df

# Example usage
file_path_input = "C:\\Users\\Ömer Yiğit Kavas\\Downloads\\exoplanet.eu_catalog.csv"
result_df = classify_all_planetary_systems(file_path_input)
print(result_df)
