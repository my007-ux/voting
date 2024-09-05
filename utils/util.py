import io
import re
import hashlib
from datetime import datetime, timedelta
from PIL import Image
import subprocess


def md5(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()


def last_month_regex():
    today = datetime.today()
    return re.compile((today.replace(day=1) - timedelta(days=1)).strftime('%Y-%m-'))


def last_day_regex():
    today = datetime.today()
    return re.compile((today - timedelta(days=1)).strftime('%Y-%m-%sd'))


def validate_page_number(page):
    try:
        return abs(int(page))

    except ValueError:
        return 1




# from django.http import StreamingHttpResponse

# def some_view(request):
#     file = open("large_file.mp4", "rb")
#     response = StreamingHttpResponse(file)
#     response['Content-Type'] = 'video/mp4'
#     return response

# from django.http import FileResponse

# def some_view(request):
#     file = open("example.pdf", "rb")
#     response = FileResponse(file)
#     response['Content-Type'] = 'application/pdf'
#     return response

# import ftplib
# from django.http import FileResponse

# def some_view(request):
#     ftp = ftplib.FTP("ftp.example.com")
#     ftp.login("username", "password")
#     ftp.cwd("/path/to/file")
#     file = io.BytesIO()
#     ftp.retrbinary("RETR file.pdf", file.write)
#     ftp.quit()
#     file.seek(0)
#     response = FileResponse(file)
#     response['Content-Type'] = 'application/pdf'
#     return response
