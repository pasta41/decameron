# BERTcaccio 1.0 project

This repository hosts the BERTcaccio project. Eventually, it will contain all relevant materials for downloading and using a [BERT](https://www.aclweb.org/anthology/N19-1423/)-style NLP language model for medieval Italian. 

The goal is to follow the procedure outlined in the [alBERTo paper](http://ceur-ws.org/Vol-2481/paper57.pdf), which creates a pre-trained BERT model on modern Italian on scraped Twitter data.

For now, this project contains rudimentary materials and dependencies for 1) downloading the Branca digital Decameron edition, 2) converting from XML to JSON format, 3) a tool for doing assisted comma numbering (this cannot be fully automated since there is no certain pattern), and 4) doing Gibbs-sampling-based LDA.

## Short-term planned work

In the short term, the goal is to see if it is possible to identify the gender of a narrator based on the text of a story.

Longer term, I would like to investigate if it is possible to predict the identity of the narrator. 

Both of these tasks will likely require building features that currently do not exist for medieval Italian, such as part-of-speech tagging. Ideally, there might be a simple way to eyeball correlating topics with gender or topics with narrator. This task will serve the basis of my final project for Italian 6450. 

## Longer-term planned work

Training BERTcaccio and open-sourcing it for broader digital humanities use. 

Building a tool that uses a modified grep to return text matches (with the surrounding comma, perhaps to be refactored to be more general later, and day/story/narrator metadata).


## Contributing
Pull requests are welcome. For major changes, please open an issue. 

## Notes

There is sometimes text that is marked as italicized or with foreign language metadata (always Latin). I have removed these tags because the text that contains it is formatted in a very odd way. The things to grep for in the original/ raw text are: @, #, text, foreign, lat, rend, block, canzonetta. 

## Citations

This work is possible due to Sapienza, Università di Roma's [Biblioteca italiana project](http://www.bibliotecaitaliana.it/). Currently, they host the Vittore Branca edition of the Decameron [here](http://backend.bibliotecaitaliana.it/wp-json/muruca-core/v1/xml/bibit000267). 

The overall digital catalog, which I will use to train BERTcaccio, can be found [here](http://www.bibliotecaitaliana.it/catalogo).
