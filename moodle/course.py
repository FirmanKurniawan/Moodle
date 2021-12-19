from moodle.moodleLogin import moodle
import requests
from moodle import SEMID
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


class course(moodle):
    def get_course(self):
        payload = {"perpage": "50"}
        r = self.session.get(
            f"http://moodle.mec.ac.in/course/index.php?categoryid={SEMID}",
            params=payload,
        )
        soup = BeautifulSoup(r.text, "html.parser")
        soup = soup.find("div", attrs={"class": "course_category_tree clearfix"})
        course_url_list = [
            url["href"]
            for url in soup.select(
                'a[href^="http://moodle.mec.ac.in/course/view.php?id="]'
            )
        ]
        return course_url_list

    def get_course_name(self, curl):
        r = self.reqUrl(curl)
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.h1.string

    def set_course_list(self, courselist):
        for url in courselist:
            r = self.session.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            r = self.reqUrl(url)
            if url == r.url:
                self.courses.update({soup.h1.string: url})
        return self.courses
