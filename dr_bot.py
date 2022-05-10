from PIL import Image
from bs4 import BeautifulSoup
import requests  
import itertools

kategoriler = ["Edebiyat/grupno=00055","Cocuk-ve-Genclik/Genclik-10-Yas/grupno=00887","Egitim-Basvuru/grupno=00056","Arastirma-Tarih/grupno=00051","Din-Tasavvuf/grupno=00054","Sanat-Tasarim/grupno=00063","Felsefe/grupno=00058","Hobi/grupno=00060","Bilim/grupno=00052","Cizgi-Roman/grupno=00053","Mizah/grupno=00061","Mitoloji-Efsane/grupno=00190"]
sayfalar = [200,157,637,480,293,120,114,73,71,71,22,10]

for kategori,sayfa in itertools.product(kategoriler,sayfalar):
    
    i=0
    page=1

    while page<sayfa:
        url = requests.get("https://www.dr.com.tr/Kategori/Kitap/"+kategori+"/?Page="+str(page)+"&ShowNotForSale=false")
        soup = BeautifulSoup(url.content, "html.parser")


        books_part = soup.find_all(class_="prd")
        for book in books_part:
            if book.find(class_="prd-row").find("a") is not None:
                img_url = book.find("img")["data-src"]
                yazar = book.find(class_="prd-row").find("a").string
                yazar = yazar.replace("?","soru").replace(":","ikinokta").replace("/","slash") # Dosya oluştururken kullanamayacağımız bağızı karakterler
                
                isim = book.find(class_="prd-content-wrapper").find("a").string
                isim = isim.replace("?","soru").replace(":","ikinokta").replace("/","slash") # Dosya oluştururken kullanamayacağımız bağızı karakterler
                
                img = Image.open(requests.get(img_url,stream=True).raw)
                img.save("resimler/"+yazar+"_"+isim+".jpg")
            
            i+=1    
        print(page)
        page+=1
            
    print(i)