# PyJaipur

Please follow the [Code of Conduct](https://www.python.org/psf/conduct/) at all times.

This repo is used to:
- Organize talk schedules using [the talk project](https://github.com/PyJaipur/PyJaipur/projects/1).
- Organize volunteer tasks using [the volunteer tasks project](https://github.com/PyJaipur/PyJaipur/projects/2).
- Have code based discussions in [the scratch folder](https://github.com/PyJaipur/PyJaipur/tree/master/scratch).
- Manage the pyjaipur.org website [source code](https://github.com/PyJaipur/PyJaipur/tree/master/website).
- Manage pyjaipur [assets which are used for events/meetups etc](https://github.com/PyJaipur/PyJaipur/tree/master/website/src/images/assets).


## Local setup for repo

```bash
git clone https://github.com/<your own fork>/PyJaipur
git remote add pyj https://github.com/PyJaipur/PyJaipur

# if you want to use python-poetry
poetry install
poetry shell

# if you want to use vanilla virtualenv
virtualenv -p python3 .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

# To submit changes
# make your changes. Then
git add <files you changed>
git commit -m 'small description of your change'
git push origin master
# now open a Pull request to pyjaipur/master

# To sync your master with pyjaipur
git fetch pyj
git checkout master
git reset --hard pyj/master
git push origin master -f
```


Changes to this repo are done as follows:
    - Fork this repo.
    - Make your changes in your copy of the fork.
    - Submit a PR to the master branch.
    - Await discussion / review and then merge. 
    - Sync your repo's master to pyjaipur master

## If you want to

- Ask a question on telegram/ask for mentoring. Please go through the following articles when you have time:
    - https://www.dontasktoask.com
    - http://www.catb.org/~esr/faqs/smart-questions.html
- [Submit a proposal for a talk](https://github.com/PyJaipur/Talks/issues/new?template=new_talk.md)
- [Propose a new event](https://github.com/PyJaipur/Talks/issues/new?template=new_event.md)
- [Make changes to pyjaipur.org](https://github.com/PyJaipur/PyJaipur/blob/master/website/README.md)
- [See talk rankings, most :+1: first](https://github.com/PyJaipur/PyJaipur/issues?utf8=%E2%9C%93&q=is%3Aopen+label%3Aupcoming+label%3Atalks+sort%3Areactions-%2B1-desc)
- Photos and videos can be found under the event dates on [this google drive folder](https://drive.google.com/drive/folders/1cuZ9h7VYSXlJUYMALhBK62STvgoXMLn3?usp=sharing)
- Ask some questions regarding your code:
    - Add your code to the scratch folder.
    - Open a pull request
    - Or upload your code to gist.github.com



## Announcing events on all social platforms

```bash
$ python -m announce --new
  Year (2020):
  Month (5):6
  Date: 27
  Event title (June meetup):
  Start time (11:00:00):
  Short description (TBD):
  Created events/2020/6/27/text.txt for description. Please fill it up
  Copy monthly meetup poster as poster for this event? (Y/n)
  Created symlink to monthly meetup poster for this event
  To announce this event please use:
       python -m announce --event events/2020/6/27 --announce

$ vim events/2020/6/27/text.txt  # To edit the description of the event.
# Things can now be submitted in a PR for review. After reviewing we can announce on all social platforms.
$ python -m announce --event events/2020/6/27 --announce
```
