from moodle.course import course
from moodle import log, CYAN, ENDC
from moodle.telegrambot import send
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from pytz import timezone

format = "%I:%M:%S"


class attendence(course):
    def get_attendence_url(self, curl):
        """
        Returns attendence url from course page
        :params course url
        """
        r = self.reqUrl(curl)
        soup = BeautifulSoup(r.text, "html.parser")
        atturl = [
            aurl["href"]
            for aurl in soup.select(
                'a[href^="http://moodle.mec.ac.in/mod/attendance/view.php?id="]'
            )
        ]
        return atturl

    def mark_attedence(self, atturl, name):
        self.tcount += 1
        attpayload = {
            "sessid": "",
            "sesskey": "",
            "_qf__mod_attendance_form_studentattendance": "1",
            "mform_isexpanded_id_session": "1",
            "status": "",
            "submitbutton": "Save changes",
        }
        r = self.reqUrl(atturl)
        soup = BeautifulSoup(r.text, "html.parser")
        url = soup.select(
            'a[href^="http://moodle.mec.ac.in/mod/attendance/attendance.php?sessid="]'
        )
        if url and url[0].text == "Submit attendance":
            url_to_parse = url[0]["href"]
            query_string = urlparse(url_to_parse).query
            attpayload["status"] = self.get_present_id(url_to_parse)
            attpayload["sessid"] = parse_qs(query_string)["sessid"][0]
            attpayload["sesskey"] = [
                parse_qs(query_string)["sesskey"][0],
                parse_qs(query_string)["sesskey"][0],
            ]
            query_string = urlparse(atturl).query
            r = self.session.post(url_to_parse, data=attpayload)
            if r.url == atturl:
                now_utc = datetime.now(timezone("UTC"))
                now_asia = now_utc.astimezone(timezone("Asia/Kolkata"))
                self.tcount -= 1
                log.info(
                    f"{CYAN}{self.get_course_name(atturl)}  -> Attedence marked successfully  at {now_asia.strftime(format)}{ENDC}"
                )
                send(f"Attendence marked :{name} at {now_asia.strftime(format)}")
            else:
                log.error(f"Attendence marking failed -> {name}")
                send(f"Attendence marking failed -> {name}")
        else:
            now_utc = datetime.now(timezone("UTC"))
            now_asia = now_utc.astimezone(timezone("Asia/Kolkata"))
            log.info(
                f"{name} --> course don't have attedence at ({now_asia.strftime(format)})"
            )

    def get_present_id(self, url):
        r = self.reqUrl(url)
        soup = BeautifulSoup(r.text, "html.parser")
        child = soup.find("span", attrs={"class": "statusdesc"}).parent
        id = child.find("input")["value"]
        return id
