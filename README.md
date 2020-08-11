# STIG-to-Inspec

Python script to parse STIG XML files from https://public.cyber.mil/stigs/downloads/ into Chef Inspec Ruby files for configuration compliance auditing. This project was created to save time creating brand new Chef Inspec checks for Configuration Complaiance Audits.

The script creates an individuals .rb file for each STIG item and pre-populates with a template containing the following information:
- Control Name
- Title
- Description
- Impact (Default 0.5)
- Check Text
- Fix Text

Usage: `python STIG-to-Inspec.py -f FILE_PATH_TO_STIG_XML`

The script is only intended for initial check creation. Running it again will overwrite any previously created scripts of the same name. Be Careful.
