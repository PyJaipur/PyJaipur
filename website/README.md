# Website

- All code is contained in `src` folder.
- We use the [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) template system.
- All files which start with `.` are ignored. For example `src/.base.html`.
- All files which don't start with `.` are rendered.

# How to run website on local.
 - you need to install staticsite `pip install staticsite`.
- from this folder build site using  `python -m staticsite build`. in local you will also have to set baseurl in staticsite.yaml equals to '/docs'.
- run `python -m http.server` to run it. 

Please make changes in your own fork and submit a PR.
