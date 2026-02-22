import streamlit as st
import os
import json
import uuid
from PIL import Image

# ======================================================
# CONFIG
# ======================================================
st.set_page_config(page_title="GS Library", layout="wide")

ADMIN_PASSWORD = "admin123"
DATA_FILE = "library.json"
IMAGE_FOLDER = "images"

os.makedirs(IMAGE_FOLDER, exist_ok=True)

# ======================================================
# LOAD / SAVE
# ======================================================
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

library = load_data()

# ======================================================
# SIDEBAR NAVIGATION
# ======================================================
menu = st.sidebar.radio("Navigation", ["📚 GS Library", "🔐 Admin Panel"])

# ======================================================
# VIEW LIBRARY
# ======================================================
if menu == "📚 GS Library":

    st.title("📚 GS Library – Stock Market Knowledge")

    if not library:
        st.info("No Books Added Yet.")
    else:
        for book in library:

            with st.expander(f"📖 {book['name']} | Subject: {book['subject']}"):

                for chapter in book["chapters"]:

                    st.subheader(f"📘 {chapter['title']}")

                    st.write(chapter["content"])

                    if chapter["image"] and os.path.exists(chapter["image"]):
                        st.image(chapter["image"], use_container_width=True)

                    st.markdown("---")

# ======================================================
# ADMIN PANEL
# ======================================================
if menu == "🔐 Admin Panel":

    password = st.text_input("Enter Admin Password", type="password")

    if password == ADMIN_PASSWORD:

        st.success("Admin Access Granted ✅")

        tab1, tab2 = st.tabs(["➕ Add Book", "➕ Add Chapter"])

        # ==================================================
        # ADD BOOK
        # ==================================================
        with tab1:

            st.subheader("Create New Book")

            book_name = st.text_input("Book Name")
            subject = st.text_input("Subject")

            if st.button("Save Book"):

                new_book = {
                    "id": str(uuid.uuid4()),
                    "name": book_name,
                    "subject": subject,
                    "chapters": []
                }

                library.append(new_book)
                save_data(library)

                st.success("Book Created Successfully 📖")

        # ==================================================
        # ADD CHAPTER
        # ==================================================
        with tab2:

            if not library:
                st.warning("Create a Book First")
            else:
                book_options = {book["name"]: book["id"] for book in library}

                selected_book = st.selectbox("Select Book", list(book_options.keys()))

                chapter_title = st.text_input("Chapter Title")

                chapter_content = st.text_area(
                    "Write or Paste Your Notes",
                    height=250
                )

                image_file = st.file_uploader(
                    "Upload Image (Optional)",
                    type=["png", "jpg", "jpeg"]
                )

                if st.button("Save Chapter"):

                    for book in library:
                        if book["id"] == book_options[selected_book]:

                            image_path = ""

                            if image_file:
                                image_name = f"{uuid.uuid4()}.png"
                                image_path = os.path.join(IMAGE_FOLDER, image_name)
                                with open(image_path, "wb") as f:
                                    f.write(image_file.getbuffer())

                            new_chapter = {
                                "id": str(uuid.uuid4()),
                                "title": chapter_title,
                                "content": chapter_content,
                                "image": image_path
                            }

                            book["chapters"].append(new_chapter)
                            save_data(library)

                            st.success("Chapter Added Successfully 📘")
                            break

    else:
        st.warning("Enter correct password")
