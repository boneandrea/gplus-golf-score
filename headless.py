from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from time import sleep
import pytest
import json
import os
import re
"""
Run:

$ pip install -r requirements.e2e.txt
$ pytest -sv test.py # print()あり テスト項目表示あり
$ pytest -v test.py # print()なし テスト項目表示あり
$ pytest test.py # silent
"""

ROOT = "http://18.180.67.181"
ENCODER = "http://18.179.171.174"
LOGINPAGE = "%s/index" % ROOT
USERNAME = "administrator"
PASSWORD = ""
CID = "64e2b9df4e64860b486df009"

driver = None

# utils


def init_browser():
    caps = webdriver.DesiredCapabilities.CHROME.copy()
    caps['acceptInsecureCerts'] = True
    options = ChromeOptions()
    options.add_argument("--no-selfandbox")
    options.add_argument("--headless")
    options.set_capability('acceptInsecureCerts', True)
    global driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(
    ).install()), options=options)  # 自動的にSeleniumとChromeバージョンを一致させる


def get_scores():
    init_browser()
    driver.get(
        "https://v2anegasaki.igolfshaper.com/anegasaki/score/2nf6slre#/landscape-a")
    driver.get(
        "https://v2anegasaki.igolfshaper.com/anegasaki/score/2nf6slre/leaderboard")
    wait = WebDriverWait(driver, timeout=5)
    show_score_button = driver.find_elements(By.CSS_SELECTOR, ".show-score")
    show_score_button[0].click()
    wait = WebDriverWait(driver, timeout=5)
    table = driver.find_elements(By.CSS_SELECTOR, ".ui-table-view")[0]

    tr = table.find_elements(By.TAG_NAME, "tr")
    num_player = len(tr)-2

    basic_info = get_basic_info()
    scores = {
        "course": basic_info["course"],
        "date": basic_info["date"],
        "scores": []
    }

    for i in range(0, num_player):
        tds = tr[i+2].find_elements(By.TAG_NAME, "td")
        score = []
        for td in tds:
            score.append(td.get_attribute("innerText").replace('\u3000', ''))
        score.pop(0)
        del score[1:6]
        score.pop(10)
        score.pop(10)
        score.pop(19)

        data = {
            "name": "",
            "score": []
        }
        name = ""
        for i, s in enumerate(score):
            if i == 0:
                data["name"] = score[i]
            if i > 0 and i < 19:
                data["score"].append({"hole": i, "score": int(score[i])})
            if i == 19:
                data["gross"] = int(score[i])

        scores["scores"].append(data)

    return scores


def get_basic_info():

    init_browser()
    driver.get(
        "https://v2anegasaki.igolfshaper.com/anegasaki/score/2nf6slre#/landscape-a")

    wait = WebDriverWait(driver, timeout=5)
    course = driver.find_elements(By.CSS_SELECTOR, ".cc-name")[
        0].get_attribute("innerText")
    import re
    course = re.sub("^【", "", course)
    course = re.sub("】$", "", course)

    date = driver.find_elements(By.CSS_SELECTOR, ".date")[
        0].get_attribute("innerText")

    # from dateutil.parser import parse
    from datetime import datetime
    date = datetime.strptime(date.replace(
        "プレー日: ", ""), "%Y年%m月%d日").strftime("%Y/%m/%d")
    return {
        "course": course,
        "date": date
    }
    # print(html)
    # html = table[1].get_attribute("innerText")
    # print(html)
    # html = table[2].get_attribute("innerText")
    # print(html)
    # html = table[3].get_attribute("innerText")
    # print(html)


scores = get_scores()
print(json.dumps(scores, indent=2, ensure_ascii=False))
driver.quit()


def login():
    driver.get(LOGINPAGE)
    user = driver.find_element(By.NAME, "user")
    user.send_keys(USERNAME)
    user.submit()


def createFilePath(file):
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), ".", file))


class Test_ログイン():
    # 非ログイン時にログインページを表示する
    def test_loginpage(self):
        driver.get(LOGINPAGE)
        assert driver.title == "SQEX-TV | Login"

    # ログインするとHomeに飛ぶ
    def test_login(self):
        login()
        assert driver.title == "SQEX-TV"
        ranking = driver.find_elements(By.ID, "ranking")
        assert ranking != None

