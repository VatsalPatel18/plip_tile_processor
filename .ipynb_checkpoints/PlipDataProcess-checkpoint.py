import os
import random
import torch
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

class PlipDataProcess(torch.utils.data.Dataset):
    def __init__(self, root_dir, files, df, img_processor=None, num_tiles_per_patient=128, max_workers=64, save_dir='processed_tile_data'):
        self.root_dir = root_dir
        self.files = files
        self.df = df
        self.img_processor = img_processor
        self.num_tiles_per_patient = num_tiles_per_patient
        self.max_workers = max_workers
        self.save_dir = save_dir
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def __len__(self):
        return len(self.files)

    def load_and_process_image(self, tile_path):
        image = Image.open(tile_path)
        return self.img_processor.preprocess(image)['pixel_values']

    def save_individual_tile_data(self, tile_data, file_data, file_name, tile_name):
        save_path = os.path.join(self.save_dir, file_name, f"{tile_name}.pt")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        torch.save({'tile_data': tile_data, 'file_data': file_data}, save_path)

    def __getitem__(self, idx):
        file = self.files[idx]
        tiles_path = os.path.join(self.root_dir, file,)
        tiles = [tile for tile in os.listdir(tiles_path) if tile != '.ipynb_checkpoints']
        selected_tiles = random.sample(tiles, min(self.num_tiles_per_patient, len(tiles)))

        #file_data = torch.tensor(self.df.loc[f'{file}-01'].values, dtype=torch.float32)
        
        try:
            file_data = torch.tensor(self.df.loc[f'{file}-01'].values, dtype=torch.float32)
        except KeyError:
            # If the file is not found in the dataframe, create a tensor of zeros
            # Shape is inferred from the other rows in the dataframe
            num_features = self.df.shape[1]
            file_data = torch.zeros(num_features, dtype=torch.float32)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for tile_name in selected_tiles:
                tile_path = os.path.join(tiles_path, tile_name)
                executor.submit(self.process_and_save_tile, tile_path, file_data, file, tile_name)

        return idx

    def process_and_save_tile(self, tile_path, file_data, file_name, tile_name):
        tile_data = self.load_and_process_image(tile_path)
        self.save_individual_tile_data(tile_data, file_data, file_name, tile_name)
