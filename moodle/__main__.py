from moodle import log, ENDC, GREEN, WARNING, START_TIME, END_TIME, CYAN, RED
from urllib.parse import urlparse, parse_qs
from moodle.attendence import attendence
from moodle.telegrambot import send
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
import schedule, time
import requests

format = "%I:%M:%S"


def banner():
    """
    Banner
    """
    print(
        f"{CYAN} ██████   ██████                       █████ ████           \n \
░░██████ ██████                       ░░███ ░░███          \n \
 ░███░█████░███   ██████   ██████   ███████  ░███   ██████ \n \
 ░███░░███ ░███  ███░░███ ███░░███ ███░░███  ░███  ███░░███\n \
 ░███ ░░░  ░███ ░███ ░███░███ ░███░███ ░███  ░███ ░███████ \n \
 ░███      ░███ ░███ ░███░███ ░███░███ ░███  ░███ ░███░░░  \n \
 █████     █████░░██████ ░░██████ ░░████████ █████░░██████ \n \
░░░░░     ░░░░░  ░░░░░░   ░░░░░░   ░░░░░░░░ ░░░░░  ░░░░░░  {ENDC}"
    )


def loophour():
    schedule.every(30).minutes.until(END_TIME).do(check)


def check():
    now_utc = datetime.now(timezone("UTC"))
    now_asia = now_utc.astimezone(timezone("Asia/Kolkata"))
    log.info(
        f"{WARNING}{now_asia.strftime(format)} : Attendence checking for all Courses{ENDC}\n\n"
    )
    k = 1
    while k <= 4:
        for name, url in m.set_course_list(m.get_course()).items():
            m.mark_attedence(m.get_attendence_url(url)[0], name)
        if m.tcount == m.tcourse:
            k += 1
            m.tcount = 0
            now_utc = datetime.now(timezone("UTC"))
            now_asia = now_utc.astimezone(timezone("Asia/Kolkata"))
            log.info(
                f"{now_asia.strftime(format)} : All classes don't have attendence now!"
            )
            if k == 4:
                send("No classes found now , please check manually")
                break
            log.info(f"Waiting,{3*k} minutes to  check again\n\n")
            time.sleep(180)
            log.info(f"Checking attendence again, after {3*k} minutes")
        else:
            m.tcount = 0
            break


if __name__ == "__main__":
    banner()
    m = attendence()
    if m.login():
        log.info(f"{GREEN}Moodle Session Started{ENDC}")
    else:
        log.error(f"{RED}Unable to login check the credential, or sever is down{ENDC}")
        exit()
    log.info(f"Attedence checking for all course ")
    if not schedule.get_jobs():
        try:
            log.debug(schedule.every(30).minutes.until(END_TIME).do(check))
        except Exception:
            log.error("30 minute scheduler stoped, no class after 3.30")
    log.debug(schedule.every().monday.at(START_TIME).do(loophour))
    log.debug(schedule.every().tuesday.at(START_TIME).do(loophour))
    log.debug(schedule.every().wednesday.at(START_TIME).do(loophour))
    log.debug(schedule.every().thursday.at(START_TIME).do(loophour))
    log.debug(schedule.every().friday.at(START_TIME).do(loophour))
    check()
    while True:
        schedule.run_pending()
        time.sleep(1)
