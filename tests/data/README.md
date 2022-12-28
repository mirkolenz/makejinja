# Dashboard Example for Home Assistant

This folder contains a fully working example for automatically generating a dashboard for Home Assistant.
The app should be invoked as follows (assuming that you run it inside the `tests/data` folder):

`makejinja ./input ./output --data ./config --filters ./filters.py --globals ./globals.py`

It is composed of the following files/folders:

- `input`: Regular `yaml` config files together with `yaml.jinja` config templates (these are rendered by makejinja).
- `output`: Resulting directory tree after running makejinja with the command shown above.
- `config`: Folder containing a `yaml` file with variables used in our Jinja templates.
- `filters.py`: Custom Jinja filters to use in our templates.
- `globals.py`: Custom functions to use in our templates.
