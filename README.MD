# Essensliste

This tool is intended to help you find food intollerances.
For each day you can list the food you ate as well as the potential symptoms you had.

The tool then tries to help you find out what kind of food is generally good and what might cause issues.
To do this the tool analyses the food and the symptoms with 1 day delay between each (configurable in `calcview.py` as `FOOD_TO_ILLNESS_OFFSET`).
Additionally the tool tries to determine combinations of foods that might cause issues.

Note: This tool is hacked together for my own usecase (that why it also has random german or english names).
It was not built with general usage in mind, but maybe it can still help.

## License

The Software is licensed under the [GNU General Public License v3](LICENSE.MD)