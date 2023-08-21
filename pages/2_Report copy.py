from pylatex import Document, Section, Subsection, Command, Figure
from pylatex.utils import italic, NoEscape
import streamlit as st
from PIL import Image

# Initialize session state for each section's subsections and images
if "subsections_ta" not in st.session_state:
    st.session_state["subsections_ta"] = []

if "figs_ta" not in st.session_state:
    st.session_state["figs_ta"] = []

if "subsections_tb" not in st.session_state:
    st.session_state["subsections_tb"] = []

if "figs_tb" not in st.session_state:
    st.session_state["figs_tb"] = []

if "subsections_durch" not in st.session_state:
    st.session_state["subsections_durch"] = []

if "figs_durch" not in st.session_state:
    st.session_state["figs_durch"] = []

if "subsections_aus" not in st.session_state:
    st.session_state["subsections_aus"] = []

if "figs_aus" not in st.session_state:
    st.session_state["figs_aus"] = []

class MyDoc:
    def __init__(self):
        self.doc = Document("basic")
        self.sec_counter = 0
        self.im_counter = 0

    def section(self, i, title="", label=""):
        with self.doc.create(Section(title)):
            stuff = st.text_area(label, key="sec" + str(i))
            self.doc.append(stuff)

    def subsection(self, i, title="", label=""):
        with self.doc.create(Subsection(title)):
            stuff = st.text_area(label, key="subsec" + str(i))
            self.doc.append(stuff)

    def fig(self, i, caption):
        images = st.file_uploader("Upload Image here", key="fig" + str(i))
        if images:
            image = Image.open(images)
            image.save(f"pdf_files/img{i}.png")
            image_path = f"img{i}.png"
            
            
            with self.doc.create(Figure(position='h!')) as kitten_pic:
                kitten_pic.add_image(image_path, width='360px')
                kitten_pic.add_caption(caption)

path_pdf = "pdf_files/"

author = st.text_input("Author:")
date = st.date_input("Date")
tite = st.text_input("Title:")

mydoc = MyDoc()
mydoc.doc.preamble.append(Command('title', tite))
mydoc.doc.preamble.append(Command('author', author))
mydoc.doc.preamble.append(Command('date', date))
mydoc.doc.append(NoEscape(r'\maketitle'))
mydoc.doc.append(NoEscape(r'\newpage'))
mydoc.doc.append(NoEscape(r'\tableofcontents'))
mydoc.doc.append(NoEscape(r'\newpage'))

ta = st.container()
tb = st.container()
durch = st.container()
aus = st.container()
with ta:
    st.header("Testaufbau")
    mydoc.section(i="ta",title="Testaufbau",label="Testaufbau")
    if st.button("Add Subsection", key="asta"):
        st.session_state["subsections_ta"].append({
            "title": "",
            "content": "",
            "images": []
        })

    for i, subsection in enumerate(st.session_state["subsections_ta"]):
        title = st.text_input(f"Subsection {i+1} Title", value=subsection["title"], key=f"subsec_title_ta_{i}")
        content = st.text_area(f"Subsection {i+1} Content", value=subsection["content"], key=f"subsec_content_ta_{i}")
        st.session_state["subsections_ta"][i]["title"] = title
        st.session_state["subsections_ta"][i]["content"] = content

        mydoc.subsection(i=f"ta{i}", title=title, label=content) 
        if st.button(f"Add Image to Subsection {i+1}", key=f"add_image_ta_{i}"):
            subsection["images"].append({
                "caption": ""
            })

        for j, image in enumerate(subsection["images"]):
            caption = st.text_input(f"Caption {j+1} Title", value=image["caption"], key=f"im_title_ta_{i}_{j}")
            subsection["images"][j]["caption"] = caption
            mydoc.fig(i=f"ta{i}_{j}", caption=caption)  # Call mydoc.fig for the added image
mydoc.doc.append(NoEscape(r'\newpage'))

