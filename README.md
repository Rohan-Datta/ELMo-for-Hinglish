# ELMo for Hinglish

This repo contains code and data for training ELMo embeddings on Hinglish data. 
[bilm-tf](https://github.com/allenai/bilm-tf) is the implementation that is used for training the embeddings and then, validating the results.

## Steps to replicate
* Clone the implementation repo and install its requirements.
* Clone this repo and make suitable changes to the config.py file.
* Preprocess your data using data_preparation.py. You can also transliterate *Devanagari* text to Latin using devanagari_to_latin.py.
* Finally, train a model on your data using bilm-tf's script.