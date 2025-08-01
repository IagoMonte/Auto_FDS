from Header import HeaderGen
from docx import Document

nome_produto = "Ácido Nítricoasihdgaifdaj lfgdipyafdjagdyiafsdjg adihafdkjagsodu"

doc = HeaderGen(Document(),nome_produto)

nome_arquivo = f'FDS_{nome_produto.replace(" ", "_")}.docx'
doc.save(nome_arquivo)
print(f'Documento \"{nome_arquivo}\" criado com sucesso.')
