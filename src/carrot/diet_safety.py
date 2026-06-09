import polars as pl
import os


class DietSafetyManager:
    def __init__(self, csv_path="animals.csv"):
        """Initializes the manager and loads the dataset."""
        # Dynamic path handling to support both local and Colab environments
        if not os.path.exists(csv_path) and os.path.exists(f"repo-1/{csv_path}"):
            csv_path = f"repo-1/{csv_path}"

        self.df = pl.read_csv(csv_path)


    def get_relationship(self, animal_name):
        """Returns whether an animal can eat you, you can eat it, or both."""
        # 1. Filter using Polars syntax
        match = self.df.filter(pl.col("animal").str.to_lowercase() == animal_name.lower())

        # 2. Check if the dataframe is empty
        if match.is_empty():
            return f"Unknown animal: {animal_name}"

        # 3. Grab the first row's values using Polars item() or row extraction
        can_eat_me = match["can_eat_me"][0]
        i_can_eat_it = match["i_can_eat_it"][0]

        if can_eat_me and i_can_eat_it:
            return "Both: Mutual danger dinner."
        elif can_eat_me:
            return "The animal eats you. Avoid."
        elif i_can_eat_it:
            return "You eat the animal. Safe to hunt."
        else:
            return "Peaceful coexistence (neither eats the other)."


    def list_by_category(self, category):
        """Lists animals based on the category: 'me', 'animal', or 'both'."""
        # Make sure polars is imported at the top of your file as pl
        import polars as pl 

        if category == 'animal':
            # It eats me, I don't eat it
            filtered = self.df.filter(
                pl.col('can_eat_me') & ~pl.col('i_can_eat_it')
            )
        elif category == 'me':
            # I eat it, it doesn't eat me
            filtered = self.df.filter(
                ~pl.col('can_eat_me') & pl.col('i_can_eat_it')
            )
        elif category == 'both':
            # We eat each other
            filtered = self.df.filter(
                pl.col('can_eat_me') & pl.col('i_can_eat_it')
            )
        else:
            return "Invalid category. Choose 'me', 'animal', or 'both'."
            
        # Polars uses .to_list() instead of Pandas' .tolist()
        return filtered['animal'].to_list() 
