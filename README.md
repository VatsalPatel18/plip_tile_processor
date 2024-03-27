# PLIP Tile Processor

This project processes whole slide images (WSI) and generates tiles using the `PlipDataProcess` class.

## Getting Started

These instructions will cover usage information and for the Docker container as well as running the script directly.

### Prerequisites

- Docker
- Python 3.8 or later
- Git

### Clone the Repository

To get started, clone this repository to your local machine:

```bash
git clone git@github.com:VatsalPatel18/plip_tile_processor.git
cd plip_tile_processor
```

### Using Docker

Building thte Docker Image

```bash
docker build -t plip_processor:latest .
```
Running the Docker Container

```bash
docker run -v /path/to/data:/data plip_processor:latest python ./process_tiles.py --csv_file /data/standardized.p4.scores.csv --root_dir /data/temp_data --save_dir /data/temp_out
```
Replace /path/to/data with the actual path to your data directory on your host machine.

### Running the Script Directly
If you prefer to run the script directly without Docker, follow these steps:

Setup
Ensure you have Python installed and then set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install Dependencies
Install the required Python packages:

```bash
pip install -r requirements.txt
```

Running the Script
Run the script with the required arguments:

```bash
python process_tiles.py --csv_file standardized.p4.scores.csv --root_dir temp_data --save_dir temp_out
```
Adjust the paths to the csv_file, root_dir, and save_dir as necessary.
Empty csv_file can be parsed, given that we are only looking for the model to predict not retrain.

### Additional Information
The Docker container runs as a non-root user by default for security reasons.

Ensure that the data volumes mounted in Docker have the correct permissions for the container to access and write the data.

Make sure to remove the placeholder text `/path/to/data` with the actual paths and filenames relevant to your project. Also, update the script parameters and file paths as per the actual usage in your project.



