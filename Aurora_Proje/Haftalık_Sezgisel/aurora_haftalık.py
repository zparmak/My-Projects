import pandas as pd
import streamlit as st
import datetime
from datetime import datetime, timedelta,date
import calendar
from PIL import Image
import locale
locale.setlocale(locale.LC_ALL, 'tr_TR')

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

kapasite1 = st.number_input("Acentelere dağıtalacak 1. gün (bugün) kontenjan miktarını giriniz: ", min_value=0, max_value=500, step=1)
kapasite2 = st.number_input("Acentelere dağıtalacak 2. gün (yarın) kontenjan miktarını giriniz: ", min_value=0, max_value=500, step=1)
kapasite3 = st.number_input("Acentelere dağıtalacak 3. gün kontenjan miktarını giriniz.", min_value=0, max_value=500, step=1)
kapasite4 = st.number_input("Acentelere dağıtalacak 4. gün kontenjan miktarını giriniz.", min_value=0, max_value=500, step=1)
kapasite5 = st.number_input("Acentelere dağıtalacak 5. gün kontenjan miktarını giriniz.", min_value=0, max_value=500, step=1)
kapasite6 = st.number_input("Acentelere dağıtalacak 6. gün kontenjan miktarını giriniz.", min_value=0, max_value=500, step=1)
kapasite7 = st.number_input("Acentelere dağıtalacak 7. gün kontenjan miktarını giriniz.", min_value=0, max_value=500, step=1)


beta = st.number_input("Kalan kapasitenin geçmiş (historik) performansa bağlı olarak dağıtılacak yüzdesini (0 ile 100 arasında) giriniz. (beta)", min_value=0, max_value=500, step=1)

alpha = st.number_input("Kalan kapasitenin gün içi performansa bağlı olarak dağıtılacak yüzdesini (0 ile 100 arasında) giriniz. (alpha) ", min_value=0, max_value=500, step=1)

df = pd.read_excel("Aurora.xlsx")

df = df.rename(columns = {"Historik data": "Historik_Data", "Acente 1": "Acente_1", "Acente 2": "Acente_2", "Acente 3": "Acente_3","Acente 4": "Acente_4" })

df["Günlük_Toplam_Satış"] = df["Acente_1"] + df["Acente_2"] + df["Acente_3"] + df["Acente_4"]

df["Acente_1_Günlük_Skor"] = (df["Acente_1"]/df["Günlük_Toplam_Satış"]).round(2)
df["Acente_2_Günlük_Skor"] = (df["Acente_2"]/df["Günlük_Toplam_Satış"]).round(2)
df["Acente_3_Günlük_Skor"] = (df["Acente_3"]/df["Günlük_Toplam_Satış"]).round(2)
df["Acente_4_Günlük_Skor"] = (df["Acente_4"]/df["Günlük_Toplam_Satış"]).round(2)

d1 = date.today()
d2 = d1 + timedelta(days=1)
d3 = d1 + timedelta(days=2)
d4 = d1 + timedelta(days=3)
d5 = d1 + timedelta(days=4)
d6 = d1 + timedelta(days=5)
d7 = d1 + timedelta(days=6)

gün_bilgisi1 = calendar.day_name[d1.weekday()]
gün_bilgisi2 = calendar.day_name[d2.weekday()]
gün_bilgisi3 = calendar.day_name[d3.weekday()]
gün_bilgisi4 = calendar.day_name[d4.weekday()]
gün_bilgisi5 = calendar.day_name[d5.weekday()]
gün_bilgisi6 = calendar.day_name[d6.weekday()]
gün_bilgisi7 = calendar.day_name[d7.weekday()]

filtre1 = df["Gün"] == gün_bilgisi1
son_Acente_1_Günlük_Skor_1 = df.loc[filtre1, "Acente_1_Günlük_Skor"].iloc[-1]
son_Acente_2_Günlük_Skor_1 = df.loc[filtre1, "Acente_2_Günlük_Skor"].iloc[-1]
son_Acente_3_Günlük_Skor_1 = df.loc[filtre1, "Acente_3_Günlük_Skor"].iloc[-1]
son_Acente_4_Günlük_Skor_1 = df.loc[filtre1, "Acente_4_Günlük_Skor"].iloc[-1]

