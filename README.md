# CoCalc Assistant

A collection of code snippet examples to assist working on CoCalc → [read more](src/README.md).

![](cocalc-assistant.png)

## Development

The source files are in `/src` and are processed via the `examples.py` Python file.

Usually, just running `make` in the main directory is enough to see if the changes did work.

The output is a unified `examples.json` file, which can be used by other tools -- right now that's [CoCalc](https://cocalc.com).

## Submodule

When used as a **submodule**, one suitable magic git commands to update all submodules is

```
git submodule foreach "git fetch origin; git checkout master; git reset --hard origin/master"
```

## Acknowledgments

* [Boilerplate](https://github.com/moble/jupyter_boilerplate.git)

## Copyright

SageMath, Inc.

## License

Code: Apache 2.0

Data: 
[Creative Commons: Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/) (more detailed information is in the header of the files in `/src`)
