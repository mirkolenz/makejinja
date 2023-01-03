# Dashboard Example for Home Assistant

This folder contains a fully working example for automatically generating a dashboard for Home Assistant.
Assuming you run `makejinja` inside this directory (`tests/data`), it can be run without any arguments as it will load its options from the `.makejinja.toml` file.

**Note:**
We adjust the default Jinja template delimiters so that there are no collisions with the Home Assistant template syntax.
This way, you can even automatically generate correct templates for sensors and other use cases.

The following files/folders are relevant:

- `.makejinja.toml`: Config file for makejinja invocation.
- `input`: Regular `yaml` config files together with `yaml.jinja` config templates (these are rendered by makejinja).
- `output`: Resulting directory tree after running makejinja with the command shown above.
- `config`: Folder containing a `yaml` file with variables used in our Jinja templates.
- `filters.py`: Custom Jinja filters to use in our templates.
- `globals.py`: Custom functions to use in our templates.
