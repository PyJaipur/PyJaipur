# Website

- All code is contained in `src` folder.
- We use the [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) template system.
- All files which start with `.` are ignored. For example `src/.base.html`.
- All files which don't start with `.` are rendered.

# How to run website on local.

- You need to install staticsite `python -m pip install staticsite`.
- From this folder build site using  `python -m staticsite build`.
- Run `(cd www && python -m http.server)` to run a local server. 
- Visit http://localhost:8000 to see your local copy of the website.

Please make changes in your own fork and submit a PR.
