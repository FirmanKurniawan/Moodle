<h1 align= center>Moodle Auto-Attendence </h1>
<h3 align = center>Python script to mark moodle course attedence</h3>

### Heroku
<p><a href="https://heroku.com/deploy?template=https://github.com/4ndu-7h4k/MoodleAttendence"><img src="https://img.shields.io/badge/Deploy%20To%20Heroku-blueviolet?style=for-the-badge&logo=heroku" width="200""/></a></p>

## Deploy Locally or Server
```
git clone https://github.com/4ndu-7h4k/MoodleAttendence
cd MoodleAttendence
pip3 install -U -r requirements.txt
nano moodle/config.py
#Fill config with your values , set server = False if not using .env
cp sample.env .env
#Fill .env with values
python3 -m moodle
 ```
## Note
 This is a Dev branch, So you might experience bugs!