filtre2 = df["Gün"] == gün_bilgisi2
son_Acente_1_Günlük_Skor_2 = df.loc[filtre2, "Acente_1_Günlük_Skor"].iloc[-1]
son_Acente_2_Günlük_Skor_2 = df.loc[filtre2, "Acente_2_Günlük_Skor"].iloc[-1]
son_Acente_3_Günlük_Skor_2 = df.loc[filtre2, "Acente_3_Günlük_Skor"].iloc[-1]
son_Acente_4_Günlük_Skor_2 = df.loc[filtre2, "Acente_4_Günlük_Skor"].iloc[-1]

filtre3 = df["Gün"] == gün_bilgisi3
son_Acente_1_Günlük_Skor_3 = df.loc[filtre3, "Acente_1_Günlük_Skor"].iloc[-1]
son_Acente_2_Günlük_Skor_3 = df.loc[filtre3, "Acente_2_Günlük_Skor"].iloc[-1]
son_Acente_3_Günlük_Skor_3 = df.loc[filtre3, "Acente_3_Günlük_Skor"].iloc[-1]
son_Acente_4_Günlük_Skor_3 = df.loc[filtre3, "Acente_4_Günlük_Skor"].iloc[-1]

filtre4 = df["Gün"] == gün_bilgisi4
son_Acente_1_Günlük_Skor_4 = df.loc[filtre4, "Acente_1_Günlük_Skor"].iloc[-1]
son_Acente_2_Günlük_Skor_4 = df.loc[filtre4, "Acente_2_Günlük_Skor"].iloc[-1]
son_Acente_3_Günlük_Skor_4 = df.loc[filtre4, "Acente_3_Günlük_Skor"].iloc[-1]
son_Acente_4_Günlük_Skor_4 = df.loc[filtre4, "Acente_4_Günlük_Skor"].iloc[-1]

filtre5 = df["Gün"] == gün_bilgisi5
son_Acente_1_Günlük_Skor_5 = df.loc[filtre5, "Acente_1_Günlük_Skor"].iloc[-1]
son_Acente_2_Günlük_Skor_5 = df.loc[filtre5, "Acente_2_Günlük_Skor"].iloc[-1]
son_Acente_3_Günlük_Skor_5 = df.loc[filtre5, "Acente_3_Günlük_Skor"].iloc[-1]
son_Acente_4_Günlük_Skor_5 = df.loc[filtre5, "Acente_4_Günlük_Skor"].iloc[-1]

filtre6 = df["Gün"] == gün_bilgisi6
son_Acente_1_Günlük_Skor_6 = df.loc[filtre6, "Acente_1_Günlük_Skor"].iloc[-1]
son_Acente_2_Günlük_Skor_6 = df.loc[filtre6, "Acente_2_Günlük_Skor"].iloc[-1]
son_Acente_3_Günlük_Skor_6 = df.loc[filtre6, "Acente_3_Günlük_Skor"].iloc[-1]
son_Acente_4_Günlük_Skor_6 = df.loc[filtre6, "Acente_4_Günlük_Skor"].iloc[-1]

filtre7 = df["Gün"] == gün_bilgisi7
son_Acente_1_Günlük_Skor_7 = df.loc[filtre7, "Acente_1_Günlük_Skor"].iloc[-1]
son_Acente_2_Günlük_Skor_7 = df.loc[filtre7, "Acente_2_Günlük_Skor"].iloc[-1]
son_Acente_3_Günlük_Skor_7 = df.loc[filtre7, "Acente_3_Günlük_Skor"].iloc[-1]
son_Acente_4_Günlük_Skor_7 = df.loc[filtre7, "Acente_4_Günlük_Skor"].iloc[-1]

df_grouped = df.groupby('Gün', as_index=False)[['Acente_1', 'Acente_2', 'Acente_3', 'Acente_4', 'Günlük_Toplam_Satış']].sum()

df_grouped["Günlük_Toplam_Satış"] = df_grouped["Acente_1"] + df_grouped["Acente_2"]+ df_grouped["Acente_3"]+ df_grouped["Acente_4"]

