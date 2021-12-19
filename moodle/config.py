class loginData(object):
    server = True
    username = ""  # moodle login username or email
    password = ""  # moodle login password
    telgramtoken = ""  # telegram bot token from @botfather
    chatid = (
        ""  # Your unique telegram chat_id or @username (settings->copy id or username)
    )
    totalcourse = 8
    # Select your semester from http://moodle.mec.ac.in/course/index.php?categoryid=4,
    # then check url for semid  eg:moodle.mec/../categoryid=28( "28"categoryid is the semid)
    moodleSemId = "28"
    startTime = "02:01"  # IST 12 hour
    endTime = "10:00"  # IST 12 hour
