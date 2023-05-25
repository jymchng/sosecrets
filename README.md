# .readthedocs.yaml
# Read the Docs configuration file
# See https://docs.readthedocs.io/en/stable/config-file/v2.html for details

# Required
version: 2

# Set the version of Python and other tools you might need
build:
  os: ubuntu-22.04
  tools:
    python: "3.8"

mkdocs:
  configuration: mkdocs.yml
  fail_on_warning: false

  # Explicitly set the version of Python and its requirements
python:
  install:
    - requirements: docs/requirements.txt