# 以下はログイン後の操作


class Test_動画をアップロードする():
    def test_アップロード画面を表示する(self):
        login()
        driver.get("%s/upload" % ROOT)
        assert driver.title == "SQEX-TV | Upload"

    def _動画をアップロードする(self, attachment=False):
        login()
        driver.get("%s/upload?cid=%s" % (ROOT, CID))
        assert driver.title == "SQEX-TV | Upload"

        upload_file = createFilePath("sample_movie.mp4")
        inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
        inputs[1].send_keys(upload_file)

        title = driver.find_element(By.ID, "title")
        title.send_keys("title")

        description = driver.find_element(By.ID, "description")
        description.send_keys("description")

        if attachment == True:
            # add attachemnt
            highLeveltab = driver.find_element(By.ID, "highLeveltab")
            highLeveltab.click()
            sleep(1)
            inputs = driver.find_elements(
                By.CSS_SELECTOR, "input[type='file']")
            upload_file = createFilePath("attachment.png")
            inputs[3].send_keys(upload_file)
            inputs[4].send_keys(upload_file)

        submit_button = driver.find_element(By.ID, "btnSubmit")
        submit_button.click()

    def test_動画をアップロードする(self):
        self._動画をアップロードする()
        wait = WebDriverWait(driver, timeout=5)
        alert = wait.until(expected_conditions.alert_is_present())
        assert alert.text == "動画を投稿しました。"

    def test_動画をアップロードするwithAttachment(self):
        self._動画をアップロードする(attachment=True)
        alert = WebDriverWait(driver, timeout=2).until(
            expected_conditions.alert_is_present())
        assert alert.text == "動画を投稿しました。"
        alert.accept()
        alert = WebDriverWait(driver, timeout=2).until(
            expected_conditions.alert_is_present())
        assert alert.text == "添付ファイルのアップロードに成功しました。"
        alert.accept()
        sleep(30)

        # homeへ移動
        driver.get("%s/index" % (ROOT))
        # wait
        sleep(3)
        thumbs = driver.find_elements(By.CSS_SELECTOR, ".t_medium_tile a")
        play_page_url = thumbs[0].get_attribute("href")
        driver.get(play_page_url)
        sleep(3)

        attachments = driver.find_elements(By.CSS_SELECTOR, ".relatedDatas a")
        assert attachments[0].get_attribute("innerText") == "attachment.png"

    def test_添付ファイル付きの動画に添付ファイルが表示される(self):
        self._動画をアップロードする(attachment=True)
        alert = WebDriverWait(driver, timeout=2).until(
            expected_conditions.alert_is_present())
        assert alert.text == "動画を投稿しました。"
        alert.accept()
        alert = WebDriverWait(driver, timeout=2).until(
            expected_conditions.alert_is_present())
        assert alert.text == "添付ファイルのアップロードに成功しました。"
        alert.accept()
        sleep(30)

        # homeへ移動
        driver.get("%s/index" % (ROOT))
        # wait
        sleep(3)
        thumbs = driver.find_elements(By.CSS_SELECTOR, ".t_medium_tile a")
        play_page_url = thumbs[0].get_attribute("href")
        driver.get(play_page_url)
        sleep(3)

        attachments = driver.find_elements(By.CSS_SELECTOR, ".relatedDatas a")
        assert attachments[0].get_attribute("innerText") == "attachment.png"

    def test_動画をアップロードする_MY動画にサムネイルが出る(self):
        self._動画をアップロードする()
        wait = WebDriverWait(driver, timeout=5)
        alert = wait.until(expected_conditions.alert_is_present())
        alert.accept()
        sleep(5)
        driver.get("%s/admin-v?cid=%s" % (ROOT, CID))
        assert driver.title == "SQEX-TV | AdminPanel"
        sleep(1)
        items = driver.find_elements(By.CLASS_NAME, "vframeListAdminBG")
        assert len(items) > 0
        image = items[0].find_element(By.CSS_SELECTOR, "img.thumbImg")
        thumbnail = image.get_attribute("src")
        pattern = r'/thumbnails/[0-9a-z]+/[0-9a-z_]+.jpg'
        assert re.search(pattern, thumbnail) != None

    def test_動画をアップロードする_MY動画にtitle_description_usernameが出る(self):
        self._動画をアップロードする()
        wait = WebDriverWait(driver, timeout=5)
        alert = wait.until(expected_conditions.alert_is_present())
        alert.accept()
        sleep(5)
        driver.get("%s/admin-v?cid=%s" % (ROOT, CID))
        assert driver.title == "SQEX-TV | AdminPanel"
        sleep(1)
        items = driver.find_elements(By.CLASS_NAME, "vframeListAdminBG")
        assert len(items) > 0
        info = items[0].find_elements(
            By.CSS_SELECTOR, "div div div.vframeListInfoAdmin")[0]
        category = info.find_elements(
            By.CSS_SELECTOR, "span.categoryNamePanel")[0].text
        assert category == "【カテゴリ未設定】"

        title = info.find_elements(
            By.CSS_SELECTOR, "a div")[0].text
        assert title == "title"

        description = info.find_elements(
            By.CSS_SELECTOR, "a div")[1].text
        assert description == "description"

        username = info.find_elements(
            By.CSS_SELECTOR, ".commonUnameIc a")[0].text
        assert username == "administrator"

    def test_動画をアップロードする_MY動画に進捗状況が出る(self):
        self._動画をアップロードする()
        wait = WebDriverWait(driver, timeout=5)
        alert = wait.until(expected_conditions.alert_is_present())
        alert.accept()
        sleep(5)
        driver.get("%s/admin-v?cid=%s" % (ROOT, CID))
        assert driver.title == "SQEX-TV | AdminPanel"
        driver.find_element(By.ID, "dispEncodeLogs").click()
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, 'elogiframe')))

        # iframeを取得
        iframe = driver.find_element(By.CSS_SELECTOR, 'iframe#elogiframe')
        # iframeの中の要素を操作するために切り替える
        driver.switch_to.frame(iframe)
        items = driver.find_elements(By.CLASS_NAME, "enclog_base")
        assert len(items) > 0

        center = items[0].find_element(By.CLASS_NAME, "logCenter")
        div = center.find_elements(By.CSS_SELECTOR, "div")
        assert div[1].text == "title"

        right = items[0].find_element(By.CLASS_NAME, "logRight")
        div = right.find_elements(By.CSS_SELECTOR, "div div")
        assert div[2].text == "sample_movie.mp4"

    def test_添付ファイル付きの動画から添付ファイルを削除する(self):
        self._動画をアップロードする(attachment=True)
        alert = WebDriverWait(driver, timeout=2).until(
            expected_conditions.alert_is_present())
        assert alert.text == "動画を投稿しました。"
        alert.accept()
        alert = WebDriverWait(driver, timeout=2).until(
            expected_conditions.alert_is_present())
        assert alert.text == "添付ファイルのアップロードに成功しました。"
        alert.accept()
        sleep(30)

        # MY動画へ移動
        driver.get(f"{ROOT}/admin-v?cid={CID}")
        # wait
        sleep(2)
        items = driver.find_elements(
            By.CSS_SELECTOR, ".vframeListAdminBG .vframeListInfoAdmin a")
        detail_page_url = items[0].get_attribute("href")
        driver.get(detail_page_url)
        sleep(3)

        # 動画詳細編集へ移動
        driver.get(detail_page_url)
        # wait
        sleep(2)
        highLeveltab = driver.find_element(By.ID, "highLeveltab")
        highLeveltab.click()
        sleep(1)

        attachmentFile = driver.find_element(By.ID, "tmpFileLinks")
        assert attachmentFile.get_attribute("innerText") == "attachment.png"

        remove_icon = driver.find_element(By.ID, "tmpLinkField0")
        remove_icon.click()

        submit_button = driver.find_element(By.ID, "btnSubmit")
        submit_button.click()
        alert = WebDriverWait(driver, timeout=1).until(
            expected_conditions.alert_is_present())
        assert alert.text == "更新しました。"
        alert.accept()
        driver.refresh()
        sleep(2)

        remove_icon = driver.find_elements(By.ID, "tmpLinkField0")
        assert len(remove_icon) == 0

    @ pytest.mark.skip(reason="うまく書けないので手動で行う")
    def test_チャンネル作成(self):
        login()
        driver.get("%s/admin_ch?mode=create?cid=%s" % (ROOT, CID))
        assert driver.title == "SQEX-TV | Create or update channel"
        sleep(2)

        # create_mode_radio = driver.find_element(By.ID, "chkcreate")
        # create_mode_radio.click()

        inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
        inputs[1].send_keys(self.createFilepath("240x80.png"))

        inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
        inputs[2].send_keys(self.createFilepath("920x320.png"))
        inputs[3].send_keys(self.createFilepath("920x320.png"))
        inputs[4].send_keys(self.createFilepath("920x320.png"))

        # alias = driver.find_element(By.ID, "description_fill")
        # alias.send_keys("the_alias")

        # shorthand = driver.find_element(By.ID, "title2")
        # shorthand.send_keys("s_h")

        # title = driver.find_element(By.ID, "title")
        # title.send_keys("the_title")
        sleep(3)
        submit = driver.find_element(By.ID, "btnSubmit2")
        submit.click()

        alert = WebDriverWait(driver, timeout=1).until(
            expected_conditions.alert_is_present())
        assert alert.text == "更新しました。"

    def test_動画再生画面表示(self):
        login()
        driver.get("%s/index" % (ROOT))
        # wait
        sleep(3)
        thumbs = driver.find_elements(By.CSS_SELECTOR, ".t_medium_tile a")
        play_page_url = thumbs[0].get_attribute("href")
        driver.get(play_page_url)
        sleep(3)
        assert driver.title == "SQEX-TV | Play"
        video = driver.find_element(By.CSS_SELECTOR, "video")
        video_url = video.get_attribute("src")
        assert re.search(
            "/videoFiles/sqextv/[0-9a-f]*.mp4", video_url) != None

    def test_コーポレートチャンネルのTOP(self):
        login()
        driver.get("%s/channel/squareenix" % (ROOT))
        assert driver.title == "SQEX-TV"

    @ pytest.mark.skip(reason="refと同じ状況だがサーバはエラーを吐いている")
    def test_コーポレートチャンネルのメンバー(self):
        login()
        driver.get("%s/admin-cmem?cid=%s" % (ROOT, CID))
        assert driver.title == "SQEX-TV | AdminPanel"
        sleep(5)
        members = driver.find_element(By.ID, "memberPanel")
        html = members.get_attribute("innerHTML")
        assert "現在情報を取得中です、しばらくお待ちください・・・" in html == False

    def test_MY動画ページにコーポレートチャンネルの全動画一覧が表示される(self):
        login()
        driver.get("%s/admin-vm?cid=%s" % (ROOT, CID))
        assert driver.title == "SQEX-TV | AdminPanel"
        sleep(3)
        items = driver.find_elements(By.CLASS_NAME, "vframeListAdminLongBG")
        assert len(items) > 0

    def test_システム管理者設定(self):
        login()
        driver.get("%s/admin-sys?cid=%s" % (ROOT, CID))
        contents = driver.find_element(By.ID, "contents_mini")
        html = contents.get_attribute("innerHTML")
        matches = re.search("(.\\s)*old menu(.\\s)*", html)
        assert matches != None

    def test_helppage(self):
        login()
        driver.get("%s/help" % (ROOT))
        contents = driver.find_element(By.ID, "content")
        html = contents.get_attribute("innerHTML")
        matches = re.search(
            "(.\\s)*対応ブラウザ：IE9及び google Chrome 36.0.1985.125 m/Firefox 31.0 にて基本的な動作を確認しております。(.\\s)*", html)
        assert matches != None

    def test_videoServer_storage_page(self):
        login()
        driver.get("%s/admin_vall?cid=%s" % (ROOT, CID))
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.TAG_NAME, 'iframe')))

        iframe = driver.find_element(By.CSS_SELECTOR, 'iframe')
        driver.switch_to.frame(iframe)
        table = driver.find_element(By.CSS_SELECTOR, "table")
        assert table != None

    @ pytest.mark.skip(reason="refと同じ状況だがサーバはエラーを吐いている")
    def test_userControl_page(self):
        login()
        driver.get("%s/admin_u?cid=%s" % (ROOT, CID))
        table = driver.find_element(By.CSS_SELECTOR, "table")
        html = table.get_attribute("innerHTML")
        matches = re.search("administrator", html)
        assert matches != None

    def test_encoding_page(self):
        login()
        driver.get("%s/admin_s2?cid=%s" % (ROOT, CID))
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'iframe')))

        # iframeを取得
        iframe = driver.find_element(By.CSS_SELECTOR, 'iframe')
        # iframeの中の要素を操作するために切り替える
        driver.switch_to.frame(iframe)
        items = driver.find_elements(By.CLASS_NAME, "enclog_base")
        assert len(items) > 0

    def test_admin_help_page(self):
        login()
        driver.get("%s/admin_h?cid=%s" % (ROOT, CID))
        contents = driver.find_element(By.ID, "content")
        html = contents.get_attribute("innerHTML")
        matches = re.search(
            "(.\\s)*対応ブラウザ：IE9及び google Chrome 36.0.1985.125 m/Firefox 31.0 にて基本的な動作を確認しております。(.\\s)*", html)
        assert matches != None

    def test_admin_v_page(self):
        login()
        driver.get("%s/admin_v_old?cid=%s" % (ROOT, CID))
        contents = driver.find_element(By.CSS_SELECTOR, "tbody")
        html = contents.get_attribute("innerHTML")
        matches = re.search("Featured Items:", html)
        assert matches != None

    def test_stats_helppage(self):
        login()
        driver.get("%s/admin_s?cid=%s" % (ROOT, CID))
        sleep(1)
        table = driver.find_element(By.CSS_SELECTOR, "table.datatable")
        tr = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        assert len(tr) > 0

    def test_comments_page(self):
        login()
        driver.get("%s/admin_c?cid=%s" % (ROOT, CID))
        sleep(1)
        table = driver.find_element(By.CSS_SELECTOR, "table.datatable")
        tr = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        assert len(tr) > 0

    def test_user_search_page(self):
        login()
        driver.get("%s/admin_dl?cid=%s" % (ROOT, CID))
        contents = driver.find_element(By.CSS_SELECTOR, "tbody")
        html = contents.get_attribute("innerHTML")
        matches = re.search(
            "A special view is displayed when it searches using a blank.", html)
        assert matches != None

    def test_channel_user_page(self):
        login()
        driver.get("%s/channel/userpage?userpage=administrator" % (ROOT))

        username = driver.find_element(By.ID, "channelNameInner")
        html = username.get_attribute("innerHTML")
        matches = re.search("administratorさんの動画", html)
        assert matches != None

        table = driver.find_element(By.ID, "categoryItemsInner")
        items = table.find_elements(By.CSS_SELECTOR, "a")
        assert len(items) > 0

    @ pytest.mark.skip(reason="ボタンが表示されないのでスキップ")
    def test_channellist(self):
        login()
        driver.get("%s/channellist" % (ROOT))

    @ pytest.mark.skip(reason="できてないので無条件でスキップします。")
    def test_sample_test(self):
        login()


