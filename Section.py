from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH


def remove_lateral_borders(cell):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    
    for child in tcPr.findall(qn('w:tcBorders')):
        tcPr.remove(child)

    tcBorders = OxmlElement('w:tcBorders')
    
    
    top = OxmlElement('w:top')
    top.set(qn('w:val'), 'single')
    top.set(qn('w:sz'), '8')     
    top.set(qn('w:space'), '0')
    top.set(qn('w:color'), '000000')
    tcBorders.append(top)

    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '8')
    bottom.set(qn('w:space'), '0')
    bottom.set(qn('w:color'), '000000')
    tcBorders.append(bottom)

    for side in ('left', 'right'):
        edge = OxmlElement(f'w:{side}')
        edge.set(qn('w:val'), 'nil')  
        tcBorders.append(edge)

    tcPr.append(tcBorders)

def addTitle(Document,Titulo):
    sectionTitleTBL = Document.add_table(rows=1,cols=2)
    sectionTitleCell = sectionTitleTBL.cell(0,0)
    sectionTitleCell.merge(sectionTitleTBL.cell(0,1))
    sectionTitleCell.paragraphs[0].text = Titulo
    sectionTitleTBL.columns[0].width = Inches(4.5)
    sectionTitleTBL.alignment = WD_TABLE_ALIGNMENT.CENTER
    #sectionTitleTBL.style = 'Table Grid'
    remove_lateral_borders(sectionTitleCell)
    run_title = sectionTitleCell.paragraphs[0].runs[0]
    run_title.font.bold = True
    run_title.font.size = Pt(14)
    run_title.font.name = "Arial"


def set_cell_background(cell, color_hex):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)  # Cor de fundo (ex: 'D9D9D9')
    
    for e in tcPr.findall(qn('w:shd')):
        tcPr.remove(e)
        
    tcPr.append(shd)

def addLine(Document,info,answer,color=False,Aligment='Center'):
    sectionLineTBL = Document.add_table(rows=1,cols=2)
    sectionLineTBL.alignment = WD_TABLE_ALIGNMENT.CENTER
    sectionLineCellQ = sectionLineTBL.cell(0,0)
    sectionLineTBL.columns[0].width= Inches(2.3)
    sectionLineCellQ.paragraphs[0].text = info
    sectionLineCellQ.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    if Aligment == 'Start':
            sectionLineCellQ.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
    run_title = sectionLineCellQ.paragraphs[0].runs[0]
    run_title.font.size = Pt(12)
    run_title.font.name = "Arial"
    
    sectionLineCellI = sectionLineTBL.cell(0,1)
    sectionLineTBL.columns[1].width= Inches(5.2)
    sectionLineCellI.paragraphs[0].text =  answer
    sectionLineCellI.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    if Aligment == 'Start':
            sectionLineCellI.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
    run_title = sectionLineCellI.paragraphs[0].runs[0]
    run_title.font.size = Pt(12)
    run_title.font.name = "Arial"

    if color==True:
        set_cell_background(sectionLineCellI,'d9d9d9')
        set_cell_background(sectionLineCellQ,'d9d9d9')

def addSubTitle(Document,Subtitle, Color = False):
    sectionSubTitleTBL = Document.add_table(rows=1,cols=2)
    sectionSubTitleTBL.alignment = WD_TABLE_ALIGNMENT.CENTER
    sectionSubTitleCell = sectionSubTitleTBL.cell(0,0)
    sectionSubTitleTBL.columns[0].width = Inches(2.3)
    sectionSubTitleTBL.columns[1].width = Inches(5.2)
    sectionSubTitleCell.merge(sectionSubTitleTBL.cell(0,1))
    sectionSubTitleCell.paragraphs[0].text = Subtitle
    run_title = sectionSubTitleCell.paragraphs[0].runs[0]
    run_title.font.bold = True
    run_title.font.size = Pt(12)
    run_title.font.name = "Arial"
    
    if Color == True:
        set_cell_background(sectionSubTitleCell,'d9d9d9')