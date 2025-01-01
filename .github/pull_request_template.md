(The lines in parentheses (like this one) are instructions for filling out this template. These lines can be deleted.)
(The lines in double curly brackets ({{}}) should be replaced as it describes.)
(You can open a PR to add or improve this template, if you find it lacking!)

(Choose one heading, or add your own.)
**CONTENT** (data addon)
**BALANCE**
**FEATURE**
**BUGFIX**
**DOCUMENTATION**
**WORKFLOW**
**UPDATE**
**REFACTOR**
**TWEAK**
**FIX**
**PROGRESS**

This PR addresses the bug/feature described in issue #{{insert number}}
This PR addresses the game progression goal #{{goal}}

## Summary
{{Describe and explain your changes. Include links to related issues.}}

## Screenshots
{{Include before and after screenshots demonstrating your changes, if applicable.}}

## Usage examples
{{If your changes affect how game data can be defined, provide examples demonstrating the changes here.}}

## Testing Done
{{Describe how you tested these changes. Ensure that new issues aren't introduced.}}
{{If this is a new feature, have you added any automated tests using the unit or integration testing framework?}}

## Testing Method
{{Provide detailed and concise method that the reviewers can use to test your changes.}}

## Save File
This save file can be used to test these changes:
{{Attach a save file that allows people to easily test your added mission content or see your new in-game art.}}

## Performance Impact
{{If this PR changed code, describe any performance impact (positive or negative). "N/A" if no performance-critical code is changed.}}

## Check-List
{{If this PR is in progress, write major actions that need to be done here.}}
- [ ] Review my own code
- [ ] Fix the workflow checks

{{If this PR is adding any artwork (ASCII art), that is yours or not, update the `copyright` file.}}
{{If this PR is adding any new attribute to a data type, please update the corresponding `schemas/` and data checks (check_yaml.py class and yaml data test workflow script).}}
{{If this PR drastically changes or adds any functions (by changing its parameters or its use) to the game engine (or a new class), please update the game engine's documentation at docs/ENGINE_FUNCTIONS.md}}
{{If this PR adds a new main command (or changes an existing one's key), make sure to update the `existing_keys` variable in both `.github/code_checks/run_yaml_data_tests.py` and `source/check_yaml.py` classes}}
