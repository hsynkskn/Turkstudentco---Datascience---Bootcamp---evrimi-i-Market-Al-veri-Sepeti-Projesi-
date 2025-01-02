import streamlit as st
import pandas as pd  # Pandas modülü ekleniyor

# Market sınıfını içe aktar
class Market:
    def __init__(self, filename='product.txt'):
        self.filename = filename
        # Dosyanın mevcut olup olmadığını kontrol et
        try:
            with open(self.filename, 'r'):
                pass
        except FileNotFoundError:
            # Dosya yoksa oluştur
            with open(self.filename, 'w') as file:
                pass
    
    def add_product(self, product_name, product_price, product_category=None, product_stock=None):
        # Ürün ekleme
        with open(self.filename, 'a') as file:
            file.write(f"{product_name},{product_category or ''},{product_price},{product_stock or ''}\n")

    def read_products(self):
        # Ürünleri okuma
        products = []
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    product = {
                        'name': parts[0],
                        'category': parts[1] if len(parts) > 1 else '',
                        'price': float(parts[2]),
                        'stock': int(parts[3]) if len(parts) > 3 else 0
                    }
                    products.append(product)
        return products

    def list_products(self):
        # Tüm ürünleri listeleme
        products = self.read_products()
        if products:
            # Ürünleri 1'den başlayarak numaralandır ve tabloyu oluştur
            df = pd.DataFrame(products)
            df.index = range(1, len(df) + 1)  # Sıra numarası 1'den başlar
            df.index.name = 'Sıra No'  # Index sütununa başlık ekler
            st.table(df)  # Ürünleri tablo formatında ekrana yazdır
        else:
            st.warning("Listeleme yapılacak ürün bulunamadı!")

    def delete_products(self, identifiers):
        # Ürünleri silme
        products = self.read_products()
        updated_products = [p for p in products if p['name'] not in identifiers]
        
        # Dosya içeriğini temizleyin
        with open(self.filename, 'w') as file:
            for product in updated_products:
                file.write(f"{product['name']},{product['category']},{product['price']},{product['stock']}\n")

# Streamlit arayüzü
st.title("Çevrimiçi Market Alışveriş Sepeti")

# Sol tarafta menü butonları
menu_option = st.sidebar.radio(
    "*** MENÜ ***",
    ["Ürün Ekle","Ürünleri Listele",  "Ürün Sil", "Çıkış"]
)

market = Market()



if menu_option == "Ürün Ekle":
    product_name = st.text_input("Ürün Adı:")
    product_price = st.number_input("Fiyat:", min_value=0.0)
    product_category = st.text_input("Kategori (isteğe bağlı):")
    product_stock = st.number_input("Stok Miktarı (isteğe bağlı):", min_value=0)
    if st.button("Ekle"):
        market.add_product(product_name, product_price, product_category, product_stock)
        st.success("Ürün başarıyla eklendi!")

elif menu_option == "Ürünleri Listele":
    market.list_products()

elif menu_option == "Ürün Sil":
    products = market.read_products()
    if products:
        # Mevcut ürün isimlerini MultiSelect için hazırlama
        product_names = [product['name'] for product in products]
        selected_products = st.multiselect("Silmek istediğiniz ürünleri seçin:", options=product_names)
        
        if selected_products:
            # Seçilen ürünlerin bilgilerini tablo olarak göster
            selected_details = [p for p in products if p['name'] in selected_products]
            df = pd.DataFrame(selected_details)
            st.table(df)  # Seçilen ürünleri tablo formatında göster
            
            # Uyarı mesajı
            st.warning("Seçilen Ürünler Ürünler Listesinden Silinecektir! Devam Etmek İçin Sil Butonuna Tıklayınız")
            
            # Silme işlemi
            if st.button("Sil"):
                market.delete_products(selected_products)
                st.success("Seçilen ürünler başarıyla silindi!")
        else:
            st.info("Silmek için bir veya daha fazla ürün seçin.")
    else:
        st.warning("Silinecek ürün bulunamadı!")

elif menu_option == "Çıkış":
    st.write("Uygulama sonlandırılıyor...")
