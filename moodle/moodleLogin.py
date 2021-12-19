import requests
from bs4 import BeautifulSoup
from moodle import log, RED, ENDC, TOTAL_COURSE
from urllib.parse import urlparse, parse_qs
from moodle import USERNAME, PASSWORD


class moodle(object):
    def __init__(self):
        self.tcount = 0
        self.tcourse = TOTAL_COURSE
        self.session = requests.session()
        self.loginUrl = "http://moodle.mec.ac.in/login/index.php"
        self.dashboard = None
        self.courses = {}

    def login(self):
        payload = {
            "anchor": "",
            "logintoken": "",
            "username": USERNAME,
            "password": PASSWORD,
            "rememberusername": "0",
        }
        headers = {
            "Host": "moodle.mec.ac.in",
            "Origin": "http://moodle.mec.ac.in",
            "Referer": "http://moodle.mec.ac.in/login/index.php",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        }
        try:
            r = self.session.get(self.loginUrl, headers=headers, timeout=4)
            payload["logintoken"] = self.get_input_token(r, "logintoken")
            self.dashboard = self.session.post(self.loginUrl, data=payload)
        except Exception as err:
            log.error(f"{RED} Error Connecting to server..! \n ERROR:{err} {ENDC}")
            return False
        else:
            try:
                log.info(f"Logged in to {self.get_profile_link()[1]} account")
            except Exception:
                log.error(f"{RED} Invalid credential unable to login {ENDC}")
                return False
            else:
                return True

    def get_input_token(self, response, findstring):
        soup = BeautifulSoup(response.text, "html.parser")
        token = soup.find("input", attrs={"name": findstring})["value"]
        return token

    def get_profile_link(self):
        soup = BeautifulSoup(self.dashboard.text, "html.parser")
        link = soup.find("a", attrs={"aria-labelledby": "actionmenuaction-2"})["href"]
        profile = self.session.get(link)
        soup = BeautifulSoup(profile.text, "html.parser")
        return link, soup.h1.string

    def reqUrl(self, url):
        if self.dashboard.url == self.session.get(self.dashboard.url).url:
            r = self.session.get(url)
            return r
        else:
            log.info("Your current login session ended, staring new one")
            self.login()
            r = self.session.get(url)
            return r
