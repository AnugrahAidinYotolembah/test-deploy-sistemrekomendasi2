import streamlit as st
import pandas as pd
import joblib

def get_recommendations(need, cosine_sim, data):
    search_recommendations = len(data)
    idx = data.loc[(data['need'] == need)].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:search_recommendations+1]
    company_indices = [i[0] for i in sim_scores]
    return data[['training_name']].iloc[company_indices].drop_duplicates()

def need_recommendation(need, data, cosine_sim):
    recommendations = get_recommendations(need, cosine_sim, data)[:10]
    recommendations['score'] = range(1, len(recommendations) + 1)
    recommendations_sorted = recommendations.sort_values(by='score', ascending=True)

    for i, row in recommendations_sorted.iterrows():
        score_percent = (len(recommendations) - row['score'] + 1) / len(recommendations) * 100
        result_string = f"{row['training_name']} (compatibility: {score_percent:.2f}%)"
        recommendations_sorted.loc[i, 'training_name'] = result_string

    recommendations_sorted = recommendations_sorted.drop(['score'], axis=1)
    dict_from_df = recommendations_sorted.to_dict(orient='list')
    return dict_from_df


# Fungsi utama
def main():
    st.set_page_config(page_title="Rekomendasi Produk Pelatihan", page_icon="📚", layout="wide", initial_sidebar_state="expanded", menu_items=None)
    # Mengatur warna latar belakang menjadi putih
    page_bg_img = '''
    <style>
    body {
        background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
        background-size: cover;
        }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    

    # Menambahkan sidebar dengan foto, nama, dan nim
    st.sidebar.title("Profile")
    st.sidebar.image("image/Anugrah Aidin Yotolembah_F55120093.jpg", use_column_width=True)
    st.sidebar.title("Anugrah Aidin Yotolembah")
    st.sidebar.title("F55120093")
    st.sidebar.title("Universitas Tadulako")

    # Judul halaman dengan warna dan style
    st.markdown(
        """
        <h2 style='text-align: center; color: #FFFFFF;'>Implementasi Sistem Rekomendasi Penjualan produk Pelatihan Terbaik menggunakan algoritma Cosine Similarity<br>(studi kasus : PT MENARA INDONESIA)</h2>
        <hr style='border: 2px solid #800000;'>
        <br>
        <h2 style='text-align: center; color: #FFFFFF;'>Rekomendasi Produk Pelatihan Terbaik</h2>
        <br>
        """,
        unsafe_allow_html=True
    )

    # Input text box untuk kebutuhan pelatihan
    need = st.text_input("Masukkan kebutuhan pelatihan:")

    # Button untuk mendapatkan rekomendasi
    if st.button("Dapatkan Rekomendasi"):
        data = pd.read_csv('dataset/AISALES_FITUR 6.csv')
        cosine_sim = joblib.load('models/AISALES_FITURR6.joblib')
        recommendations = need_recommendation(need, data, cosine_sim)

        # Menampilkan header dengan warna dan style
        st.markdown("<h2 style='color: #000000;'>Rekomendasi Pelatihan:</h2>", unsafe_allow_html=True)
        st.markdown("---")

        # Menampilkan rekomendasi dalam bentuk tabel
        st.table(pd.DataFrame(recommendations))
        
        
if __name__ == '__main__':
    main()