with tb:
    st.header("Testbeschreibung")
    mydoc.section(i="tb", title="Testbeschreibung", label="Testbeschreibung")

    if st.button("Add Subsection", key="astb"):
        st.session_state["subsections_tb"].append({
            "title": "",
            "content": "",
            "images": []
        })

    for i, subsection in enumerate(st.session_state["subsections_tb"]):
        title = st.text_input(f"Subsection {i+1} Title", value=subsection["title"], key=f"subsec_title_tb_{i}")
        content = st.text_area(f"Subsection {i+1} Content", value=subsection["content"], key=f"subsec_content_tb_{i}")
        st.session_state["subsections_tb"][i]["title"] = title
        st.session_state["subsections_tb"][i]["content"] = content

        if st.button(f"Add Image to Subsection {i+1}", key=f"tb_add_image_{i}"):
            subsection["images"].append({
                "caption": ""
            })

        for j, image in enumerate(subsection["images"]):
            caption = st.text_input(f"Caption {j+1} Title", value=image["caption"], key=f"tbim_title_tb_{i}_{j}")
            subsection["images"][j]["caption"] = caption
            mydoc.fig(i=f"tb{i}_{j}", caption=caption)
            
        mydoc.subsection(i=f"tb{i}", title=title, label=content)  # Add this line to create the subsection in the PDF
mydoc.doc.append(NoEscape(r'\newpage'))


with durch:
    st.header("Durchführung")
    mydoc.section(i="du", title="Durchführung", label="Durchführung")

    if st.button("Add Subsection", key="asdurch"):
        st.session_state["subsections_durch"].append({
            "title": "",
            "content": "",
            "images": []
        })

    for i, subsection in enumerate(st.session_state["subsections_durch"]):
        title = st.text_input(f"Subsection {i+1} Title", value=subsection["title"], key=f"subsec_title_durch_{i}")
        content = st.text_area(f"Subsection {i+1} Content", value=subsection["content"], key=f"subsec_content_durch_{i}")
        st.session_state["subsections_durch"][i]["title"] = title
        st.session_state["subsections_durch"][i]["content"] = content

        if st.button(f"Add Image to Subsection {i+1}", key=f"durch_add_image_{i}"):
            subsection["images"].append({
                "caption": ""
            })

        for j, image in enumerate(subsection["images"]):
            caption = st.text_input(f"Caption {j+1} Title", value=image["caption"], key=f"im_title_durch_{i}_{j}")
            subsection["images"][j]["caption"] = caption
            mydoc.subsection(i=f"du{i}", title=title, label=content)  # Use content from st.text_area

mydoc.doc.append(NoEscape(r'\newpage'))


with aus:
    st.header("Auswertung")
    mydoc.section(i="aus", title="Auswertung", label="Auswertung")

    if st.button("Add Subsection", key="asaus"):
        st.session_state["subsections_aus"].append({
            "title": "",
            "content": "",
            "images": []
        })

    for i, subsection in enumerate(st.session_state["subsections_aus"]):
        title = st.text_input(f"Subsection {i+1} Title", value=subsection["title"], key=f"subsec_title_aus_{i}")
        content = st.text_area(f"Subsection {i+1} Content", value=subsection["content"], key=f"subsec_content_aus_{i}")
        st.session_state["subsections_aus"][i]["title"] = title
        st.session_state["subsections_aus"][i]["content"] = content

        if st.button(f"Add Image to Subsection {i+1}", key=f"aus_add_image_{i}"):
            subsection["images"].append({
                "caption": ""
            })

        for j, image in enumerate(subsection["images"]):
            caption = st.text_input(f"Caption {j+1} Title", value=image["caption"], key=f"im_title_aus_{i}_{j}")
            subsection["images"][j]["caption"] = caption
            mydoc.subsection(i=f"aus{i}", title=title, label=content)  # Use content from st.text_area

mydoc.doc.append(NoEscape(r'\newpage'))
save_button = st.button("Save", key="save_data")

if save_button:
    mydoc.doc.generate_pdf(path_pdf + 'Test_Report', clean_tex=False)
    tex = mydoc.doc.dumps()  # The document as string in LaTeX syntax
    with open("pdf_files/Test_Report.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(label="Export_Report",
                       data=PDFbyte,
                       file_name="test.pdf",
                       mime='application/octet-stream')
