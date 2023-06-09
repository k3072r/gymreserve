from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium import common
import multiprocessing
import time
from datetime import datetime

def reserve_main(ward, place, place_detail):

    # Chrome の起動オプションを設定する
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    # ブラウザの新規ウィンドウを開く
    # print('connectiong to remote browser...')
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        desired_capabilities=options.to_capabilities(),
        options=options,
    )
    wait = WebDriverWait(driver, 10)

    # 仙台市の体育館予約ページにアクセスする
    driver.get('https://www.cm2.epss.jp/sendai/eweb/index.jsp')
    wait.until(EC.presence_of_element_located((By.NAME, 'userId')))

    wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='hogehoge']")))

    # ユーザ名とパスワードの入力欄を見つける
    username_input = driver.find_element(By.NAME, 'userId')
    password_input = driver.find_element(By.NAME, 'password')

    # ユーザ名とパスワードを入力する
    username_input.send_keys('1000033425')
    password_input.send_keys('1011')

    # ログインボタンのimgタグを見つける
    login_img = driver.find_element(By.XPATH, "//img[@src='image/bw_login.gif']")
    # imgタグの親要素である<a>タグを取得し、クリックする
    login_button = login_img.find_element(By.XPATH, "..")
    login_button.click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='予約の申込み']")))

    # 「予約の申込み」ボタンのクリック
    click_img = driver.find_element(By.XPATH, "//img[@alt='予約の申込み']")
    click_button = click_img.find_element(By.XPATH, "..")
    click_button.click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='地域から']")))

    # 「地域から」ボタンのクリック
    click_img = driver.find_element(By.XPATH, "//img[@alt='地域から']")
    click_button = click_img.find_element(By.XPATH, "..")
    click_button.click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '" + ward + "')]")))

    # 「〇〇区」ボタンのクリック
    click_button = driver.find_element(By.XPATH, "//a[contains(text(), '" + ward + "')]")
    click_button.click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '" + place + "')]")))

    # 「〇〇市民センター」ボタンのクリック
    click_button = driver.find_element(By.XPATH, "//a[contains(text(), '" + place + "')]")
    click_button.click()

    driver.implicitly_wait(10)

    # 「施設（体育館）」ボタンのクリック
    click_button = driver.find_element(By.XPATH, "//a[contains(text(), '" + place + "') and .//following-sibling::text()[contains(., '" + place_detail + "')]]")
    click_button.click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='次の月']")))

    # 「次の月」ボタンを2回クリック
    click_img = driver.find_element(By.XPATH, "//img[@alt='次の月']")
    click_button = click_img.find_element(By.XPATH, "..")
    click_button.click()
    driver.implicitly_wait(10)
    click_img = driver.find_element(By.XPATH, "//img[@alt='次の月']")
    click_button = click_img.find_element(By.XPATH, "..")
    click_button.click()

    # wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='全て予約可' or @alt='一部予約可']")))
    driver.implicitly_wait(10)

    # 「全て予約可」の日付を取得
    available_dates = driver.find_elements(By.XPATH, "//img[@alt='全て予約可' or @alt='一部予約可']")
    available_num = len(available_dates)

    # 予約埋まってたらその旨を表示することにする
    if available_num == 0:
        print(place + ' 全部埋まってた')
        return

    for i in range(available_num, 0, -1):
        # 「全て予約可」か「一部予約可」の日付をクリック
        available_dates = driver.find_elements(By.XPATH, "//img[@alt='全て予約可' or @alt='一部予約可']")
        click_img = available_dates[i - 1]
        click_button = click_img.find_element(By.XPATH, "..")
        click_button.click()

        ## 当該日付の夜間コマが空いているか：該当するimgタグのalt属性より取得
        # クラスが'akitablelist'のtable要素を取得
        table_element = driver.find_element(By.CSS_SELECTOR, "table.akitablelist")
        # 4つ目のtr要素を取得
        fourth_tr_element = table_element.find_elements(By.TAG_NAME, "tr")[3]
        # 一番初めのtdタグ内のimgタグを取得
        first_img_element = fourth_tr_element.find_element(By.XPATH, ".//td/img | .//td/a/img")
        # imgタグのalt属性を取得
        img_alt_attribute = first_img_element.get_attribute("alt")

        if img_alt_attribute == "予約不可":
            click_img = driver.find_element(By.XPATH, "//img[@alt='もどる']")
            click_button = click_img.find_element(By.XPATH, "..")
            click_button.click()
            continue
        elif img_alt_attribute == "予約可":
            click_img = first_img_element
            click_button = click_img.find_element(By.XPATH, "..")
            click_button.click()
        else:
            print("なんかおかしい")
            break

        wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='申込み']")))

        # 「申込み」ボタンのクリック
        click_img = driver.find_element(By.XPATH, "//img[@alt='申込み']")
        click_button = click_img.find_element(By.XPATH, "..")
        click_button.click()

        wait.until(EC.presence_of_element_located((By.ID, "ruleFg_1")))


        # 「利用規約に同意する」にチェックを入れるのがうまくいかないことがあるので、例外をキャッチしたらリトライするように
        retry = True
        while retry:
            try:
                # 「利用規約に同意する」にチェックを入れ、「確認」ボタンをクリックする
                agree_button = driver.find_element(By.ID, "ruleFg_1")
                driver.execute_script("window.scrollTo(0, " + str(agree_button.location['y']) + ");")   #ラジオボタンが画面外にありnot clickableなことがあるためスクロール
                agree_button.click()
                while not agree_button.is_selected():
                    agree_button = driver.find_element(By.ID, "ruleFg_1")
                    agree_button.click()
                wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='確認']")))
                click_img = driver.find_element(By.XPATH, "//img[@alt='確認']")
                click_button = click_img.find_element(By.XPATH, "..")
                click_button.click()

                retry = False
            
            except common.exceptions.ElementClickInterceptedException:
                print("例外をキャッチ！")
                click_img = driver.find_element(By.XPATH, "//img[@alt='もどる']")
                click_button = click_img.find_element(By.XPATH, "..")
                click_button.click()
                wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='申込み']")))
                click_img = driver.find_element(By.XPATH, "//img[@alt='申込み']")
                click_button = click_img.find_element(By.XPATH, "..")
                click_button.click()


        driver.implicitly_wait(10)

        # 表示用に、予約する日付を取得しておく
        date_element = driver.find_element(By.XPATH, '//table/tbody/tr/td/table/tbody/tr/td[@align="center"]/div[contains(@class, "dcontent")]')
        date_text = date_element.text
        date_text = date_text[ date_text.find('年') + 1 : date_text.find('日') + 1 ] 

        ### TODO 不要になったので消す
        # 同様に館名も取得
        facility_name_element = driver.find_element(By.XPATH, "//td[@class='tablelist'][3]/div[@class='dcontent']")
        facility_name = facility_name_element.text

        # 利用目的の入力
        click_img = driver.find_element(By.XPATH, "//img[@alt='目的の選択']")
        click_button = click_img.find_element(By.XPATH, "..")
        click_button.click()

        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'すべて')]")))
        click_button = driver.find_element(By.XPATH, "//a[contains(text(), 'すべて')]")
        click_button.click()

        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'バレーボール')]")))
        click_button = driver.find_element(By.XPATH, "//a[contains(text(), 'バレーボール')]")
        click_button.click()

        # 利用人数の入力
        wait.until(EC.presence_of_element_located((By.NAME, "applyNum")))
        applyNum_textbox = driver.find_element(By.NAME, "applyNum")
        applyNum_textbox.send_keys('21')

        # # 「申込み」ボタンのクリック
        # click_img = driver.find_element(By.XPATH, "//img[@alt='申込み']")
        # click_button = click_img.find_element(By.XPATH, "..")
        # click_button.click()

        # driver.implicitly_wait(10)

        # wait = WebDriverWait(driver,10)
        # try:

        #     wait.until(EC.alert_is_present())   #Javascriptのアラートがでてくるまで待つ
        #     Alert(driver).accept()              #アラート受け入れる(OKを押す)        
        #     time.sleep(1)                       #1秒まつ

        # except Exception as e:
        #     print("アラートの処理でエラー")

        print(date_text + ' ' + facility_name + ' 予約完了')

        # # 「終了」ボタンのクリック
        # click_img = driver.find_element(By.XPATH, "//img[@alt='終了']")
        # click_button = click_img.find_element(By.XPATH, "..")
        # click_button.click()

        # 「メニューへ」ボタンのクリック
        click_img = driver.find_element(By.XPATH, "//img[@alt='メニューへ']")
        click_button = click_img.find_element(By.XPATH, "..")
        click_button.click()

        # 「予約の申込み」ボタンのクリック
        click_img = driver.find_element(By.XPATH, "//img[@alt='予約の申込み']")
        click_button = click_img.find_element(By.XPATH, "..")
        click_button.click()

        wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='地域から']")))

        # 「地域から」ボタンのクリック
        click_img = driver.find_element(By.XPATH, "//img[@alt='地域から']")
        click_button = click_img.find_element(By.XPATH, "..")
        click_button.click()

        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '" + ward + "')]")))

        # 「宮城野区」ボタンのクリック
        click_button = driver.find_element(By.XPATH, "//a[contains(text(), '" + ward + "')]")
        click_button.click()

        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '" + place + "')]")))

        # 「福室市民センター」ボタンのクリック
        click_button = driver.find_element(By.XPATH, "//a[contains(text(), '" + place + "')]")
        click_button.click()

        driver.implicitly_wait(10)

        # 「調理実習室」ボタンのクリック
        click_button = driver.find_element(By.XPATH, "//a[contains(text(), '" + place + "') and .//following-sibling::text()[contains(., '" + place_detail + "')]]")
        click_button.click()

        wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='次の月']")))

        # 「次の月」ボタンを2回クリック
        click_img = driver.find_element(By.XPATH, "//img[@alt='次の月']")
        click_button = click_img.find_element(By.XPATH, "..")
        click_button.click()
        driver.implicitly_wait(10)
        click_img = driver.find_element(By.XPATH, "//img[@alt='次の月']")
        click_button = click_img.find_element(By.XPATH, "..")
        click_button.click()

        driver.implicitly_wait(10)

    # ブラウザを終了する
    driver.quit()


def main():

    reserve_main('若林区', '六郷市民センター', '体育館')

    # process1 = multiprocessing.Process(target=reserve_main, args=('若林区', '六郷市民センター', '体育館'))
    # process2 = multiprocessing.Process(target=reserve_main, args=('太白区', '生出市民センター', '体育館'))
    # process3 = multiprocessing.Process(target=reserve_main, args=('宮城野区', '東部市民センター', '体育館'))
    # process4 = multiprocessing.Process(target=reserve_main, args=('太白区', '茂庭台市民センター', '体育館'))
    # process5 = multiprocessing.Process(target=reserve_main, args=('宮城野区', '榴ケ岡市民センター', '体育館'))

    # process1.start()
    # process2.start()
    # process3.start()
    # process4.start()
    # process5.start()

    # process1.join()
    # process2.join()
    # process3.join()
    # process4.join()
    # process5.join()



if __name__ == '__main__':
    main()