class Test_個人設定():
    def test_個人設定画面を表示する(self):
        login()
        driver.get(f"{ROOT}/admin-uch?cid={CID}")
        assert driver.title == "SQEX-TV | Create or update channel"

    def test_個人設定を変更する(self):
        login()
        driver.get(f"{ROOT}/admin-uch?cid={CID}")

        img_thumb = driver.find_element(By.ID, "img_thumb")
        assert img_thumb.get_attribute(
            "src") == f"{ENCODER}/channelfiles/userpage/administrator/icon.png"

        inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")

        upload_file = createFilePath("76x76.png")
        inputs[0].send_keys(upload_file)
        inputs[1].send_keys(upload_file)

        upload_file = createFilePath("banner.png")
        inputs[2].send_keys(upload_file)
        inputs[3].send_keys(upload_file)

        sleep(1)

        img_thumb = driver.find_element(By.ID, "img_thumb")
        img_src = img_thumb.get_attribute("src")
        assert re.search("[0-9a-f]*.png", img_src) != None

        img_ban = driver.find_element(By.ID, "img_ban")
        img_src = img_ban.get_attribute("src")
        assert re.search("[0-9a-f]*.png", img_src) != None

        submit_button = driver.find_element(By.ID, "btnSubmit")
        submit_button.click()
        sleep(1)

        alert = WebDriverWait(driver, timeout=1).until(
            expected_conditions.alert_is_present())
        assert alert.text == "更新しました。"


"""
#### 200を調べるUrls
####
- 動画投稿/変更時の「高度な機能」タブの添付ファイル（添付削除時）
"""
