import os
import pandas as pd
from PlipDataProcess import PlipDataProcess
from transformers import CLIPImageProcessor
import argparse

def main(csv_file, root_dir, save_dir):
    df4 = pd.read_csv(csv_file).set_index('PatientID')
    there = set(list(x[:-3] for x in df4.index))

    wsi_data = {}
    for file in os.listdir(root_dir):
        fol_p = os.path.join(root_dir, file)
        f2lp_t = len(os.listdir(fol_p))
        wsi_data[file] = f2lp_t

    wsi_there = set(wsi_data.keys())
    use = list(there.intersection(wsi_there))

    img_processor = CLIPImageProcessor.from_pretrained("./plip/")

    dataset = PlipDataProcess(
        root_dir=root_dir,
        files=use,
        df=df4,
        img_processor=img_processor,
        num_tiles_per_patient=2000,
        max_workers=64,
        save_dir=save_dir
    )

    for i in range(len(dataset)):
        _ = dataset[i] 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process WSI images and generate tiles")
    parser.add_argument('--csv_file', type=str, required=True, help='Path to the CSV file with patient scores')
    parser.add_argument('--root_dir', type=str, required=True, help='Root directory for WSI tiles')
    parser.add_argument('--save_dir', type=str, required=True, help='Directory to save the processed tile data')

    args = parser.parse_args()

    main(csv_file=args.csv_file, root_dir=args.root_dir, save_dir=args.save_dir)
