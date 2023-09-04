from pylatex import Document, PageStyle, Head, Foot, MiniPage, \
    StandAloneGraphic, MultiColumn, Tabu, LongTabu, LargeText, MediumText, \
    LineBreak, NewPage, Tabularx, TextColor, simple_page_number,Command,Subsection,Section,Figure, Package
from pylatex.utils import bold, NoEscape,escape_latex
import streamlit as st
from PIL import Image
import os
st.set_page_config(
    page_title="Data Acquisition",
    page_icon=r"favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })
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
        self.geometry_options = {
        "head": "40pt",
        "margin": "1.0in",
        "bottom": "0.6in",
        "includeheadfoot": True
    }
        self.doc = Document("basic",geometry_options=self.geometry_options)
        self.sec_counter = 0
        self.im_counter = 0
    def title_page(self, author, date, title,bauteil):
        template_path = r"pdf_files\titlepage.tex"
        with open(template_path, "r") as template_file:
            template_content = template_file.read()
        image_path="MSG-Signet-Schwarz-CMYK-170414-01.png"
        image_path2 = "MSG-Signet-Schwarz-CMYK-170414-02.png"
        
        # Replace placeholders with actual values
        template_content = template_content.replace("__IMAGE_PATH__", image_path)
        template_content = template_content.replace("__BT__", bauteil)

        template_content = template_content.replace("__IMAGE_PATH2__", image_path2)
        template_content = template_content.replace("__TITLE__", title)
        template_content = template_content.replace("__AUTHOR__", author)
        template_content = template_content.replace("__DATE__", str(date))

        # Add the title page to the document
        self.doc.append(NoEscape(template_content))
        self.doc.append(NoEscape(r'\newpage'))
        self.doc.append(NoEscape(r'\tableofcontents'))
        self.doc.append(NoEscape(r'\newpage'))

    def section(self, i, title="", label=""):
        with self.doc.create(Section(title)):
            stuff = NoEscape(st.text_area(label, key="sec" + str(i)))
            self.doc.append(stuff)

    def subsection(self, i, title="", section=""):
        with self.doc.create(Subsection(title)):
            stuff = NoEscape(st.text_area(f"{section}: Subsection", key="subsec" + str(i)))
            self.doc.append(stuff)

    def fig(self, i, caption):
        images = st.file_uploader("Upload Image here", key="fig" + str(i))
        scale = st.slider(min_value=0.0,max_value=1.0,step=0.1,key=f"img{i}",label="Scale")
        if images:
            image = Image.open(images)
            image.save(f"pdf_files/img{i}.png")
            image_path = f"img{i}.png"
            
            
            with self.doc.create(Figure(position='h!')) as pic:
                pic.add_image(image_path, width=NoEscape(f"{scale}"+r"\textwidth"))
                pic.add_caption(caption)


path_pdf = "pdf_files/"

c1,c2 = st.columns(2)
with c1: 
    author = st.text_input("Author:")
    date = st.date_input("Date")
with c2: 
    tite = st.text_input("Title:")
    bauteil = st.text_input("Bauteil:")


mydoc = MyDoc()

header= PageStyle("header")
header.change_thickness(element="header",thickness=0.5)
header.change_thickness(element="footer",thickness=0.5)

with header.create(Head("L")):
    header.append("")
# Create center header
with header.create(Head("L")):
    header.append(NoEscape(r'\nouppercase{\leftmark}'))
# Create right header
with header.create(Head("R")):
    header.append(StandAloneGraphic(filename=r"MSG-Signet-Schwarz-CMYK-170414-02.png",image_options="height=1cm"))
# Create right footer
with header.create(Foot("R")):
    header.append(NoEscape( r'\thepage'))
# Create left footer
with header.create(Foot("L")):
    header.append(str(date))
# Create right footer
with header.create(Foot("C")):
    header.append(tite)

mydoc.doc.preamble.append(header)
mydoc.doc.change_document_style("header")
mydoc.doc.packages.append(Package('graphicx'))
mydoc.doc.packages.append(Package('hyperref'))
mydoc.doc.preamble.append(NoEscape(r"\hypersetup{colorlinks=true,citecolor=black,filecolor=black,linkcolor=black,menucolor=black,urlcolor=black}"))
mydoc.doc.preamble.append(Command('title', tite))
mydoc.doc.preamble.append(Command('author', author))
mydoc.doc.preamble.append(Command('date', date))
mydoc.title_page(author=author, date=date, title=tite,bauteil=bauteil)

t1,t2 = st.columns(2)

ta = st.container()
tb = st.container()
durch = st.container()
aus = st.container()



with ta:
    st.header("Testaufbau")
    mydoc.section(i="ta",title="Testaufbau",label="Testaufbau")
    # Add the option to add images to the section
    if st.button("Add Image to Section", key="add_image_ta"):
        st.session_state["figs_ta"].append({
        "caption": ""
    })
    # Display the images added to the section
    for i, image in enumerate(st.session_state["figs_ta"]):
        caption = st.text_input(f"Caption for Image {i+1}", value=image["caption"], key=f"im_caption_ta_{i}")
        st.session_state["figs_ta"][i]["caption"] = caption
        mydoc.fig(i=f"ta_{i}{image}", caption=caption)


    if st.button("Add Subsection", key="asta"):
        st.session_state["subsections_ta"].append({
            "title": "",
            "content": "",
            "images": []
        })

    for i, subsection in enumerate(st.session_state["subsections_ta"]):
        title = st.text_input(f"Subsection {i+1} Title", value=subsection["title"], key=f"subsec_title_ta_{i}")
        #content = st.text_area(f"Subsection {i+1} Content", value=subsection["content"], key=f"subsec_content_ta_{i}")
        st.session_state["subsections_ta"][i]["title"] = title
        #st.session_state["subsections_ta"][i]["content"] = content

        mydoc.subsection(i=f"ta{i}", title=title, section=f"Testaufbau") 
        if st.button(f"Add Image to Subsection {i+1}", key=f"add_image_ta_{i}"):
            subsection["images"].append({
                "caption": ""
            })

        for j, image in enumerate(subsection["images"]):
            caption = st.text_input(f"Caption {j+1} Title", value=image["caption"], key=f"im_title_ta_{i}_{j}")
            subsection["images"][j]["caption"] = caption

            mydoc.fig(i=f"ta{i}_{j}", caption=caption)  # Call mydoc.fig for the added image
    choice_indices = st.multiselect(options=list(range(len(st.session_state["subsections_ta"]))), label="Select subsections to remove",key="msta")
    remove_button3 = st.button("Remove", key="remove_data_ta")

    if remove_button3:
        st.session_state["subsections_ta"] = [subsection for i, subsection in enumerate(st.session_state["subsections_ta"]) if i not in choice_indices]
        remove_button = False
    print(st.session_state["subsections_ta"])
mydoc.doc.append(NoEscape(r'\newpage'))

with tb:
    st.header("Testbeschreibung")
    mydoc.section(i="tb", title="Testbeschreibung", label="Testbeschreibung")
    if st.button("Add Image to Section", key="add_image_tb"):
        st.session_state["figs_tb"].append({
        "caption": ""
        })

    # Display the images added to the section
    for i, image in enumerate(st.session_state["figs_tb"]):
        caption = st.text_input(f"Caption for Image {i+1}", value=image["caption"], key=f"im_caption_tb_{i}")
        st.session_state["figs_tb"][i]["caption"] = caption
        mydoc.fig(i=f"ta_{i}", caption=caption)

    if st.button("Add Subsection", key="astb"):
        st.session_state["subsections_tb"].append({
            "title": "",
            "content": "",
            "images": []
        })

    for i, subsection in enumerate(st.session_state["subsections_tb"]):
        title = st.text_input(f"Subsection {i+1} Title", value=subsection["title"], key=f"subsec_title_tb_{i}")
        #content = st.text_area(f"Subsection {i+1} Content", value=subsection["content"], key=f"subsec_content_tb_{i}")
        st.session_state["subsections_tb"][i]["title"] = title
        #st.session_state["subsections_tb"][i]["content"] = content

        mydoc.subsection(i=f"tb{i}", title=title, section="Testbeschreibung")  # Add this line to create the subsection in the PDF
        if st.button(f"Add Image to Subsection {i+1}", key=f"tb_add_image_{i}"):
            subsection["images"].append({
                "caption": ""
            })

        for j, image in enumerate(subsection["images"]):
            caption = st.text_input(f"Caption {j+1} Title", value=image["caption"], key=f"tbim_title_tb_{i}_{j}")
            subsection["images"][j]["caption"] = caption
            mydoc.fig(i=f"tb{i}_{j}", caption=caption)
        choice_indices = st.multiselect(options=list(range(len(st.session_state["subsections_tb"]))), label="Select subsections to remove",key="mstb")
        remove_button2 = st.button("Remove", key="remove_data_tb")

        if remove_button2:
            st.session_state["subsections_tb"] = [subsection for i, subsection in enumerate(st.session_state["subsections_tb"]) if i not in choice_indices]
            remove_button = False

mydoc.doc.append(NoEscape(r'\newpage'))


with durch:
    st.header("Durchführung")
    mydoc.section(i="du", title="Durchführung", label="Durchführung")
    if st.button("Add Image to Section", key="add_image_durch"):
        st.session_state["figs_durch"].append({
        "caption": ""
        })
        
    # Display the images added to the section
    for i, image in enumerate(st.session_state["figs_durch"]):
        caption = st.text_input(f"Caption for Image {i+1}", value=image["caption"], key=f"im_caption_durch_{i}")
        st.session_state["figs_durch"][i]["caption"] = caption
        mydoc.fig(i=f"durch_{i}", caption=caption)
    if st.button("Add Subsection", key="asdurch"):
        st.session_state["subsections_durch"].append({
            "title": "",
            "content": "",
            "images": []
        })

    for i, subsection in enumerate(st.session_state["subsections_durch"]):
        title = st.text_input(f"Subsection {i+1} Title", value=subsection["title"], key=f"subsec_title_durch_{i}")
        #content = st.text_area(f"Subsection {i+1} Content", value=subsection["content"], key=f"subsec_content_durch_{i}")
        st.session_state["subsections_durch"][i]["title"] = title
        #st.session_state["subsections_durch"][i]["content"] = content

        mydoc.subsection(i=f"du{i}", title=title, section="Duchführung")  # Use content from st.text_area
        if st.button(f"Add Image to Subsection {i+1}", key=f"durch_add_image_{i}"):
            subsection["images"].append({
                "caption": ""
            })

        for j, image in enumerate(subsection["images"]):
            caption = st.text_input(f"Caption {j+1} Title", value=image["caption"], key=f"im_title_durch_{i}_{j}")
            subsection["images"][j]["caption"] = caption
            mydoc.fig(i=f"durch{i}_{j}", caption=caption)

        choice_indices = st.multiselect(options=list(range(len(st.session_state["subsections_durch"]))), label="Select subsections to remove",key="msdurch")
        remove_button1 = st.button("Remove", key="remove_data_durch")

        if remove_button1:
            st.session_state["subsections_durch"] = [subsection for i, subsection in enumerate(st.session_state["subsections_durch"]) if i not in choice_indices]
            remove_button = False
mydoc.doc.append(NoEscape(r'\newpage'))


with aus:
    st.header("Auswertung")
    mydoc.section(i="aus", title="Auswertung", label="Auswertung")
    if st.button("Add Image to Section", key="add_image_aus"):
        st.session_state["figs_aus"].append({
        "caption": ""
        })
    # Display the images added to the section
    for i, image in enumerate(st.session_state["figs_aus"]):
        caption = st.text_input(f"Caption for Image {i+1}", value=image["caption"], key=f"im_caption_aus_{i}")
        st.session_state["figs_aus"][i]["caption"] = caption
        mydoc.fig(i=f"aus_{i}", caption=caption)
    if st.button("Add Subsection", key="asaus"):
        st.session_state["subsections_aus"].append({
            "title": "",
            "images": []
        })

    for i, subsection in enumerate(st.session_state["subsections_aus"]):
        title = st.text_input(f"Subsection {i+1} Title", value=subsection["title"], key=f"subsec_title_aus_{i}")
        #content = st.text_area(f"Subsection {i+1} Content", value=subsection["content"], key=f"subsec_content_aus_{i}")
        st.session_state["subsections_aus"][i]["title"] = title
        #st.session_state["subsections_aus"][i]["content"] = content

        mydoc.subsection(i=f"aus{i}", title=title, section="Auswertung")  # Use content from st.text_area
        if st.button(f"Add Image to Subsection {i+1}", key=f"aus_add_image_{i}"):
            subsection["images"].append({
                "caption": ""
            })

        for j, image in enumerate(subsection["images"]):
            caption = st.text_input(f"Caption {j+1} Title", value=image["caption"], key=f"im_title_aus_{i}_{j}")
            subsection["images"][j]["caption"] = caption
            mydoc.fig(i=f"aus{i}_{j}", caption=caption)

    choice_indices = st.multiselect(options=list(range(len(st.session_state["subsections_aus"]))), label="Select subsections to remove")
    remove_button = st.button("Remove", key="aus_remove_data")

    if remove_button:
        st.session_state["subsections_aus"] = [subsection for i, subsection in enumerate(st.session_state["subsections_aus"]) if i not in choice_indices]
        remove_button = False
    mydoc.doc.append(NoEscape(r'\newpage'))





_,c,_= st.columns(3)

with c :
    save_button = st.button("Compile", key="save_data")


    if save_button:
        with st.spinner('Compiling...'):
            mydoc.doc.generate_pdf(path_pdf + 'Test_Report', clean_tex=False)
            st.success('Done!')

        tex = mydoc.doc.dumps()  # The document as string in LaTeX syntax
        with open("pdf_files/Test_Report.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        st.download_button(label="Download PDF",
                            data=PDFbyte,
                            file_name=f"{tite}.pdf",
                            mime='application/octet-stream')
