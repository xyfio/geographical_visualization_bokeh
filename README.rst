*************************************
Geographical visualization with bokeh
*************************************

**Installing the required packages**

.. code-block:: python

    pip install -r requirements.txt

- Note that plot does not update when user change slider value when running code in IDE/jupyter notebook
- For interactive mode, user need to set up a local Bokeh server or javascript callback


1. Open terminal/cmd window and cd into working directory 
2. Execute below code to launch local bokeh server

.. code-block:: python

    bokeh serve --show geographical_bokeh.py

`dataset: <https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide>`
`world map - countries <https://www.naturalearthdata.com/downloads/110m-cultural-vectors/>`
