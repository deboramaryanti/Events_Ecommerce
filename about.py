import streamlit as st
from streamlit.components.v1 import html
from streamlit_option_menu import option_menu
import os

def tampilkan_about():
    # Buat 3 kolom kosong, taruh gambar di kolom tengah
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if os.path.exists("Pict.jpg"):
            st.image("Pict.jpg", width=300)
        else:
            st.warning("Profile picture not found.")

    # Animasi teks "Halo 👋"
    st.markdown("""
        <style>
        .halo-animation {
            font-size: 40px;
            font-weight: bold;
            color: #4A90E2;
            margin: 20px auto;
            text-align: center;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.1); opacity: 0.7; }
            100% { transform: scale(1); opacity: 1; }
        }
        </style>

        <div class="halo-animation">Hi There! 👋</div>
    """, unsafe_allow_html=True)

    # Animasi typing
    custom_html = """
    <div id="typewriter" style="
        font-family: monospace;
        font-size: 20px;
        color: #4A90E2;
        width: 90%;
        max-width: 700px;
        margin: 30px auto;
        border-right: 2px solid #4A90E2;
        white-space: pre-wrap;
        overflow-wrap: break-word;
        word-wrap: break-word;
        overflow: hidden;
        min-height: 200px;
    "></div>

    <script>
        const text = `I'm Debora Maryanti. 

I'm a results-oriented professional with a background in Physics and over five years of experience in Sales. Currently, I'm transitioning into the field of Data Science through an intensive training program at DiBimbing Bootcamp. 

By combining my analytical mindset from Physics, business insight from Sales, and technical skills in Python, SQL, and data visualization, I aim to transform complex data into meaningful, actionable insights. 

This portfolio reflects my journey of applying data, logic, and business understanding to solve real-world challenges. I believe data is more than just numbers—it’s a powerful tool to drive smarter decisions. 

Thank you for visiting, and I hope you enjoy exploring my portfolio project!

For more information about me:`;

        let i = 0;
        const speed = 40;

        function typeWriter() {
            if (i < text.length) {
                document.getElementById("typewriter").innerHTML += text.charAt(i);
                i++;
                setTimeout(typeWriter, speed);
            }
        }

        typeWriter();
    </script>
    """
    html(custom_html, height=550)

    # Gunakan session_state untuk menyimpan apakah tombol sudah ditekan
    if "kontak_ditampilkan" not in st.session_state:
        st.session_state.kontak_ditampilkan = False

    if st.button("Show My Contact", key="kontak_button"):
        st.session_state.kontak_ditampilkan = True

    if st.session_state.kontak_ditampilkan:
        st.markdown("---")
        st.subheader("Find me")

        sub = option_menu(
            None,
            ["LinkedIn", "GitHub", "Email", "Instagram"],
            icons=["linkedin", "github", "envelope", "instagram"],
            orientation="vertical",
            key="menu_kontak"
        )

        if sub == "LinkedIn":
            st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-black)](https://www.linkedin.com/in/deboramaryanti/)")
        elif sub == "GitHub":
            st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-Profile-black)](https://github.com/deboramaryanti)")
        elif sub == "Email":
            st.write("📧 Email: [deboramaryanti@gmail.com](mailto:deboramaryanti@gmail.com)")
        elif sub == "Instagram":
            st.markdown("[![Instagram](https://img.shields.io/badge/Instagram-Profile-black)](https://www.instagram.com/db.raa/)")