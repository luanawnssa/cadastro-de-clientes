from tkinter import *  ### CHAMANDO O TKINTER 
from tkinter import ttk
import sqlite3

root = Tk()  ### CRIANDO VARIAVEL

class Funcs():
    def limpa_cliente(self):
        self.codigo_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
        self.fone_entry.delete(0, END)
        self.nome_entry.delete(0, END)
    
    def conecta_bd(self):
        """Conectar ao banco de dados com o uso do 'with'"""
        try:
            self.conn = sqlite3.connect("clientes.db")
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.conn, self.cursor = None, None
    
    def desconecta_bd(self):
        """Desconectar do banco de dados"""
        if self.conn:
            self.conn.close()

    def montaTabelas(self):  # Cria tabelas dentro do banco de dados
        self.conecta_bd()
        if self.conn:  # Verifica se a conexão foi bem-sucedida
            # Criar tabela
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    cod INTEGER PRIMARY KEY,
                    nome_cliente CHAR(40) NOT NULL,
                    telefone INTEGER(20),
                    cidade CHAR(40)               
                );
            """)
            self.conn.commit() 
            print("Banco de dados criado")
        self.desconecta_bd()

    def variaveis(self):
     self.codigo = self.codigo_entry.get()
     self.nome = self.nome_entry.get()
     self.fone = self.fone_entry.get()
     self.cidade = self.cidade_entry.get()
     
     # Verifica se todos os campos estão preenchidos
     if not self.nome or not self.fone or not self.cidade:
         print("Erro: Preencha todos os campos!")
     else:
         print("Campos preenchidos corretamente")

    def add_cliente(self):  # Adiciona os valores ao banco de dados digitados na tela
        self.variaveis()
        if self.nome and self.fone and self.cidade:  # Verifica se todos os campos estão preenchidos
            self.conecta_bd()  # Conecta ao banco de dados
            if self.conn:  # Verifica se a conexão foi bem-sucedida
                self.cursor.execute("""
                    INSERT INTO clientes (nome_cliente, telefone, cidade)
                    VALUES (?, ?, ?)""", (self.nome, self.fone, self.cidade))
                self.conn.commit()  # Valida os dados
                self.desconecta_bd()
                self.select_lista()
                self.limpa_cliente()
        else:
            print("Preencha todos os campos para adicionar um cliente.")
    
    def select_lista(self):
        """Atualiza a lista de clientes na interface"""
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        if self.conn:
            lista = self.cursor.execute("""
                SELECT cod, nome_cliente, telefone, cidade FROM clientes
                ORDER BY nome_cliente ASC; 
            """)
            for i in lista:
                self.listaCli.insert("", END, values=i)
        self.desconecta_bd()
    
    def OnDoubleClick(self, event):
        """Preenche os campos com os dados do cliente selecionado"""
        self.limpa_cliente()
        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.fone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)
    
    def deleta_cliente(self):
        """Deleta o cliente selecionado"""
        self.variaveis()
        if self.codigo:
            self.conecta_bd()
            if self.conn:
                self.cursor.execute("""DELETE FROM clientes WHERE cod = ?""", (self.codigo,))
                self.conn.commit()
                self.desconecta_bd()
                self.limpa_cliente()
                self.select_lista()
    
    def altera_cliente(self):
        """Altera os dados do cliente selecionado"""
        self.variaveis()
        if self.codigo:
            self.conecta_bd()
            if self.conn:
                self.cursor.execute("""
                    UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ? WHERE cod = ?
                """, (self.nome, self.fone, self.cidade, self.codigo))
                self.conn.commit()
                self.desconecta_bd()
                self.select_lista()
                self.limpa_cliente()

    def busca_cliente(self):
        """Busca clientes pelo nome"""
        self.conecta_bd()
        if self.conn:
            self.listaCli.delete(*self.listaCli.get_children())
            nome = self.nome_entry.get().strip() + '%'
            self.cursor.execute("""
                SELECT cod, nome_cliente, telefone, cidade FROM clientes
                WHERE nome_cliente LIKE ? ORDER BY nome_cliente ASC
            """, (nome,))
            buscas = self.cursor.fetchall()
            for i in buscas:
                self.listaCli.insert("", END, values=i)
            self.limpa_cliente()
            self.desconecta_bd()

class Application(Funcs): ### CONFIGURAÇÃO DA JANELA E FUNÇÕES
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()  # módulo para mostrar os clientes cadastrados
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        root.mainloop() 

    def tela(self): ### CONFIGURAÇÕES DA TELA 
        self.root.title("Cadastro de Clientes")
        self.root.configure(background= '#1e3743')
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.maxsize(width= 900, height= 700)
        self.root.minsize(width=500, height= 400)
        
    def frames_da_tela(self): ### CRIANDO CAIXAS PARA SEPARAR ITENS DA TELA
        self.frame_1 = Frame(self.root, bd = 4, bg= '#dfe3ee',
                             highlightbackground= '#759fe6', highlightthickness=3 )
        self.frame_1.place(relx= 0.02, rely=0.02, relwidth= 0.96, relheight= 0.46)

        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee',
                             highlightbackground='#759fe6', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)
        
    def widgets_frame1(self):  ### CRIAÇÃO DE BOTÕES E POSIÇÕES
        self.bt_limpar = Button(self.frame_1, text= "Limpar", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'), command= self.limpa_cliente)
        self.bt_limpar.place(relx= 0.2, rely=0.1, relwidth=0.1, relheight= 0.15)

        self.bt_buscar = Button(self.frame_1, text="Buscar", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'), command = self.busca_cliente)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

        self.bt_novo = Button(self.frame_1, text="Novo", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'), command= self.add_cliente)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)

        self.bt_alterar = Button(self.frame_1, text="Alterar", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'), command= self.altera_cliente)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)

        self.bt_apagar = Button(self.frame_1, text="Apagar", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'), command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        self.lb_codigo = Label(self.frame_1, text = "Código", bg= '#dfe3ee', fg = '#107db2')
        self.lb_codigo.place(relx= 0.05, rely= 0.05 )

        self.codigo_entry = Entry(self.frame_1 )
        self.codigo_entry.place(relx= 0.05, rely= 0.15, relwidth= 0.08)

        self.lb_nome = Label(self.frame_1, text="Nome", bg= '#dfe3ee', fg = '#107db2')
        self.lb_nome.place(relx=0.05, rely=0.35)

        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.8)

        self.lb_nome = Label(self.frame_1, text="Telefone", bg= '#dfe3ee', fg = '#107db2')
        self.lb_nome.place(relx=0.05, rely=0.6)

        self.fone_entry = Entry(self.frame_1)
        self.fone_entry.place(relx=0.05, rely=0.7, relwidth=0.4)

        self.lb_nome = Label(self.frame_1, text="Cidade", bg= '#dfe3ee', fg = '#107db2')
        self.lb_nome.place(relx=0.5, rely=0.6)

        self.cidade_entry = Entry(self.frame_1)
        self.cidade_entry.place(relx=0.5, rely=0.7, relwidth=0.4)
        
    def lista_frame2(self): 
        self.listaCli = ttk.Treeview(self.frame_2, height=3, column=("col1", "col2", "col3", "col4"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Codigo")
        self.listaCli.heading("#2", text="Nome")
        self.listaCli.heading("#3", text="Telefone")
        self.listaCli.heading("#4", text="Cidade")

        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=200)
        self.listaCli.column("#3", width=125)
        self.listaCli.column("#4", width=125)
        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)
        
        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)
        
    def Menus(self): 
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)    

        def Quit(): self.root.quit()
        
        menubar.add_cascade(label= "Opções", menu= filemenu)
        menubar.add_cascade(label= "Sobre", menu= filemenu2)
        
        filemenu.add_command(label="Sair", command= Quit)
        filemenu2.add_command(label= "Limpa Cliente", command= self.limpa_cliente)

Application()
