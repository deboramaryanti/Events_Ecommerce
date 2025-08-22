import streamlit as st
from streamlit.components.v1 import html   # ⬅️  tambahkan ini!

def tampilkan_home():
    st.set_page_config(page_title="Home", layout="centered")

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
        <div class="halo-animation">Halo 👋</div>
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
        const text = `Welcome to my portfolio. I hope you're having a great day 😊

In this dashboard, you can explore several analysis and prediction projects that I have developed — and continue to improve.

This portfolio is about showcasing my skills and passion for data science, machine learning, and web development.
Feel free to explore and don't hesitate to reach out if you have any questions or feedback!`;

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
    html(custom_html, height=380)

    st.success("Click the menu on the side to start exploring 👈")
    st.caption("Version 1.0 | Made with ❤️ using Streamlit")