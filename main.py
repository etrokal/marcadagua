from tkinter import filedialog
from tkinter import *
import PyPDF2
import os

class Application:
    def __init__(self, root=None):
        self.arquivos = []
        self.marcaDagua = None

        # Hook destroy event to root
        self.root = root
        root.protocol('WM_DELETE_WINDOW', self.destroy)

        self.frame = Frame(root)
        self.frame.grid()

        self.statusMsg = Label(self.frame, text="Nenhum arquivo selecionado")
        self.statusMsg.grid(row=0, column=0, columnspan=2,
                            sticky=W+E, padx=50, pady=20)

        self.btnSelecionarArquivos = Button(self.frame)
        self.btnSelecionarArquivos["text"] = "Selecionar arquivos"
        self.btnSelecionarArquivos["command"] = self.abrirDialogoDeArquivos
        self.btnSelecionarArquivos.grid(row=1, column=0, padx=10, pady=10)

        self.btnSelecionarMarcaDagua = Button(self.frame)
        self.btnSelecionarMarcaDagua["text"] = "Selecionar Marca D'água"
        self.btnSelecionarMarcaDagua["command"] = self.abrirDialogoMarcaDagua
        self.btnSelecionarMarcaDagua.grid(row=1, column=1, padx=10, pady=10)

        self.btnAplicarMarcaDagua = Button(self.frame)
        self.btnAplicarMarcaDagua["text"] = "Aplicar Marca D'Água"
        self.btnAplicarMarcaDagua["command"] = self.aplicarMarcaDagua
        self.btnAplicarMarcaDagua.grid(row=2, column=0, columnspan=2)

    def destroy(self):
        self.closeFiles()
        self.root.destroy()

    def closeFiles(self):
        for arquivo in self.arquivos:
            arquivo.close()
            
        if self.marcaDagua:
            self.marcaDagua.close()

    def abrirDialogoDeArquivos(self):
        self.arquivos = filedialog.askopenfiles(
            mode="rb", filetypes=[("PDF", "*.pdf")])
        self.atualizarMensagem()

    def abrirDialogoMarcaDagua(self):
        self.marcaDagua = filedialog.askopenfile(
            mode="rb", filetypes=[("PDF", "*.pdf")])
        # assert(isinstance(self.marcaDagua, object))
        self.atualizarMensagem()

    def aplicarMarcaDagua(self):
        if len(self.arquivos) == 0:
            return

        arquivo = self.arquivos[0]

        # criar diretorio se não existir
        caminho_do_arquivo = os.path.dirname(os.path.realpath(arquivo.name))
        nome_arquivo = os.path.basename(os.path.realpath(arquivo.name))
        caminho_diretorio = os.path.join(caminho_do_arquivo, "marcadagua")

        try:
            os.mkdir(caminho_diretorio)
        except FileExistsError:
            print("Diretório de saída já existe.")
            pass

        watermark_file = PyPDF2.PdfFileReader(self.marcaDagua)
        watermark_page = watermark_file.getPage(0)

        for arquivo in self.arquivos:
            # criar referencias para pdfs
            input_pdf = PyPDF2.PdfFileReader(arquivo)
            output = PyPDF2.PdfFileWriter()

            # aplicar marcadagua em todas as páginas
            for input_page in input_pdf.pages:
                input_page.mergePage(watermark_page)
                output.addPage(input_page)

            # salvar arquivo
            output_file = open(os.path.join(caminho_diretorio, nome_arquivo), "wb")
            output.write(output_file)
            output_file.close()
            del(input_pdf)
            del(output)

    def atualizarMensagem(self):
        msgArquivos = ""
        msgMarcaDagua = ""

        numArquivos = len(self.arquivos)
        if numArquivos == 0:
            msgArquivos = "Nenhum arquivo selecionado"
        elif numArquivos == 1:
            msgArquivos = "1 arquivo selecionado"
        else:
            msgArquivos = f"{numArquivos} arquivos selecionados"

        if self.marcaDagua:
            msgMarcaDagua = "Marca D'água selecionada"
        else:
            msgMarcaDagua = ""

        self.statusMsg["text"] = "\n\n".join([msgArquivos, msgMarcaDagua])


root = Tk()
root.geometry("320x240")
Application(root)
root.mainloop()