df_grouped["Acente_1_Historic_Skor"] = (df_grouped["Acente_1"] / df_grouped["Günlük_Toplam_Satış"]).round(2)
df_grouped["Acente_2_Historic_Skor"] = (df_grouped["Acente_2"] / df_grouped["Günlük_Toplam_Satış"]).round(2)
df_grouped["Acente_3_Historic_Skor"] = (df_grouped["Acente_3"] / df_grouped["Günlük_Toplam_Satış"]).round(2)
df_grouped["Acente_4_Historic_Skor"] = (df_grouped["Acente_4"] / df_grouped["Günlük_Toplam_Satış"]).round(2)

acente_1_kapasite_önerisi_1 = int((((beta / 100 * kapasite1 * df_grouped[df_grouped["Gün"] == gün_bilgisi1]["Acente_1_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite1 * alpha / 100 * son_Acente_1_Günlük_Skor_1) + ((1-beta /100) * kapasite1 * (1 - alpha / 100) / 4 )).round(0))
acente_2_kapasite_önerisi_1 = int((((beta / 100 * kapasite1 * df_grouped[df_grouped["Gün"] == gün_bilgisi1]["Acente_2_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite1 * alpha / 100 * son_Acente_2_Günlük_Skor_1) + ((1-beta /100) * kapasite1 * (1 - alpha / 100) / 4 )).round(0))
acente_3_kapasite_önerisi_1 = int((((beta / 100 * kapasite1 * df_grouped[df_grouped["Gün"] == gün_bilgisi1]["Acente_3_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite1 * alpha / 100 * son_Acente_3_Günlük_Skor_1) + ((1-beta /100) * kapasite1 * (1 - alpha / 100) / 4 )).round(0))
acente_4_kapasite_önerisi_1 =  kapasite1 - (acente_1_kapasite_önerisi_1 + acente_2_kapasite_önerisi_1 + acente_3_kapasite_önerisi_1)

acente_1_kapasite_önerisi_2 = int((((beta / 100 * kapasite2 * df_grouped[df_grouped["Gün"] == gün_bilgisi2]["Acente_1_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite2 * alpha / 100 * son_Acente_1_Günlük_Skor_2) + ((1-beta /100) * kapasite2 * (1 - alpha / 100) / 4 )).round(0))
acente_2_kapasite_önerisi_2 = int((((beta / 100 * kapasite2 * df_grouped[df_grouped["Gün"] == gün_bilgisi2]["Acente_2_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite2 * alpha / 100 * son_Acente_2_Günlük_Skor_2) + ((1-beta /100) * kapasite2 * (1 - alpha / 100) / 4 )).round(0))
acente_3_kapasite_önerisi_2 = int((((beta / 100 * kapasite2 * df_grouped[df_grouped["Gün"] == gün_bilgisi2]["Acente_3_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite2 * alpha / 100 * son_Acente_3_Günlük_Skor_2) + ((1-beta /100) * kapasite2 * (1 - alpha / 100) / 4 )).round(0))
acente_4_kapasite_önerisi_2 =  kapasite2 - (acente_1_kapasite_önerisi_2 + acente_2_kapasite_önerisi_2 + acente_3_kapasite_önerisi_2)

acente_1_kapasite_önerisi_3 = int((((beta / 100 * kapasite3 * df_grouped[df_grouped["Gün"] == gün_bilgisi3]["Acente_1_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite3 * alpha / 100 * son_Acente_1_Günlük_Skor_3) + ((1-beta /100) * kapasite3 * (1 - alpha / 100) / 4 )).round(0))
acente_2_kapasite_önerisi_3 = int((((beta / 100 * kapasite3 * df_grouped[df_grouped["Gün"] == gün_bilgisi3]["Acente_2_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite3 * alpha / 100 * son_Acente_2_Günlük_Skor_3) + ((1-beta /100) * kapasite3* (1 - alpha / 100) / 4 )).round(0))
acente_3_kapasite_önerisi_3 = int((((beta / 100 * kapasite3 * df_grouped[df_grouped["Gün"] == gün_bilgisi3]["Acente_3_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite3 * alpha / 100 * son_Acente_3_Günlük_Skor_3) + ((1-beta /100) * kapasite3 * (1 - alpha / 100) / 4 )).round(0))
acente_4_kapasite_önerisi_3 =  kapasite3 - (acente_1_kapasite_önerisi_3 + acente_2_kapasite_önerisi_3 + acente_3_kapasite_önerisi_3)

acente_1_kapasite_önerisi_4 = int((((beta / 100 * kapasite4 * df_grouped[df_grouped["Gün"] == gün_bilgisi4]["Acente_1_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite4 * alpha / 100 * son_Acente_1_Günlük_Skor_4) + ((1-beta /100) * kapasite4 * (1 - alpha / 100) / 4 )).round(0))
acente_2_kapasite_önerisi_4 = int((((beta / 100 * kapasite4 * df_grouped[df_grouped["Gün"] == gün_bilgisi4]["Acente_2_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite4 * alpha / 100 * son_Acente_2_Günlük_Skor_4) + ((1-beta /100) * kapasite4 * (1 - alpha / 100) / 4 )).round(0))
acente_3_kapasite_önerisi_4 = int((((beta / 100 * kapasite4 * df_grouped[df_grouped["Gün"] == gün_bilgisi4]["Acente_3_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite4 * alpha / 100 * son_Acente_3_Günlük_Skor_4) + ((1-beta /100) * kapasite4 * (1 - alpha / 100) / 4 )).round(0))
acente_4_kapasite_önerisi_4 =  kapasite4 - (acente_1_kapasite_önerisi_4 + acente_2_kapasite_önerisi_4 + acente_3_kapasite_önerisi_4)

acente_1_kapasite_önerisi_5 = int((((beta / 100 * kapasite5 * df_grouped[df_grouped["Gün"] == gün_bilgisi5]["Acente_1_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite5 * alpha / 100 * son_Acente_1_Günlük_Skor_5) + ((1-beta /100) * kapasite5 * (1 - alpha / 100) / 4 )).round(0))
acente_2_kapasite_önerisi_5 = int((((beta / 100 * kapasite5 * df_grouped[df_grouped["Gün"] == gün_bilgisi5]["Acente_2_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite5 * alpha / 100 * son_Acente_2_Günlük_Skor_5) + ((1-beta /100) * kapasite5 * (1 - alpha / 100) / 4 )).round(0))
acente_3_kapasite_önerisi_5 = int((((beta / 100 * kapasite5 * df_grouped[df_grouped["Gün"] == gün_bilgisi5]["Acente_3_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite5 * alpha / 100 * son_Acente_3_Günlük_Skor_5) + ((1-beta /100) * kapasite5 * (1 - alpha / 100) / 4 )).round(0))
acente_4_kapasite_önerisi_5 =  kapasite5 - (acente_1_kapasite_önerisi_5 + acente_2_kapasite_önerisi_5 + acente_3_kapasite_önerisi_5)

acente_1_kapasite_önerisi_6 = int((((beta / 100 * kapasite6 * df_grouped[df_grouped["Gün"] == gün_bilgisi6]["Acente_1_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite6 * alpha / 100 * son_Acente_1_Günlük_Skor_6) + ((1-beta /100) * kapasite6 * (1 - alpha / 100) / 4 )).round(0))
acente_2_kapasite_önerisi_6 = int((((beta / 100 * kapasite6 * df_grouped[df_grouped["Gün"] == gün_bilgisi6]["Acente_2_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite6 * alpha / 100 * son_Acente_2_Günlük_Skor_6) + ((1-beta /100) * kapasite6 * (1 - alpha / 100) / 4 )).round(0))
acente_3_kapasite_önerisi_6 = int((((beta / 100 * kapasite6 * df_grouped[df_grouped["Gün"] == gün_bilgisi6]["Acente_3_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite6 * alpha / 100 * son_Acente_3_Günlük_Skor_6) + ((1-beta /100) * kapasite6 * (1 - alpha / 100) / 4 )).round(0))
acente_4_kapasite_önerisi_6 =  kapasite6 - (acente_1_kapasite_önerisi_6 + acente_2_kapasite_önerisi_6 + acente_3_kapasite_önerisi_6)

acente_1_kapasite_önerisi_7 = int((((beta / 100 * kapasite7 * df_grouped[df_grouped["Gün"] == gün_bilgisi7]["Acente_1_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite7 * alpha / 100 * son_Acente_1_Günlük_Skor_7) + ((1-beta /100) * kapasite7 * (1 - alpha / 100) / 4 )).round(0))
acente_2_kapasite_önerisi_7 = int((((beta / 100 * kapasite7 * df_grouped[df_grouped["Gün"] == gün_bilgisi7]["Acente_2_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite7 * alpha / 100 * son_Acente_2_Günlük_Skor_7) + ((1-beta /100) * kapasite7 * (1 - alpha / 100) / 4 )).round(0))
acente_3_kapasite_önerisi_7 = int((((beta / 100 * kapasite7 * df_grouped[df_grouped["Gün"] == gün_bilgisi7]["Acente_3_Historic_Skor"].iloc[-1]))+((1-beta /100) * kapasite7 * alpha / 100 * son_Acente_3_Günlük_Skor_7) + ((1-beta /100) * kapasite7 * (1 - alpha / 100) / 4 )).round(0))
acente_4_kapasite_önerisi_7 =  kapasite7 - (acente_1_kapasite_önerisi_7 + acente_2_kapasite_önerisi_7 + acente_3_kapasite_önerisi_7)

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
    st.write(f""" {d1} , {gün_bilgisi1} günü kapasite dağılım önerisi: 
      Acente 1: {acente_1_kapasite_önerisi_1},
      Acente 2: {acente_2_kapasite_önerisi_1},
      Acente 3: {acente_3_kapasite_önerisi_1},
      Acente 4: {acente_4_kapasite_önerisi_1}""")
    st.write(f""" {d2} , {gün_bilgisi2} günü kapasite dağılım önerisi: 
      Acente 1: {acente_1_kapasite_önerisi_2},
      Acente 2: {acente_2_kapasite_önerisi_2},
      Acente 3: {acente_3_kapasite_önerisi_2},
      Acente 4: {acente_4_kapasite_önerisi_2}""")
    st.write(f""" {d3} , {gün_bilgisi3} günü kapasite dağılım önerisi: 
      Acente 1: {acente_1_kapasite_önerisi_3},
      Acente 2: {acente_2_kapasite_önerisi_3},
      Acente 3: {acente_3_kapasite_önerisi_3},
      Acente 4: {acente_4_kapasite_önerisi_3}""")
    st.write(f""" {d4} , {gün_bilgisi4} günü kapasite dağılım önerisi: 
      Acente 1: {acente_1_kapasite_önerisi_4},
      Acente 2: {acente_2_kapasite_önerisi_4},
      Acente 3: {acente_3_kapasite_önerisi_4},
      Acente 4: {acente_4_kapasite_önerisi_4}""")
    st.write(f""" {d5} , {gün_bilgisi5} günü kapasite dağılım önerisi: 
      Acente 1: {acente_1_kapasite_önerisi_5},
      Acente 2: {acente_2_kapasite_önerisi_5},
      Acente 3: {acente_3_kapasite_önerisi_5},
      Acente 4: {acente_4_kapasite_önerisi_5}""")
    st.write(f""" {d6} , {gün_bilgisi6} günü kapasite dağılım önerisi: 
      Acente 1: {acente_1_kapasite_önerisi_6},
      Acente 2: {acente_2_kapasite_önerisi_6},
      Acente 3: {acente_3_kapasite_önerisi_6},
      Acente 4: {acente_4_kapasite_önerisi_6}""")
    st.write(f""" {d7} , {gün_bilgisi7} günü kapasite dağılım önerisi: 
      Acente 1: {acente_1_kapasite_önerisi_7},
      Acente 2: {acente_2_kapasite_önerisi_7},
      Acente 3: {acente_3_kapasite_önerisi_7},
      Acente 4: {acente_4_kapasite_önerisi_7}""")
