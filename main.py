from requests import Session
from bs4 import BeautifulSoup
import urllib3
import pwinput
import os
import sys
import re

# disable urllib3 warning
urllib3.disable_warnings()

# clear screen
os.system("clear")

# urls
url = {
  "base": "https://siakad-unsrit.aistech.id",
  "login": "https://siakad-unsrit.aistech.id/auth/login",
  "dashboard": "https://siakad-unsrit.aistech.id/dashboard",
  "profile": "https://siakad-unsrit.aistech.id/profile",
  "khs": "https://siakad-unsrit.aistech.id/khsmahasiswa"
}

class Siakad:

  def __init__(self) -> None:
    self.r = Session()
    self.source = self.r.get(url["base"], verify=False)

  def get_token(self) -> str:
    token_soup = BeautifulSoup(self.source.text, "html.parser")
    token = token_soup.find("input", attrs={"name": "_token"})
    return token["value"]

  def login(self, username: str, password: str) -> None:
    token = self.get_token()
    payload = {"_token": token, "username": username, "password": password}
    login_r= self.r.post(url["login"], data=payload)
    login_soup = BeautifulSoup(login_r.text, "html.parser")
    if login_soup.find("title").get_text() == "Dashboard":
      return True
    return False
  
  def user(self) -> str:
    user_r = self.r.get(url["profile"])
    user_soup = BeautifulSoup(user_r.text, "html.parser")
    form_group = user_soup.find("div", attrs={"class": "form-group"})
    user_fullname = form_group.find("input", attrs={"class": "form-control"})
    return user_fullname["value"]

  def khs(self) -> None:
    print(f"[PROCESS] mencari link KHS ...\n")
    ksh_r = self.r.get(url["khs"])
    khs_soup = BeautifulSoup(ksh_r.text, "html.parser")
    cards = khs_soup.find_all("div", attrs={"class": "row p-t-10 p-b-10"})
    pattern = r"bukajendela\(\'(.*)\'\)"
    jumlah = 0
    for i, card in enumerate(cards):
      anchor = card.find("a")["onclick"]
      result = re.findall(pattern, anchor)[0]
      print(f"[>] semester {i+1} : {result}\n")
      jumlah += 1
    print(f"[DONE] berhasil mendapatkan {jumlah} link KHS :)\n")

  def main(self, username: str, password: str) -> None:
    login = self.login(username, password)
    if login:
      print(f"\n[SUCCESS] login berhasil ({self.user()})")
      self.khs()
    else:
      print("[FAIL] login gagal :(")
      sys.exit(1)

if __name__ == "__main__":
  siakad = Siakad()
  username = input("[?] username atau NIM : ")
  password = pwinput.pwinput("[?] password : ", mask="*")
  siakad.main(username, password)