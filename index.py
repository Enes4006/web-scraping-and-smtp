import smtplib
import requests
from bs4 import BeautifulSoup

url = "https://yemek.bozok.edu.tr/"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"}


def check_food():
    page = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(page.content, 'html.parser')

    menu_text = soup.find(id="example").get_text().strip()
    lines = [line.strip() for line in menu_text.split('\n') if line.strip()]

    yemekler = []
    kaloriler = []
    toplam_kalori = ""

    for line in lines:
        # Toplam kalori satırı
        if "TOPLAM" in line.upper():
            toplam_kalori = line
        # Kalori satırları: tamamen rakam ise
        elif line.replace(" ", "").isdigit():
            kaloriler.append(line)
        # Yemek satırları: sayı değil, başlıkları atıyoruz
        elif any(c.isalpha() for c in line):
            # "Menü", "Kalori" gibi başlıkları at
            if line.lower() not in ["menü", "kalori"]:
                yemekler.append(line)

    # Sonuç formatlama
    result = "Bugün Menü:\n\n"
    result += "{:<30} {:>6}\n".format("Yemek", "Kalori")
    result += "-"*38 + "\n"

    for y, k in zip(yemekler, kaloriler):
        result += "{:<30} {:>6}\n".format(y, k)

    result += "\n" + toplam_kalori

    print(result)
    return result


def send_mail():
    sender='enesbaysal04@gmail.com'
    receiver='enesbaysal04@gmail.com'
    password='jmlxfjmblmzjapvs' # uygulama şifresi
    #message.attach(MIMEText(body, 'plain', 'utf-8'))  # <--- TÜRKÇE için UTF-8 kodlama
    try:
        server=smtplib.SMTP('smtp.gmail.com',587) # gmail smtp server
        server.ehlo() # başlatma
        server.starttls() # güvenlik
        server.login(sender,password) # uygulama şifresi
        
        subject='Python ile mail gonderme denemesi'
        #body='Python ile mail gonderiyorum.'
        body=check_food()
        message='Subject: {}\n\n{}'.format(subject,body)
        
        server.sendmail(sender,receiver,message.encode('utf-8'))  # TÜRKÇE için UTF-8 kodlama
        print('Mail basariyla gonderildi.')
        
    except smtplib.SMTPResponseException as e:
        print('Hata kodu: ',e.smtp_code)
        print('Hata mesaji: ',e.smtp_error)
    finally:
        server.quit()
        
if __name__ == '__main__':
    send_mail()