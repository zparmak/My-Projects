import pandas as pd
import streamlit as st
import calendar
import datetime
from datetime import datetime, date, timedelta
from PIL import Image


st.markdown("""
			<div style="background-color:#FFA500;\
						border-radius: 10px;\
						padding:15px">
			<h2 style="color:white;\
					   text-align:center;\
					   font-family:cursive;">AURORA Historik ve Gün İçi Performans Bazlı Günlük Kapasite Dağıtım Sezgiseli\
			</h2>
			</div>
			""", unsafe_allow_html=True
			)

st.markdown("""
			<style>
    		[data-baseweb="select"] {
                
        							margin-top: 50px;
    								}
    		</style>
    		""", unsafe_allow_html=True,
			)

st.image("https://cdn.iha.com.tr/Contents/images/2021/28/3975550.jpg", width=700)


kapasite = st.number_input("Acentelere dağıtalacak günlük kontenjan miktarını giriniz.", min_value=0, max_value=500, step=1)


beta = st.number_input("Kalan kapasitenin geçmiş (historik) performansa bağlı olarak dağıtılacak yüzdesini (0 ile 100 arasında) giriniz.", min_value=0, max_value=500, step=1)

alpha = st.number_input("Kalan kapasitenin gün içi performansa bağlı olarak dağıtılacak yüzdesini (0 ile 100 arasında) giriniz. ", min_value=0, max_value=500, step=1)


df = pd.read_excel("Aurora.xlsx")

df = df.rename(columns = {"Historik data": "Historik_Data", "Acente 1": "Acente_1", "Acente 2": "Acente_2", "Acente 3": "Acente_3","Acente 4": "Acente_4" })

df["Günlük_Toplam_Satış"] = df["Acente_1"] + df["Acente_2"] + df["Acente_3"] + df["Acente_4"]

df["Acente_1_Günlük_Skor"] = (df["Acente_1"]/df["Günlük_Toplam_Satış"]).round(2)
df["Acente_2_Günlük_Skor"] = (df["Acente_2"]/df["Günlük_Toplam_Satış"]).round(2)
df["Acente_3_Günlük_Skor"] = (df["Acente_3"]/df["Günlük_Toplam_Satış"]).round(2)
df["Acente_4_Günlük_Skor"] = (1 - (df["Acente_1_Günlük_Skor"] + df["Acente_2_Günlük_Skor"] + df["Acente_3_Günlük_Skor"])).round(2)


# get today's date
d = date.today()
print('Date is:', d)

# get day name in english
gün_bilgisi = calendar.day_name[d.weekday()]


if gün_bilgisi == 'Monday':
    gün_bilgisi = 'Pazartesi'
elif gün_bilgisi == 'Tuesday':
    gün_bilgisi = 'Salı'
elif gün_bilgisi == 'Wednesday':
    gün_bilgisi = 'Çarşamba'
elif gün_bilgisi == 'Thursday':
    gün_bilgisi = 'Perşembe'
elif gün_bilgisi == 'Friday':
    gün_bilgisi = 'Cuma'
elif gün_bilgisi == 'Saturday':
    gün_bilgisi = 'Cumartesi'
else:
    gün_bilgisi = 'Pazar'


filtre = df["Gün"] == gün_bilgisi
son_Acente_1_Günlük_Skor = df.loc[filtre, "Acente_1_Günlük_Skor"].iloc[-1]
son_Acente_2_Günlük_Skor = df.loc[filtre, "Acente_2_Günlük_Skor"].iloc[-1]
son_Acente_3_Günlük_Skor = df.loc[filtre, "Acente_3_Günlük_Skor"].iloc[-1]
son_Acente_4_Günlük_Skor = df.loc[filtre, "Acente_4_Günlük_Skor"].iloc[-1]


df_grouped = df.groupby('Gün', as_index=False)[['Acente_1', 'Acente_2', 'Acente_3', 'Acente_4', 'Günlük_Toplam_Satış']].sum()

df_grouped["Acente_1_Historic_Skor"] = (df_grouped["Acente_1"] / df_grouped["Günlük_Toplam_Satış"]).round(2)
df_grouped["Acente_2_Historic_Skor"] = (df_grouped["Acente_2"] / df_grouped["Günlük_Toplam_Satış"]).round(2)
df_grouped["Acente_3_Historic_Skor"] = (df_grouped["Acente_3"] / df_grouped["Günlük_Toplam_Satış"]).round(2)
df_grouped["Acente_4_Historic_Skor"] = (1 - (df_grouped["Acente_1_Historic_Skor"] + df_grouped["Acente_2_Historic_Skor"] + df_grouped["Acente_3_Historic_Skor"])).round(2)


acente_1_kapasite_önerisi = int((((beta / 100 * kapasite * df_grouped[df_grouped["Gün"] == gün_bilgisi]["Acente_1_Historic_Skor"]))+((1-beta /100) * kapasite * alpha / 100 * son_Acente_1_Günlük_Skor) + ((1-beta /100) * kapasite * (1 - alpha / 100) / 4 )).round(0))
acente_2_kapasite_önerisi = int((((beta / 100 * kapasite * df_grouped[df_grouped["Gün"] == gün_bilgisi]["Acente_2_Historic_Skor"]))+((1-beta /100) * kapasite * alpha / 100 * son_Acente_2_Günlük_Skor) + ((1-beta /100) * kapasite * (1 - alpha / 100) / 4 )).round(0))
acente_3_kapasite_önerisi = int((((beta / 100 * kapasite * df_grouped[df_grouped["Gün"] == gün_bilgisi]["Acente_3_Historic_Skor"]))+((1-beta /100) * kapasite * alpha / 100 * son_Acente_3_Günlük_Skor) + ((1-beta /100) * kapasite * (1 - alpha / 100) / 4 )).round(0))
acente_4_kapasite_önerisi =  kapasite - (acente_1_kapasite_önerisi + acente_2_kapasite_önerisi + acente_3_kapasite_önerisi)


dağılım_önerisi = '''
    <style>
        .custom-button {
            background-color: #FFA500;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 0.3rem;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            cursor: pointer;
        }
    </style>
    <button class="custom-button">Dağılım Önerisi</button>
'''

st.markdown(dağılım_önerisi, unsafe_allow_html=True)

if dağılım_önerisi:
    st.write(f"Acente 1 için {d} tarihli {gün_bilgisi} günü kontenjan önerisi: {acente_1_kapasite_önerisi}")
    st.write(f"Acente 2 için {d} tarihli {gün_bilgisi} günü kontenjan önerisi: {acente_2_kapasite_önerisi}")
    st.write(f"Acente 3 için {d} tarihli {gün_bilgisi} günü kontenjan önerisi: {acente_3_kapasite_önerisi}")
    st.write(f"Acente 4 için {d} tarihli {gün_bilgisi} günü kontenjan önerisi: {acente_4_kapasite_önerisi}")
               




