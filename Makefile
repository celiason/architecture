# Get house image data 

# NB: .env enables MPS fallback for pytorch. This is necessary for the notebook to work


## PROJECT SETUP

PYTHON_INTERPRETER = python3



## DATA SETS

data:
	kaggle datasets download -d wwymak/architecture-dataset -o data/raw/architecture-dataset.zip
	unzip data/raw/architecture-dataset.zip


redfin:
	$(PYTHON_INTERPRETER) src/scrape.py

# download roads shape file
roads: data/raw/roads/
	curl https://apps.gisconsortium.org/giscsharedstorage/VOP/Streets.zip -o data/raw/Streets.zip
	unzip data/raw/Streets.zip -d data/raw/roads