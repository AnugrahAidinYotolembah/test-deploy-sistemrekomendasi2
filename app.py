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
        <h2 style='text-align: center; color: #000000;'>Implementasi Sistem Rekomendasi Penjualan produk Pelatihan Terbaik menggunakan algoritma Cosine Similarity<br>(studi kasus : PT MENARA INDONESIA)</h2>
        <hr style='border: 2px solid #FFFFEC;'>
        <br>
        <h2 style='text-align: center; color: #000000;'>Rekomendasi Produk Pelatihan Terbaik</h2>
        <br>
        """,
        unsafe_allow_html=True
    )

    
    # Pilihan list up-down untuk kebutuhan pelatihan
    options = ["Production Control With Kanban","ProResolve Production Genius","TroubleSolver TechCraft",
               "InnovateEase Production Solutions", "MasterMind ProblemSolve Suite","Project Management & Assertive User Handling",
               "Modern Project Management: Telling, Doodly, Storyline and Video-Sound",
               "Compherensive Train The Trainers (Indoor-outdoor) Activity",
               "Train The Trainer For Outbound",
               "Mastering 10 Core Trainer’s Tools", "Design Thinking: Creating Innovative Product, Excellent Services and Powerful Selling",
               "Innovation Catalyst",
               "Pusat Inovasi Pengembangan Produk",
               "Innovation Solutions Suite for Product Development",
               "Mastery Tools for Product Innovation", "Creative Promotion & Campaign Management",
               "Innovative Business Thinking & Productive",
               "Innovative Leadership for Changes",
               "Combining Scrum & Sprint",
               "Creativity with IDEO & XQ Principles","Pemahaman Pasar TrenAnalitik",
               "Marketing Research For Business Using SPSS",
               "TrendProbe Advanced Research","Trend Market Analysis","Navigator Tren Pasar Data riset", "Leaders As A Coach & Sales Team Developer",
               "Leaders as a Coach & Team Developer in Collection",
               "Paket Pengawasan MonitorWise", "Guardian Tools for Smart Monitoring", "Watchtower Tech for SupervisionPlus","Risk & Governance in Digital Era",
               "Information Security Awareness",
               "Electronic Filing & Document Management System",
               "Understanding Millenials - Managing for High Performance and Engagement", "Professional Digital Marketing",
               "Extraordinary Digital Presentation, Public Speaking & Training Delivery Skills", "Pandai Bicara Profesional Suite",
               "KomunikaCerdas Pelatihan Bahasa", "Suaraku Jelas Modul Komunikasi", "Optimalisasi Social Media Branding Menggunakan Storytelling",
               "Presentation & Selling Skills Using Story-Telling", "ExpressVista Communication Canvas",
               "ImagineFlow Creative Communique", "Dinamika Kreatif TrenTalk", "Warehouse Administration for Better Complete Beginner",
               "Manajemen Pembelian, PPIC, Pergudangan & Negosiasi Pengadaan","perencanaan produksi Cerdas",
               "Strategi finansial dalam  Perencana produksi",
               "perencanaan Optimalisasi Pengelolaan Produksi", "Hak dan Kewajiban Pegawai di Era New Normal: Adaptasi Kebijakan Baru pasca Covid 19",
               "Hukum Bisnis Indonesia Consult", "Legal Maju Pengetahuan Bisnis IndoLaw",
               "Aspek Hukum CorporateWise IndoLegal", "Hukum Perusahaan Indonesia", "System Application & Technology Knowledge & Skill for Transaction",
               "Electronic Filing preparing for BlockChain, IOT",
               "bantuan layanan Troubleshoot di indonesia", "Mitra Teknologi Dukungan IT Cerdas",
               "Solusi Bantuan Teknologi troubleshoot", "Legal Drafting to Prevent and Anticipate",
               "Risk Analysis: to Reduce Losses and Increase Profits", "Aspek Legal Pembiayaan & Penagihan Kartu Kredit",
               "LawGuard Compliance Solutions", "Wawasan Hukum ComplianceCraft", "Akuisisi Produk Financial Services Melalui Digital Marketing",
               "Program Penguasaan SkillMinds","InnovateLearn Workshop Series", "CreativeFlow Training Experience",
               "Akselerator TalentCraft", "Legal Drafting to Prevent and Anticipate",
               "Strategic Partnership - How to Optimize Partnership Efforts for Your Strategic Goals in New Normal Era",
               "Kursus Penguasaan Wawasan Hukum", "Program Keterampilan Analisis LawCraft",
               "Pelatihan program Analisis Hukum LegalMind", "Excel & PowerPoint for Powerful Business Application",
               "Pelatihan Profesional OfficeSkills", "EfficientOffice Mastery Program", "AdminTech Essentials Workshop Series",
               "DataMastery Administrative Training", "How To Conduct TNA, Creating Training Material & Measuring Training Effectivity",
               "ScholarCraft Research Intensive", "Pelatihan Keunggulan Penelitian DiscoverMind", "ScholarCraft Research Intensive",
               "DiscoverMind Research Excellence Training", "Powerful Database Analysis & Dashbord Reporting with Excel",
               "Applied Debt Collection Strategy & Tactics", "DataHarbor Analytics Mastery",
               "Insightful Data Mining Techniques", "Strategic Data Collection Tactics", "Leaders As A Coach & Sales Team Developer","Leaders as a Coach & Team Developer in Collection",
               "Penguasaan Komunikasi untuk Pimpinan Tim", "Membangun Tim Efektif melalui Komunikasi",
               "Leadership Communication Strategies", "Project Management & Assertive User Handling",
               "Modern Project Management: Telling, Doodly, Storyline and Video-Sound", "TI Project Management Excellence",
               "Strategic IT Project Leadership", "Agile Project Management for Technology Professionals", "Leaders As A Coach & Sales Team Developer",
               "Leaders as a Coach & Team Developer in Collection",
               "Conflict, Executive Coaching, Change Management and Business Transformation",
               "Mediation Mastery: Resolving Disputes Effectively", "Negotiation Skills for Business Professionals", "Presentation & Selling Skills Using Story-Telling",
               "Effective Communication & Interpersonal Skills", "Advanced Business Communication Strategies",
               "Strategic Communication Excellence", "Professional Communication Mastery", "Understanding Millenials - Managing for High Performance and Engagement",
               "Standard Operating Procedures for Efficient Operations", "Operational Excellence: From Strategy to Execution",
               "Optimizing Business Processes for Efficiency", "Procedures and Processes Optimization Workshop", "Leaders As A Coach & Sales Team Developer",
               "Leaders as a Coach & Team Developer in Collection", "Conflict, Executive Coaching, Change Management and Business Transformation", "Mediation Mastery: Resolving Disputes Effectively",
               "Negotiation Skills for Business Professionals", "Presentation & Selling Skills Using Story-Telling",
               "Effective Communication & Interpersonal Skills", "Advanced Business Communication Strategies",
               "Strategic Communication Excellence", "Professional Communication Mastery", "Understanding Millenials - Managing for High Performance and Engagement",
               "Standard Operating Procedures for Efficient Operations", "Operational Excellence: From Strategy to Execution",
               "Optimizing Business Processes for Efficiency", "Procedures and Processes Optimization Workshop", "Conflict, Executive Coaching, Change Management and Business Transformation",
               "Executive Coaching for Business Transformation", "Strategic Change Management Workshop", "Mediation Mastery: Effective Dispute Resolution",
               "Negotiation Skills for Business Professionals", "Warehouse Administration for Better Complete Beginner",
               "Optimisasi Operasional: Strategi Peningkatan Produktivitas", "Pelatihan Proses Produksi yang Lebih Baik",
               "Mengelola Operasional Bisnis dengan Efektif", "Teknik Efisiensi Proses Produksi Terbaik", "How To Recruit, Interview, Select & Place the Right Employee",
               "Effective Recruitment Strategies Workshop", "Advanced Employee Selection Techniques Training",
               "Recruitment Excellence: Finding the Right Fit", "Mastering the Art of Employee Hiring and Selection", "Marketing Research For Business Using SPSS",
               "Enterprise Solution Selling", "Advanced Marketing and Advertising Techniques", "Strategic Sales Promotion Training",
               "Mastering the Art of Marketing Communication", "Powerful Database Analysis & Dashboard Reporting with Excel",
               "Pelatihan Teknik Analisis yang Mendalam", "Keterampilan Analitis Proaktif",
               "Strategi Analisis Data yang Efektif", "Pelatihan Keterampilan Analisis Bisnis", "System Application & Technology Knowledge & Skill for Transaction",
               "IT Systems Mastery Program", "Advanced Infrastructure Understanding Workshop",
               "Strategic IT Infrastructure Management Training", "IT Infrastructure Excellence Certification", "Information Security Awareness",
               "Understanding Millenials - Managing for High Performance and Engagement", "Kesehatan dan Keselamatan Kerja: Panduan Praktis",
               "Pelatihan Keselamatan Kerja di Lingkungan Kerja", "Kesehatan Pekerjaan dan Keselamatan: Aspek Penting", "Risk Analysis: to Reduce Losses and Increase Profits",
               "Risk & Governance in Digital Era", "Pelatihan Strategi Mengurangi Kerugian dan Meningkatkan Keuntungan",
               "Risiko dan Tata Kelola di Era Digital", "Pelatihan Analisis Risiko Proyek yang Efektif", "Project Management & Assertive User Handling",
               "Modern Project Management: Telling, Doodly, Storyline and Video-Sound",
               "TI Project Management Excellence", "Strategic IT Project Leadership",
               "Agile Project Management for Technology Professionals", "Leaders As A Coach & Sales Team Developer",
               "Leaders as a Coach & Team Developer in Collection",
               "Conflict, Executive Coaching, Change Management and Business Transformation",  "Mediation Mastery: Resolving Disputes Effectively","Negotiation Skills for Business Professionals",
               "Risk Analysis: to Reduce Losses and Increase Profits",
               "Financial Management Mastery", "Strategic Risk and Financial Analysis",
               "ProfitOptics: Financial Decision Excellence", "Quantitative Financial Modeling", "Modern Project Management: Telling, Doodly, Storyline and Video-Sound",
               "Project Lifecycle Insights", "Effective Project Execution Strategies",
               "ProActive Project Management", "Project Lifecycle Mastery", "Enterprise Solution Selling", 
               "Supply Chain Management Mastery", "Strategic Supply Chain Optimization", 
               "Supply Chain Excellence: From Sourcing to Delivery", "Advanced Supply Chain Strategies"

 ]  # Ganti dengan pilihan yang sesuai
    need = st.selectbox("Pilih kebutuhan pelatihan:", options)

    # Button untuk mendapatkan rekomendasi
    if st.button("Dapatkan Rekomendasi"):
        data = pd.read_csv('dataset/AISALES_FITUR 6.csv')
        cosine_sim = joblib.load('models/AISALES_FITURR6.joblib')
        recommendations = need_recommendation(need, data, cosine_sim)

        # Menampilkan header dengan warna dan style
        st.markdown("<h2 style='color: #FFFFFF;'>Rekomendasi Pelatihan:</h2>", unsafe_allow_html=True)
        st.markdown("---")

        # Menampilkan rekomendasi dalam bentuk tabel
        st.table(pd.DataFrame(recommendations))
        
        
if __name__ == '__main__':
    main()
