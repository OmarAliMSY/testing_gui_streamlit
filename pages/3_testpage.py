from pylatex import Document, PageStyle, Head, Foot, MiniPage, \
    StandAloneGraphic, MultiColumn, Tabu, LongTabu, LargeText, MediumText, \
    LineBreak, NewPage, Tabularx, TextColor, simple_page_number,Command,Subsection,Section,Figure, Package, \
    Tabu
from pylatex.utils import bold, NoEscape,escape_latex
import streamlit as st
from PIL import Image
import os
import json

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
# Load data from a file
uploaded_file = st.file_uploader("Load Session state here")

if uploaded_file is not None:
    # Read the contents of the file
    file_contents = uploaded_file.read()
    
    # Parse or process the data as needed
    # For example, you can convert the data to a string and store it in a variable
    loaded_data = json.loads(file_contents)

    # You can then use loaded_data as a dictionary in your app
    st.write("Loaded Data:")
    st.session_state = loaded_data
    st.write(loaded_data)
# Initialize session state for each section's subsections and images
if "subsections_ta" not in st.session_state:
    st.session_state["subsections_ta"] = []
if "section_ta" not in st.session_state:
        st.session_state["section_ta"] = {
            "title": "",
            "content": "",
            "images": []
        }

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
if "tt" not in st.session_state:
    st.session_state["tt"] = ""
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
            return stuff

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

    def generate_latex_table(self,input_data, rows, cols):
        latex_table = "\\begin{center} \\begin{tabular}{|"
        for _ in range(cols):
            latex_table += f"p{{{1/(cols+1)}\\textwidth}}|"
        latex_table += "}\n\\hline\n"
        for i in range(rows):
            for j in range(cols):
                index = i * cols + j
                if index < len(input_data):
                    cell_value = input_data[index]
                else:
                    cell_value = ""
                latex_table += str(cell_value) + " & "
            latex_table = latex_table[:-2]  # Remove the last ' & ' from the row
            latex_table += " \\\\\n\\hline\n"

        latex_table += "\\end{tabular}  \\end{center}"
        self.doc.append(NoEscape(latex_table))
        with self.doc.create(Subsection(title='h!')):
                self.doc.append(NoEscape(latex_table))


    
path_pdf = "pdf_files/"

c1,c2 = st.columns(2)
with c1: 
    author = st.text_input("Author:",key="author")
    date = st.date_input("Date:",key="date")
with c2: 
    tite = st.text_input("Title:",key="title")
    bauteil = st.text_input("Bauteil:",key="bauteil")


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




def add_section(title, label, subsections):
    mydoc.section(i=title, title=title, label=label)

    # Initialize the section if it doesn't exist
    if title not in st.session_state:
        st.session_state[title] = {
            "title": "",
            "content": "",
            "images": [],
            "tables": [],
        }

    # Add the option to add images, subsections, and tables to the section
    if st.button(f"Add Image to {title}", key=f"add_image_{title}"):
        st.session_state[title]["images"].append({
            "caption": ""
        })

    if st.button(f"Add Subsection to {title}", key=f"add_subsection_{title}"):
        subsections[title].append({
            "title": "",
            "content": "",
            "images": [],
        })

    if st.button(f"Add Table to {title}", key=f"add_table_{title}"):
        st.session_state[title]["tables"].append({
            "input_data": [],
            "rows": 0,
            "cols": 0,
        })

    # Display the images, subsections, and tables added to the section
    for i, image_sec in enumerate(st.session_state[title]["images"]):
        caption = st.text_input(f"Caption for Image {i + 1}", value=image_sec["caption"], key=f"im_caption_{title}_{i}")
        mydoc.fig(i=f"{title}_{i}{image_sec}", caption=caption)

    for i, subsection in enumerate(subsections[title]):
        sub_title = st.text_input(f"{title} - Subsection {i + 1} Title", value=subsection["title"], key=f"subsec_title_{title}_{i}")
        subsection["title"] = sub_title
        subsection["content"] = mydoc.subsection(i=f"{title}_{i}", title=sub_title, section=title)

    for i, table_sec in enumerate(st.session_state[title]["tables"]):
        rows = st.slider(min_value=0, max_value=10, step=1, key=f"table_rows_{title}_{i}", label=f"Rows for Table {i + 1}")
        cols = st.slider(min_value=0, max_value=10, step=1, key=f"table_cols_{title}_{i}", label=f"Cols for Table {i + 1}")
        # Create an empty table with the specified rows and cols
        input_data = []
        if cols > 0 and rows >0:
            num_cols = cols
            fig_cols = st.columns(num_cols)
            for row in range(rows):
                for col in range(cols):
                    with fig_cols[col % num_cols]:
                        input_val = st.text_input(label=f'{row},{col}', key=f'input_{row}_{col}')
                        input_data.append(input_val)



        table_sec["input_data"] = input_data
                #input_data.append(col_list)
        if st.button(f"Generate LaTeX Table for Table {i + 1}", key=f"generate_table_{title}_{i}"):
            if rows > 0 and cols > 0:
                input_data = table_sec["input_data"]
                mydoc.generate_latex_table(table_sec["input_data"], rows, cols)
                table_sec["input_data"] = input_data
                table_sec["rows"] = rows
                table_sec["cols"] = cols
                st.session_state[title]["tables"][i] = table_sec



    # Remove Subsection button
    choice_indices = st.multiselect(options=list(((subsections[title]))), label=f"Select subsections to remove from {title}", key=f"remove_subsection_{title}")
    if st.button(f"Remove Subsections from {title}", key=f"remove_button_{title}"):
        subsections[title] = [subsection for i, subsection in enumerate(subsections[title]) if i not in choice_indices]


    
if "sections" not in st.session_state:
    st.session_state["sections"] = ["Testaufbau", "Testbeschreibung","Durchführung","Auswertung"]
    st.session_state["subsections"] = {section: [] for section in st.session_state["sections"]}
sections = st.session_state["sections"]  
subsections = st.session_state["subsections"] 

for section in sections:
    add_section(section, section, subsections)
    mydoc.doc.append(NoEscape(r"\newpage"))

    


#
mydoc.doc.append(NoEscape(st.session_state["tt"]+r'\newpage'))
mydoc.doc.append(NoEscape(r"\newpage \listoffigures \newpage \listoftables"))


    

# Update session state with the show_table value


_,c,_,d= st.columns(4)

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
    with c :
        export_button = st.button("EXP", key="exp_data")
    if export_button:
        with open(os.path.join("pdf_files/","sts.json"), 'w') as json_file:
            json.dump(st.session_state.to_dict(), json_file, indent=4, default=str)  # 'indent=4' is optional for pretty formatting