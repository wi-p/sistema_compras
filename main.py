#=================================================================================
#Importação das bibliotecas necessárias para o projeto
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooser
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import subprocess as subp
from datetime import date, datetime
from kivy.lang.builder import Builder
from sqlite3 import connect,IntegrityError
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color,Ellipse,Rectangle
from kivy.properties import ListProperty
from kivy.metrics import sp
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image 


class ImageButton(ButtonBehavior, Image):
    pass 


# Botões usados no app
class BtnPersonalizado(ButtonBehavior,Label):
    cor=ListProperty([0.6,0.6,0.7,1])
    cor2=ListProperty([0.4,0.4,0.5,1])

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.size_hint=(1,None)
        self.font_size=25
        self.atualizarBotao()

    def on_size(self,*args):
        self.text_size=(self.width/2,None)
        self.align='center'
        self.atualizarBotao()

    def on_pos(self,*args):
        self.atualizarBotao()

    def on_cor(self,*args):
        self.atualizarBotao()

    def on_press(self,*args):
        self.cor,self.cor2=self.cor2,self.cor

    def on_release(self,*args):
        self.cor,self.cor2=self.cor2,self.cor

    def atualizarBotao(self,*args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.cor)
            Ellipse(size=(self.height,self.height),pos=self.pos)
            Ellipse(size=(self.height,self.height),pos=(self.x+self.width-self.height,self.y))
            Rectangle(size=(self.width-self.height,self.height),pos=(self.x+self.height/2.0,self.y))

class RotuloProduto(BoxLayout):
    """
    classe que representa o rótulo do produto cadastrado
    contendo todas as infomações que vão ser guardadas no
    banco de dados e vão ser mostradas no estoque.
    """

    def __init__(self,nome='',codigo='',descricao='',quantidade='',**kwargs):
        """
        Construtor da classe, ele que vai fazer a requesição das informações para
        serem guardadas
        """
        super().__init__(**kwargs)

        self.ids.nome.text=nome
        self.ids.codigo.text=codigo
        self.ids.descricao.text=descricao
        self.ids.quantidade.text=quantidade

class MiniMenu(BoxLayout):
    pass

class EstandInfo(BoxLayout):
    def __init__(self,rzSocial,rzFantasia,cnpj,**kwargs):
        super().__init__(**kwargs)
        self.ids.rzSocial.text=rzSocial
        self.ids.rzFantasia.text=rzFantasia
        self.ids.cnpj.text=cnpj

class BoxStand(BoxLayout):
    def __init__(self,nomeProduto,quantidadeProduto,precoProduto,totalProduto,**kwargs):
        super().__init__(**kwargs)
        self.ids.nomeProdu.text=nomeProduto
        self.ids.quantiProdu.text=quantidadeProduto
        self.ids.precoProdu.text=precoProduto
        self.ids.totProdu.text=totalProduto


Builder.load_string("""
<Pop>:
    size_hint:(None,None)
    width:'11cm'
    height:'7cm'
    BoxLayout:
        orientation:'vertical'
        Label:
            id:lblNotify
            size_hint_y:None
            text_size:(root.width*0.8,None)
            font_size:20

            text:'oi'
        AnchorLayout:
            anchor_x:'center'
            BtnPersonalizado:
                text:'Voltar'
                on_release:root.dismiss()
                size_hint_x:None
                width:root.width*0.4

<PopInfo>:
    size_hint:(None,None)
    width:'20cm'
    height:'15cm'
    BoxLayout:
        orientation:'vertical'
        spacing:5

        BoxLayout:
            size_hint_y:None
            height:root.height*0.1

            Label:
                font_size:20
                text:'Informações do produto'

        GridLayout:
            cols:3
            BoxLayout:
                orientation:'vertical'
                Label:
                    id:nomeProduto
                    font_size:18
                    text:'Nome produto: '
                Label:
                    id:codigoProduto
                    font_size:18
                    text:'Código produto: '
                Label:
                    id:especificacao
                    font_size:18
                    text:'Especificação: '
                Label:
                    id:qtdInicial
                    font_size:18
                    text:'Quantidade inicial: '

            BoxLayout:
                orientation:'vertical'

                Label:
                    id:valMercadoria
                    font_size:18
                    text:'Valor Pago na mercadoria:R$ '
                Label:
                    id:quantidade
                    font_size:18
                    text:'Quantidade atual: '
                Label:
                    id:totVendido
                    font_size:18
                    text:'Total vendido:R$'
                Label:
                    id:prcCompra
                    text:'Preço de compra:R$'
                    font_size:18

                Label:
                    id: prcVenda
                    text: 'Preço de venda:R$'
                    font_size: 18
                Label:
                    id:vldProduto
                    text:'Validade do produto: '
                    font_size:18

        BtnPersonalizado:
            size_hint:(None,None)
            width:root.width*0.2
            height:root.height*0.1
            text:'Voltar'
            on_release:root.dismiss()
<PopSaida>:
    size_hint:(None,None)
    width:'4cm'
    height: '2cm'
    BoxLayout:
        orientation:'vertical'
        spacing:10
        padding:10
        Image:
            source:'atencao.png'
        BoxLayout:
            spacing:10
            BtnPersonalizado:
                size_hint:(None,None)
                height:"1.5cm"
                width:"4cm"
                font_size:20
                text:'Sim'
                halign: "center"
                on_release:app.get_running_app().stop()
            BtnPersonalizado:
                size_hint:(None,None)
                height:"1.5cm"
                width:"4cm"
                font_size:20
                text:'Não'
                halign: "center"
                on_release:root.dismiss()

<PopAlerta>:
    size_hint:(None,None)
    width:'10cm'
    height:'8cm'
    BoxLayout:
        orientation:'vertical'
        Label:
            id:textoInfo
            font_size:20
            text:''
        AnchorLayout:
            anchor_x:'center'
            BtnPersonalizado:
                size_hint:(None,None)
                height:"1.5cm"
                width:"4cm"
                text:'voltar'
                text_align: "center"
                on_release:root.dismiss()

""")



class Pop(Popup):
    def __init__(self,notify,**kwargs):
        super().__init__(**kwargs)

        self.ids.lblNotify.text=notify
        self.title='Erro!'

    def open(self,*args):
        super().open()

        return True

class PopInfo(Popup):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.title='informações sobre o produto'
        self.title_size=20

    def open(self,*args):
        super().open()

        return True

    def receberInfo(self,infosProduto,infPermanentes,infoGanho,vldProduto):

        self.ids.qtdInicial.text+='{}'.format(bancoDados33.getQtdInicial(infosProduto[0][1]))
        self.ids.valMercadoria.text+='{:.2f}'.format((bancoDados33.getValMercadoria(infosProduto[0][1])))
        self.ids.vldProduto.text+='{}'.format(infPermanentes[0][5])
        self.ids.totVendido.text+='{}'.format(infoGanho)
        self.ids.prcVenda.text+='{}'.format(infPermanentes[0][-1])


        coluna1=[
        self.ids.nomeProduto,
        self.ids.codigoProduto,
        self.ids.especificacao,
        self.ids.quantidade
        ]
        i=0

        prcCompra=bancoDados33.getPrcCompra(infosProduto[0][1])

        self.ids.prcCompra.text+='{:.2f}'.format(prcCompra[0][0])

        for valor in infosProduto[0]:
            coluna1[i].text+=str(valor)
            i+=1

class PopSaida(Popup):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.width = "10cm"
        self.height = "8cm"
        self.title_size=25
        self.title='Deseja realmente sair?'

    def open(self,*args):
        super().open()

class PopAlerta(Popup):
    def __init__(self,mensagem,**kwargs):
        super().__init__(**kwargs)
        self.title_size=25
        self.title='Aviso'
        self.ids.textoInfo.text=mensagem
        self.ids.textoInfo.size_hint_y=None

def mostrarErroProduto():
    pop=Popup()



class BancoDados33:
    conn=connect('produtos.db')
    cursor=conn.cursor()

    def getQtdInicial(self,codigo):
        self.cursor.execute("""
            select qtdInicial from infoPermanentes
            where codProduto=?;
        """,(codigo,))

        qtdInicial=self.cursor.fetchall()

        self.cursor.execute("""
            select * from infoPermanentes;
        """)

        infos=self.cursor.fetchall()

        return qtdInicial[0][0]

    def getValMercadoria(self,codigo):
        self.cursor.execute("""
            select valMercadoria from infoPermanentes
            where codProduto=?;
        """,(codigo,))

        valMercadoria=self.cursor.fetchall()

        return valMercadoria[0][0]

    def getPrcCompra(self,codigo):
        self.cursor.execute("""
            select prcCompra from infoPermanentes
            where codProduto=?;
        """,(codigo,))

        prcCompra=self.cursor.fetchall()

        return prcCompra


class BancoDados22:
    conn=connect('produtos.db')
    cursor=conn.cursor()

    def mostrarMarca(self,cnpj):
        self.cursor.execute("""
            select rzFantasia from empresas
            where cnpj=?;
        """,(cnpj, ))

        marca=self.cursor.fetchall()

        return marca


class BancoDados:
    conn=connect('produtos.db')
    cursor=conn.cursor()

    def __init__(self):
        self.adicionarTabelas()

#========================================== TABELAS ==========================================================
    def adicionarTabelas(self):
        self.cursor.execute("""
            create table if not exists produtos(
                nome varchar(40),
                codigo varchar(30) not null,
                especificacao text,
                quantidade int unsigned,
                prcUnidade float,
                primary key(codigo)
            );
        """)
        self.conn.commit()

        self.cursor.execute("""
            create table if not exists diviClientes(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome varchar(40),
                valor float
            );
        """)
        self.conn.commit()

        self.cursor.execute("""
            create table if not exists infoPermanentes(
                codProduto varchar(30),
                qtdInicial int,
                prcCompra float,
                valMercadoria float,
                ganho float,
                vldProduto date,
                prcVenda float,
                foreign key(codProduto) references produtos(codigo)
            );
        """)
        self.conn.commit()

        self.cursor.execute("""
            create table if not exists senhaUsuario(
                senha varchar(10),
                plvrChave varchar(50),
                primary key(senha)
            );
        """)
        self.conn.commit()

#=============================================================================================================

    def getPrecoVenda(self, codigo):
        self.cursor.execute("""
            select prcVenda from infoPermanentes
            where codProduto = ?;
        """, (codigo, ))

        cod = self.cursor.fetchall()

        return cod[0][0]


    def getCod(self, ):
        cods = list()
        self.cursor.execute('''
            select codigo from produtos;
        ''')

        for cod in self.cursor.fetchall():
            cods.append(cod)

        return cods



#========================================= MÉTODOS GET E SET DAS TABELAS =====================================

    #TABELA PRODUTOS

    def getNome(self,codigo,*args):
        self.cursor.execute("""
            select nome from produtos
            where codigo=?;
        """,(codigo,))

        val=self.cursor.fetchall()

        return val[0][0]

    def setNome(self,codigo,newNome,*args):
        self.cursor.execute("""
            update produtos
            set nome=?
            where codigo=?;
        """,(newNome,codigo,))

        self.conn.commit()

    def getcodigo(self,codigo,*args):
        self.cursor.execute("""
            select codigo from produtos
            where codigo=?;
        """,(codigo,))

        codigo=self.cursor.fetchall()

        return codigo[0][0]

    def setCodigo(self,codigo,newCodigo,*args):
        self.cursor.execute("""
            update produtos
            set codigo=?
            where codigo=?;
        """,(newCodigo,codigo))
        self.conn.commit()

    def getEspecificacao(self,codigo,*args):
        self.cursor.execute("""
            select especificacao from produtos
            where codigo=?;
        """,(codigo))

        especificacao=self.cursor.fetchall()

        return especificacao[0][0]

    def setEspecificacao(self,codigo,newEspecificacao,*args):
        self.cursor.execute("""
            update produtos
            set especificacao=?
            where codigo=?;
        """,(newEspecificacao,codigo,))
        self.conn.commit()

    def getQuantidade(self,codigo,*args):
        self.cursor.execute("""
            select quantidade from produtos
            where codigo=?;
        """,(codigo,))

        quantidade=self.cursor.fetchall()

        return quantidade[0][0]

    def setQuantidade(self,codigo,newQuantidade,*args):
        self.cursor.execute("""
            update produtos
            set quantidade=?
            where codigo=?;
        """,(newQuantidade,codigo,))
        self.conn.commit()

    def getCnpjEmp(self,codigo,*args):
        self.cursor.execute("""
            select cnpjEmp from produtos
            where codigo=?;
        """,(codigo,))

        cnpjEmp=self.cursor.fetchall()

        return cnpjEmp[0][0]

    def setCnpjEmp(self,codigo,newCnpjEmp,*args):
        self.cursor.execute("""
            update produtos
            set cnpjEmp=?
            where codigo=?;
        """,(newCnpjEmp,codigo,))
        self.conn.commit()

    #TABELA INFOPERMANENTES

    def getQtdInicial(self,codigo,*args):
        self.cursor.execute("""
            select qtdInicial from infoPermanentes
            where codProduto=?;
        """,(codigo,))

        qtdInicial=self.cursor.fetchall()

        return qtdInicial[0][0]

    def setQtdInicial(self,codigo,newQtdInicial,*args):
        self.cursor.execute("""
            update infoPermanentes
            set qtdInicial=?
            where codProduto=?;
        """,(newQtdInicial,codigo))
        self.conn.commit()

    def getPrcCompra(self,codigo,*args):
        self.cursor.execute("""
            select prcCompra from infoPermanentes
            where codProduto=?;
        """,(codigo,))

        prcCompra=self.cursor.fetchall()

        return prcCompra[0][0]

    def setPrcCompra(self,codigo,newPrcCompra,*args):
        self.cursor.execute("""
            update infoPermanentes
            set prcCompra=?
            where codProduto=?;
        """,(newPrcCompra,codigo))
        self.conn.commit()

    def getGanho(self,codigo,*args):
        self.cursor.execute("""
            select ganho from infoPermanentes
            where codProduto=?;
        """,(codigo,))

        ganho=self.cursor.fetchall()

        return ganho[0][0]

    def setGanho(self,codigo,newGanho,*args):
        self.cursor.execute("""
            update infoPermanentes
            set ganho=?
            where codProduto=?;
        """,(newGanho,codigo,))
        self.conn.commit()

    def getValMercadoria(self,codigo,*args):
        self.cursor.execute("""
            select valMercadoria from infoPermanentes
            where codProduto=?;
        """,(codigo,))

        valMercadoria=self.cursor.fetchall()

        return valMercadoria[0][0]

    def setValMercadoria(self,codigo,newValor,*args):
        self.cursor.execute("""
            update infoPermanentes
            set valMercadoria=?
            where codProduto=?;
        """,(newValor,codigo,))
        self.conn.commit()

    def setVldMercadoria(self,codigo,newValidade,*args):
        self.cursor.execute("""
            update infoPermanentes
            set vldProduto=?
            where codProduto=?;
        """,(newValidade,codigo,))
        self.conn.commit()

#=============================================================================================================

#================================== MÉTODOS DOS PRODUTOS =====================================================
    def mostrarProdutos(self,*args):
        produtos=[]

        self.cursor.execute("""
            select * from produtos
            order by nome;
        """)

        for produto in self.cursor.fetchall():
            produtos.append(produto)

        return produtos

    def mostrarTudo(self,*args):
        pass

    def cadastrarProduto(self,nome,codigo,especificacao,quantidade,prcUnidade):
        if nome!='' and codigo!='' and especificacao!='' and quantidade!='' and prcUnidade!='' :
            try:
                self.cursor.execute("""
                    insert into produtos
                    (nome,codigo,especificacao,quantidade,prcUnidade)
                    values
                    (?,?,?,?,?);
                """,(nome,codigo,especificacao,quantidade,prcUnidade))
                self.conn.commit()
            except IntegrityError:
                PopAlerta("Erro! O código do produto já\nestá cadastrado no sistema, por favor\ncorrija-o.").open()

                return True
        else:
            PopAlerta('por favor, preencha os campos').open()

    def mostrarInfoProduto(self,codigoP,*args):

        self.cursor.execute("""
            select nome,codigo,especificacao,quantidade from produtos
            where codigo=?;
        """,(codigoP,))

        infoProduto=self.cursor.fetchall()

        return infoProduto

    def atualizarQtdProdutos(self,codigo,quantidade):
        try:
            self.cursor.execute("""
                select quantidade from produtos
                where codigo=?;
            """,(codigo,))

            valorEstoque=self.cursor.fetchall()

            if valorEstoque[0][0]<=0 :
                return PopAlerta('Erro, o estoque do produto\né atualmente 0, por favor reponha').open()


            self.cursor.execute("""
                update produtos
                set quantidade=?
                where codigo=?;
            """,(int(valorEstoque[0][0])-int(quantidade),codigo,))

            self.conn.commit()

            #PopAlerta('O estoque desse produto, atualmente, é '+str(valorEstoque[0][0] - int(quantidade))).open()

        except IndexError:
            return PopAlerta('Erro, este produto não\nestá cadastrado no estoque').open()

    def removerRegistro(self,codigoProduto,*args):
        codigos=[]

        self.cursor.execute("""
            select codigo from produtos;
        """)

        for codigo in self.cursor.fetchall():
            codigos.append(codigo[0])

        if codigoProduto in codigos:
            self.cursor.execute("""
                delete from produtos
                where codigo=?;
            """,(codigoProduto,))

            self.conn.commit()

            PopAlerta("Produto removido com sucesso.").open()
        else:
            return PopAlerta('Erro, produto não está no estoque').open()

    def reporProduto(self,codigo,quantidade,prcCompra,vldProduto):
        valMercadoria=float(prcCompra)*float(quantidade)
        valRestante=float(self.getQuantidade(codigo))*float(self.getPrcCompra(codigo))

        self.setVldMercadoria(codigo,vldProduto)
        self.setValMercadoria(codigo,valMercadoria+valRestante)
        self.setQuantidade(codigo,int(self.getQuantidade(codigo))+quantidade)
        self.setQtdInicial(codigo,self.getQuantidade(codigo))
        self.setPrcCompra(codigo,prcCompra)
        self.setGanho(codigo,0)

    def infosProduto(self, codigoP,*args):
        self.cursor.execute("""
            select nome from produtos
            where codigo=?;
        """,(codigoP,))

        info=self.cursor.fetchall()

        return info

    def adicionarInfosPermanentes(self, codigo, quantidade, preco, valMercadoria, vldProduto, prc_Venda):
        if codigo!='' and quantidade!='' and preco!='':

            validade = "{}/{}/{}".format(vldProduto[2], vldProduto[1], vldProduto[0])

            self.cursor.execute("""
                insert into infoPermanentes
                (codProduto, qtdInicial, prcCompra, valMercadoria, ganho, vldProduto, prcVenda)
                values
                (?, ?, ?, ?, ?, ?, ?);
            """,(codigo,int(quantidade),float(preco),valMercadoria,0,validade, prc_Venda ))

            self.conn.commit()
        else:
            return Pop('Erro, as informações\n precisam ser preenchidas').open()

    def mostrarInfosPermanentes(self,codigo):
        self.cursor.execute("""
            select * from infoPermanentes
            where codProduto=?;
        """,(codigo,))

        infos=self.cursor.fetchall()

        return infos

    def atualizarGanho(self,codigo,valor):
        self.cursor.execute("""
            select ganho from infoPermanentes
            where codProduto=?;
        """,(codigo,))

        valAtual=self.cursor.fetchall()

        valNovo=valAtual[0][0]
        if valNovo==None:
           valNovo=0

        self.cursor.execute("""
            update infoPermanentes
            set ganho=?
            where codProduto=?;
        """,(float(valNovo)+valor,codigo,))
        self.conn.commit()

        self.cursor.execute("""
            select ganho from infoPermanentes
            where codProduto=?;
            """,(codigo,))

        valor=self.cursor.fetchall()

    def mostrarValor(self,codProduto):
        self.cursor.execute("""
            select ganho from infoPermanentes
            where codProduto=?;
        """,(codProduto,))

        ganho=self.cursor.fetchall()

        if ganho[0][0]==None:
            ganho[0][0]=[[0]]

        return ganho

    def totProdutos(self,*args):
        self.cursor.execute("""
            select * from produtos;
        """)

        totProdutos=self.cursor.fetchall()

        return len(totProdutos)

    def mostrarInfosProdutoEsp(self,nmeProduto):
        self.cursor.execute("""
            select * from produtos
            where nome=?;
        """,(nmeProduto,))

        produtos=self.cursor.fetchall()

        return produtos

    def devolverProduto(self,codigo,quantidade,valorFinal):
        cods = self.getCod()


        for codig in cods:
            if codigo in codig[0]:
                qtdAtual=self.getQuantidade(codigo)
                valorGanho=self.getGanho(codigo)

                self.setQuantidade(codigo,qtdAtual+quantidade)
                self.setGanho(codigo,valorGanho-(quantidade*valorFinal))

                return PopAlerta('Produto devolvido com sucesso').open()

        return PopAlerta('Erro! produto não está cadastrado.').open()
#=============================================================================================================

#=================================== Métodos dos clientes que devem um valor =================================

    def adicionarDivCliente(self,nome,valor):
        self.cursor.execute("""
            insert into diviClientes
            (nome,valor)
            values
            (?,?);
        """,(nome,valor,))
        self.conn.commit()

    def mostrarDivClientes(self):
        self.cursor.execute("""
            select * from diviClientes;
        """)

        divs=self.cursor.fetchall()

        return divs

    def removerDivCliente(self,id,*args):
        self.cursor.execute("""
            delete from diviClientes
            where id=?;
        """,(id,))
        self.conn.commit()

    #=============== MÉTODOS DAS SENHAS ============================================

    def cadastrarSenha(self,senha,palavraChave):
        self.cursor.execute("""
            select * from senhaUsuario;
        """)

        senhas=self.cursor.fetchall()

        if len(senhas)==0:
            self.cursor.execute("""
                insert into senhaUsuario
                (senha,plvrChave)
                values
                (?,?);
            """,(senha,palavraChave))
            self.conn.commit()

            PopAlerta('Senha cadastrada com sucesso!!').open()
        else:
            PopAlerta('Alerta, a senha não pode ser cadastrada,pois\nhá um usuário cadastrado.').open()

    def mostrarSenha(self,*args):
        self.cursor.execute("""
            select * from senhaUsuario;
        """)

        senha=self.cursor.fetchall()
        if senha==[]:
            return None
        else:
            return senha[0][0]

    def alterarSenha(self,senha,newSenha):
        self.cursor.execute("""
            update senhaUsuario
            set senha=?
            where senha=?;
        """,(newSenha,senha))
        self.conn.commit()

        PopAlerta('Senha alterada com sucesso!!').open()

    def retornarInfosVal(self):

        produtos=[]
        self.cursor.execute("""
            select codProduto,vldProduto from infoPermanentes
            order by vldProduto;
        """)

        validades=self.cursor.fetchall()

        def returnValue(id):
            self.cursor.execute("""
                select nome,codigo from produtos
                where codigo=?;
            """, (id,))

            val = self.cursor.fetchall()

            return val
        for produto in validades:
            data = produto[1].split('/')
            date = "{}/{}/{}".format(datetime.today().year, datetime.today().month, datetime.today().day)
            diferenca = datetime(year = int(data[0]), month = int(data[1]), day = int(data[2])) - datetime(year = datetime.today().year,
                                                                                                  month = datetime.today().month,
                                                                                                  day = datetime.today().day)
            if diferenca.days < 10:
                var = returnValue(produto[0])

                produtos.append(var[0])


        return produtos,validades

def mostrarM(cnpj):
    conn=connect('produtos.db')
    cursor=conn.cursor()

    cursor.execute("""
        select rzFantasia from empresas
        where cnpj=?;
        """,(cnpj,))

    marca=cursor.fetchall()

    return marca
#===============================================================================



Builder.load_string("""
<Gerenciador>:
    Menu:
        name: 'menu'
    SenhaModificada:
        name:'snhModificada'
    CadastrarProduto:
        name: 'cadPro'
    Estoque:
        name:'estoque'
    Lixeira:
        name:'lixeira'
    ProdutosVenda:
        name:'produtosvenda'
    ProdutoReposicao:
        name:'produtoreposicao'
    ContaCliente:
        name:'contacliente'
    ValidadeProdutos:
        name:'validadeprodutos'
    ProdutoDevolvido:
        name:'produtodevolvido'

<Menu>:
    id:telaMenu

    BoxLayout:
        orientation: 'vertical'
        padding: 100
        spacing: 10
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size

        AnchorLayout:
            anchor_x:'left'
            anchor_y:'bottom'

            BoxLayout:
                size_hint_y:None
                height:root.height*0.6

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None

                    GridLayout:
                        id:boxCols
                        cols:3
                        spacing:10

                        BoxLayout:
                            orientation: 'vertical'
                            spacing: 10

                            BtnPersonalizado:
                                text: 'Cadastrar Produto'
                                halign:'center'
                                on_release: app.root.current = 'cadPro'
                            BtnPersonalizado:
                                text: 'Analisar Estoque'
                                halign:'center'
                                on_release:app.root.current='estoque'
                            BtnPersonalizado:
                                text: 'Remover Produtos'
                                halign:'center'
                                on_release:app.root.current='lixeira'
                            BtnPersonalizado:
                                text: 'Sair'
                                halign:'center'
                                on_release:root.confirmarSaida()
                        BoxLayout:
                            orientation:'vertical'
                            spacing:10

                            BtnPersonalizado:
                                text:'Vendas'
                                halign:'center'
                                on_release:app.root.current='produtosvenda'
                            BtnPersonalizado:
                                text:'Repor Produto'
                                halign:'center'
                                on_release:app.root.current='produtoreposicao'
                            BtnPersonalizado:
                                text:'Validades próximas'
                                halign:'center'
                                on_release:app.root.current='validadeprodutos'
                            BtnPersonalizado:
                                text:'Devolução de produto'
                                halign:'center'
                                on_release:app.root.current='produtodevolvido'
                            BtnPersonalizado:
                                text:'Ver arrecadação'

                        BoxLayout:
                            BoxLayout:
                                size_hint_y: None
                                height: root.height * 0.8

                                canvas.before:
                                    Color:
                                        rgba:1,1,1,1
                                    Rectangle:
                                        pos:self.pos
                                        size:self.size




<CadastrarProduto>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 10
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size


        ActionBar:
            size_hint_y: None
            height: "1cm"
            ActionView:
                ActionPrevious:
                    app_icon_width: 1
                    title: 'Cad. Produtos'
                    on_release: app.root.current = 'menu'
        GridLayout:
            cols:2
            padding:10
            spacing:10
            BoxLayout:
                orientation:'vertical'
                spacing:10
                AnchorLayout:
                    anchor_y:'top'
                    BoxPersonalizado:
                        size_hint_y:None
                        height:'1.5cm'

                        LblPer:
                            text: 'Nome: '
                            color: (0, 0, 0, 1)
                        TextInput:
                            id: nome
                AnchorLayout:
                    anchor_y:'top'
                    BoxPersonalizado:
                        size_hint_y:None
                        height:'1.5cm'

                        LblPer:
                            text: 'Código: '
                            color: (0, 0, 0, 1)
                        TextInput:
                            id: codigo
                AnchorLayout:
                    anchor_y:'top'
                    BoxPersonalizado:
                        size_hint_y:None
                        height:'2cm'

                        LblPer:
                            text:'Preço de custo por unidade:'
                            color: (0, 0, 0, 1)

                        AnchorLayout:
                            anchor_y: "top"
                            TextInput:
                                id:prcUnidade
                                size_hint_y: None
                                height: "1.5cm"


            BoxLayout:
                orientation:'vertical'
                spacing:10
                AnchorLayout:
                    anchor_y:'top'
                    BoxPersonalizado:
                        size_hint_y:None
                        height:'1.5cm'

                        LblPer:
                            text: 'Especificação:'
                            color: (0, 0, 0, 1)

                        TextInput:
                            id: descricao
                AnchorLayout:
                    anchor_y:'top'
                    BoxPersonalizado:
                        size_hint_y:None
                        height:'1.5cm'

                        LblPer:
                            text:'Total de unidades:'
                            color: (0, 0, 0, 1)

                        TextInput:
                            id:qtdProduto

                AnchorLayout:
                    anchor_y: 'top'

                    BoxPersonalizado:
                        size_hint_y: None
                        height: "1.5cm"

                        LblPer:
                            text: "Preço de venda: "
                            color: (0, 0, 0, 1)

                        TextInput:
                            id: prc_venda

        AnchorLayout:
            anchor_y:'center'
            BoxPersonalizado:
                size_hint_y:None
                height:'1.5cm'
                pading: 20
                LblPer:
                    text:'Vld Produto:'
                    color: (0, 0, 0, 1)
                    font_size: 18
                    height: "1.5cm"

                LblPer:
                    text: "Dia: "
                    color: (0, 0, 0, 1)
                    font_size:18
                    height: "1.5cm"

                TextInput:
                    id:vldProduto_Dia
                    size_hint_y:None
                    height:'1.5cm'

                LblPer:
                    text: "Mês: "
                    color: (0, 0, 0, 1)
                    font_size: 18
                    height: "1.5cm"

                TextInput:
                    id: vldProduto_Mes
                    size_hint_y: None
                    height: "1.5cm"

                LblPer:
                    text: "Ano: "
                    color: (0, 0, 0, 1)
                    font_size: 18
                    height: "1.5cm"

                TextInput:
                    id: vldProduto_Ano
                    size_hint_y: None
                    height: "1.5cm"

        AnchorLayout:
            anchor_x:'center'
            anchor_y:'top'
            size_hint_y:None

            BoxLayout:
                padding:20
                BtnPersonalizado:
                    font_size: 40
                    size_hint_x:None
                    width:root.width*0.26
                    text: 'Cadastrar'
                    on_release: root.cadastrarProduto()
<Estoque>:
    BoxLayout:
        orientation:'vertical'
        spacing:10
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size


        ActionBar:
            size_hint_y: None
            height: "1cm"
            ActionView:
                ActionPrevious:
                    app_icon_width: 1
                    title:'Estoque'
                    on_release:app.root.current='menu'

        BoxLayout:
            spacing:10
            size_hint_y:None
            height:root.height*0.1
            Label:
                size_hint_x:None
                width:root.width*0.14
                text:'Código do produto: '
                color: (0, 0, 0, 1)
                font_size:18
            TextInput:
                id:codPesquisa
                size_hint_x:None
                width:root.width*0.1
            BtnPersonalizado:
                size_hint:(None,None)
                width:root.width*0.14
                height:root.height*0.1
                text:'Pesquisar'
                halign:'center'
                font_size:18
                on_release:root.detalharProd()
            Label:
                size_hint_x:None
                width:root.width*0.14
                color: (0, 0, 0, 1)
                text:'Nome do produto:'
                font_size:18
            TextInput:
                id:nmeProduto
                size_hint_x:None
                width:root.width*0.14
            BtnPersonalizado:
                size_hint:(None,None)
                width:root.width*0.14
                height:root.height*0.1
                text:'Pesquisar'
                font_size:18
                on_release:root.mostrarProdutosEspecificos()

            BoxLayout:
                orientation: "vertical"
                Label:
                    halign:'right'
                    text:"Total de produtos:"
                    color: (0, 0, 0, 1)
                    font_size:18
                Label:
                    id:totProdutosCad
                    halign: "right"
                    font_size: 18
                    color: (0, 0, 0, 1)

        BoxLayout:
            size_hint_y:None
            height:root.height*0.10
            canvas.before:
                Color:
                    rgba:0.1,0.4,0.9,0.5
                Rectangle:
                    pos:self.pos
                    size:self.size

            Label:
                text:'Nome'

            Label:
                text:'Código'

            Label:
                text:'Descrição'

            Label:
                text:'Quantidade'

            Label:
                text:'Opções'


        ScrollView:
            BoxLayout:
                id:box
                spacing:10
                orientation:'vertical'
                size_hint_y:None
                height:self.minimum_height

<RotuloProduto>:
    size_hint_y:None
    height:200
    spacing:10
    canvas.before:
        Color:
            rgba:0.1,0.4,0.6,0.5
        Rectangle:
            pos:self.pos
            size:self.size

    AnchorLayout:
        anchor_x:'center'
        anchor_y:'center'
        Label:
            font_size:25
            id: nome
            size_hint:(1,None)
            text_size:(self.width-sp(10),None)
            halign:'center'
    AnchorLayout:
        anchor_x:'center'
        anchor_y:'center'
        Label:
            font_size:25
            id:codigo
            size_hint:(1,None)
            text_size:(self.width-sp(10),None)
            halign:'center'
    AnchorLayout:
        anchor_x:'center'
        anchor_y:'center'
        Label:
            font_size:25
            id:descricao
            size_hint:(1,None)
            text_size:(self.width-sp(10),None)
            halign:'center'
    AnchorLayout:
        anchor_x:'center'
        anchor_y:'center'
        Label:
            id:quantidade
            font_size:25
            size_hint:(1,None)
            text_size:(self.width,None)
            halign:'center'
    AnchorLayout:
        anchor_y:'center'
        BtnPersonalizado:
            id:self.ids.cnpjEmpr.text
            text:'Detalhar'
            font_size:15
            halign:'center'
            size_hint_x:None
            width:root.width*0.1
            on_release:app.root.get_screen('estoque').detalharInfo(root.ids)

<Lixeira>:
    BoxLayout:
        orientation:'vertical'
        spacing:5
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size

        ActionBar:
            size_hint_y:None
            height:"1cm"
            ActionView:
                ActionPrevious:
                    app_icon_width: 1
                    title:'Lixeira'
                    on_release:app.root.current='menu'

        BoxLayout:
            padding:180
            AnchorLayout:
                anchor_x:'center'
                anchor_y:'center'

                BoxLayout:
                    id:box2
                    orientation:'vertical'
                    padding:10
                    spacing:10

                    Label:
                        text:'Digite o código do produto'
                        color: (0, 0, 0, 1)
                        size_hint_y:None
                        height:box2.height*0.3
                        font_size:20
                    TextInput:
                        id:codgo2
                        size_hint_y:None
                        height:box2.height*0.3

                    AnchorLayout:
                        anchor_x:'center'
                        anchor_y:'center'
                        size_hint_y:None
                        height:box2.height*0.3
                        BtnPersonalizado:
                            text:'Apagar'
                            on_release:root.removerProduto()
                            size_hint:(None,None)
                            height:root.height*0.1
                            width:root.width*0.25
                            halign:'center'


<EstandInfo>:
    size_hint_y:None
    canvas.before:
        Color:
            rgba: 0.1,0.4,0.6,0.5
        Rectangle:
            pos:self.pos
            size:self.size
    height:200
    Label:
        id:rzSocial
        font_size:20
    Label:
        id:rzFantasia
        font_size:20
    Label:
        id:cnpj
        font_size:20


<ProdutosVenda>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size


    BoxLayout:
        orientation:'vertical'

        ActionBar:
            size_hint_y: None
            height: "1cm"
            ActionView:
                ActionPrevious:
                    app_icon_width: 1
                    title:'Vendas'
                    on_release:app.root.current='menu'

                ActionButton:
                    text:'Conta clientes'
                    on_release:app.root.current='contacliente'
        GridLayout:
            cols:2
            padding:20
            BoxLayout:
                orientation:'vertical'
                spacing:10

                AnchorLayout:
                    anchor_y:'center'
                    GridLayout:
                        cols:1
                        spacing:5
                        padding:10


                        BoxLayout:
                            orientation:'vertical'
                            size_hint_x:None
                            width:root.width*0.5
                            spacing:20

                            BoxPersonalizado:
                                size_hint_y: None
                                height: "1.5cm"
                                LblPer:
                                    text:'Código:'
                                    color: (0, 0, 0, 1)
                                TextInput:
                                    size_hint_x:None
                                    width:root.width*0.2
                                    id:codigo
                            BoxPersonalizado:
                                size_hint_y: None
                                height: "1.5cm"
                                LblPer:
                                    text:'Quantidade:'
                                    color: (0, 0, 0, 1)
                                TextInput:
                                    size_hint_x:None
                                    width:root.width*0.2
                                    id:qtdProduto



                AnchorLayout:
                    anchor_x:'left'
                    anchor_y:'center'
                    GridLayout:
                        cols:2
                        spacing:10
                        size_hint_y:None
                        height:root.height*0.15

                        BoxLayout:
                            orientation:'vertical'
                            spacing:20
                            BtnPersonalizado:
                                size_hint: (None, None)
                                width:root.width*0.2
                                height: root.height * 0.1
                                text:'Adicionar ao carrinho'
                                haling:'center'
                                on_release:root.adicionarProdutoCar()

                            BtnPersonalizado:
                                size_hint: (None, None)
                                width:root.width*0.2
                                height: root.height * 0.1
                                text:'Finalizar Compra'
                                halign:'center'
                                on_release:root.finalizarCompra()

            AnchorLayout:
                anchor_y:'top'
                BoxLayout:
                    orientation:'vertical'
                    id:stinfo
                    size_hint:(None,None)
                    height:root.height*0.8
                    padding:20
                    width:root.width*0.4
                    canvas.before:
                        Color:
                            rgba:1,1,1,1
                        Rectangle:
                            pos:self.pos
                            size:self.size

                    AnchorLayout:
                        anchor_x: "center"
                        anchor_y:"top"

                        BoxLayout:
                            size_hint: (None, None)
                            width: "6cm"
                            heigth:"1.5cm"
                            halign: "right"
                            spacing: 20


                            Label:
                                id:lblData
                                halign: "right"
                                font_size: 22
                                size_hint_x:None
                                width:"1cm"
                                color:0,0,0,1
                                text:'Data:   '

                            Label:
                                text:'  Carrinho:'
                                font_size: 22
                                halign:'left'
                                color:0,0,0,1


                    ScrollView:
                        BoxLayout:
                            id:standProdutos
                            spacing:10
                            orientation:'vertical'
                            size_hint_y:None
                            height:self.minimum_height
                    BoxLayout:
                        size_hint_y:None
                        height:root.height*0.1

                        Label:
                            text:'Total: R$'
                            color:0,0,0,1

                        Label:
                            id:lblValCompra
                            text:'0'
                            color:0,0,0,1
                            size_hint_x:None
                            width:root.width*0.1

<ProdutoReposicao>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size


    BoxLayout:
        orientation:'vertical'
        spacing:20

        ActionBar:
            size_hint_y: None
            height: "1cm"
            ActionView:
                ActionPrevious:
                    app_icon_width: 1
                    title:'Repor produto'
                    on_release:app.root.current='menu'

        GridLayout:
            cols:2
            padding:5

            BoxLayout:
                orientation:'vertical'
                spacing:5

                BoxPersonalizado:
                    size_hint_y: None
                    height: "1.5cm"
                    Label:
                        text:'Código:'
                        color: (0, 0, 0, 1)
                        font_size:27
                    TextInput:
                        id:codigoRepor
                        size_hint_x:None
                        width:root.width*0.3

                BoxPersonalizado:
                    size_hint_y:None
                    height: "1.5cm"
                    Label:
                        text:'Quantidade:'
                        color: (0, 0, 0, 1)
                        font_size:27
                    TextInput:
                        id:quantidadeRepor
                        size_hint_x:None
                        width:root.width*0.3
                BoxPersonalizado:
                    size_hint_y: None
                    height: "1.5cm"
                    Label:
                        text:'Preço por unidade:'
                        color: (0, 0, 0, 1)
                        font_size:27
                    TextInput:
                        id:prcReposicao
                        size_hint_x:None
                        width:root.width*0.3

                BoxPersonalizado:
                    size_hint_y: None
                    height: "1.5cm"
                    Label:
                        text:'Validade: '
                        color: (0, 0, 0, 1)
                        font_size:27
                    Label:
                        text: 'Dia: '
                        color: (0, 0, 0, 1)
                        font_size: 27

                    TextInput:
                        id:dataProduto_dia

                    Label:
                        text: 'Mês: '
                        color: (0, 0, 0, 1)
                        font_size:27

                    TextInput:
                        id: dataProduto_mes

                    Label:
                        text: 'Ano: '
                        color: (0, 0, 0, 1)
                        font_size:27

                    TextInput:
                        id: dataProduto_ano

            BoxLayout:
                orientation:'vertical'
                spacing:10
                size_hint_x: None
                width: root.width * 0.4

        AnchorLayout:
            anchor_x:'center'
            BtnPersonalizado:
                size_hint:(None,None)
                width:root.width*0.2
                height:root.height*0.15
                text:'Repor'
                halign:'center'
                on_release:root.enviarInformacoes()

<ContaCliente>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size


    BoxLayout:
        orientation:'vertical'
        spacing:40

        ActionBar:
            size_hint_y: None
            height: "1cm"
            ActionView:
                ActionPrevious:
                    app_icon_width: 1
                    on_release:app.root.current='produtosvenda'

        GridLayout:
            cols:2
            padding:20
            spacing:20

            GridLayout:
                cols:1

                AnchorLayout:
                    anchor_y:'top'
                    BoxLayout:
                        size_hint_y:None
                        height:root.height*0.3
                        orientation:'vertical'
                        spacing:40

                        BoxPersonalizado:
                            size_hint_y: None
                            height: "1.5cm"

                            Label:
                                text:'Nome:'
                                color: (0, 0, 0, 1)
                                font_size:25
                            TextInput:
                                id:nomCliente
                        BoxPersonalizado:
                            size_hint_y: None
                            height: "1.5cm"

                            Label:
                                text:'Valor:'
                                color: (0, 0, 0, 1)
                                font_size:25
                            TextInput:
                                id:valCliente

                        AnchorLayout:
                            anchor_y:'top'
                            BoxLayout:
                                orientation:'vertical'
                                size_hint_y:None
                                height:root.height*0.5
                                spacing:40

                                AnchorLayout:
                                    anchor_y:'center'
                                    BtnPersonalizado:
                                        size_hint:(None,None)
                                        height:root.height*0.1
                                        width:root.width*0.2
                                        text:'Adicionar'
                                        halign:'center'
                                        on_release:root.adicionarClientes()

            BoxLayout:
                orientation:'vertical'
                spacing:10
                BoxLayout:
                    size_hint_y:None
                    height:'1cm'
                    canvas.before:
                        Color:
                            rgba:0,0.5,0.9,0.1
                        Rectangle:
                            pos:self.pos
                            size:self.size

                    Label:
                        text:'Opções'
                        color: (0, 0, 0, 1)
                    Label:
                        text:'Número'
                        color: (0, 0, 0, 1)
                    Label:
                        text:'Nome'
                        color: (0, 0, 0, 1)
                    Label:
                        text:'Valor R$'
                        color: (0, 0, 0, 1)

                ScrollView:

                    BoxLayout:
                        orientation:'vertical'
                        size_hint_y:None
                        height:self.minimum_height
                        id:boxClientes
                        spacing:10

<ValidadeProdutos>:
    BoxLayout:
        orientation:'vertical'
        spacing:10
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size


        ActionBar:
            size_hint_y: None
            height: "1cm"

            ActionView:
                ActionPrevious:
                    app_icon_width: 1
                    title:'Validades'
                    on_release:app.root.current='menu'

        BoxLayout:
            size_hint_y:None
            height:root.height*0.1
            canvas.before:
                Color:
                    rgba:0.1,0.4,.9,0.5
                Rectangle:
                    pos:self.pos
                    size:self.size

            Label:
                font_size:18
                text:'Nome'


            Label:
                font_size:18
                text:'Código'

            Label:
                font_size:18
                text:'Validade'
        BoxLayout:

            ScrollView:
                BoxLayout:
                    orientation:'vertical'
                    size_hint_y:None
                    height:self.minimum_height
                    spacing:10
                    id:boxValidade

<ProdutoDevolvido>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos:self.pos
            size:self.size


    BoxLayout:
        orientation:'vertical'
        ActionBar:
            size_hint_y: None
            height: "1cm"

            ActionView:
                ActionPrevious:
                    app_icon_width: 1
                    title:'Devolução de produto'
                    on_release:app.root.current='menu'

        AnchorLayout:
            anchor_y:'top'
            anchor_x:'left'
            BoxLayout:
                orientation:'vertical'
                size_hint:(None,None)
                width:root.width*0.5
                height:root.height*0.9
                padding:10
                spacing:20



                BoxPersonalizado:
                    size_hint_y:None
                    height:'2cm'

                    LblPer:
                        text:'Código:'
                        color: (0, 0, 0, 1)

                    AnchorLayout:
                        anchor_y: "top"
                        TextInput:
                            id:codigoDevol
                            size_hint_y: None
                            height: "1.5cm"

                BoxPersonalizado:
                    size_hint_y:None
                    height:'2cm'

                    LblPer:
                        text:'Quantidade devolvida:'
                        color: (0, 0, 0, 1)

                    AnchorLayout:
                        anchor_y: "top"
                        TextInput:
                            id:quantidadeDevol
                            size_hint_y: None
                            height: "1.5cm"

                BoxPersonalizado:
                    size_hint_y:None
                    height:'2cm'

                    LblPer:
                        text:'Valor final da únidade:'
                        color: (0, 0, 0, 1)

                    AnchorLayout:
                        anchor_y: "top"
                        TextInput:
                            id:valorProduto
                            size_hint_y: None
                            height: "1.5cm"

                AnchorLayout:
                    anchor_x:'center'
                    BtnPersonalizado:
                        text:'Repor'
                        halign:'center'
                        size_hint_x:None
                        width:root.width*0.2
                        on_release:root.devolverProduto()

<BoxP>:
    size_hint_y:None
    height:200
    spacing:10
    padding:30
    canvas.before:
        Color:
            rgba:0,0.5,0.9,0.1
        Rectangle:
            pos:self.pos
            size:self.size
    AnchorLayout:
        anchor_y:'center'
        BtnPersonalizado:
            text:'Apagar'
            font_size:18
            halign:'center'
            on_release:app.root.get_screen('contacliente').removerCliente(root)


#widgets customizados
<BoxPersonalizado@BoxLayout>:
    canvas.before:
        Color:
            rgba:0,0.5,0.9,0.1
        Rectangle:
            pos:self.pos
            size:self.size
    size_hint_y:None
    height:'1.6cm'

<LblPer@Label>:
    size_hint_y:None
    text_size:(self.width-self.height*1,self.height-self.height*0.3)
    font_size:27


<TextPers@TextInput>:
    size_hint_y:None
    height:root.height*0.15

<LblQueb@Label>:#Label que se adapta ao conteúdo.
    size_hint_y:None
    text_size:(self.width,None)

<BoxStand>:
    size_hint_y:None
    height:100

    Label:
        id:nomeProdu
        text:''
        color:0,0,0,1
    Label:
        id:quantiProdu
        text:''
        color:0,0,0,1
    Label:
        id:precoProdu
        text:''
        color:0,0,0,1
    Label:
        id:totProdu
        text:''
        color:0,0,0,1

<Box>:
    canvas.before:
        Color:
            rgba:0.1,0.4,0.6,0.5
        Rectangle:
            pos:self.pos
            size:self.size


    """)


#=============================================================================

#=================================================================================
#Programa principal

"""
Objeto que faz a representação geral do banco de dados. O mesmo possui o escopo
global, podendo ser utilizado em qualquer parte do programa, inclusive dentro de
classes e funções
"""
global bancoDados
bancoDados=BancoDados()

class SenhaModificada(Screen):
    def modificarSenha(self):
        if self.ids.senha.text!='' and self.ids.newSenha.text!='' and self.ids.cnfm.text!='':
            if self.ids.senha.text==bancoDados.mostrarSenha():
                if self.ids.newSenha.text==self.ids.cnfm.text:

                    bancoDados.alterarSenha(self.ids.senha.text,self.ids.newSenha.text)

                    self.ids.senha.text=''
                    self.ids.newSenha.text=''
                    self.ids.cnfm.text=''
                else:
                    PopAlerta('Erro, as senhas não batem').open()

                    self.ids.senha.text=''
                    self.ids.newSenha.text=''
            else:
                PopAlerta('Erro, senha incorreta').open()



        else:
            PopAlerta('Erro, preencha os campos').open()

class Gerenciador(ScreenManager):
    pass

class Menu(Screen):
    def on_pre_enter(self):#função que ativa a função de confirmação(popup)
        #Window.bind(on_request_close=self.confirmarSaida)
        bancoDados.adicionarTabelas()

    def confirmarSaida(self, *args,**kwargs):
        popSaida=PopSaida()

        popSaida.open()

        return True

    def buscarAjudaOnline(self):
        subp.Popen(['xdg-open','http://127.0.0.1/aula/tipos.php?a=5&b=2'])

class CadastrarProduto(Screen):
    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltarMenu)
        Window.bind(on_keyboard = self.help_keyboard)
        self.ids.nome.focus = True

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltarMenu)

    def voltarMenu(self, window, key,*args):
        if key==27:
                App.get_running_app().root.current='menu'

                return TrueP

    def help_keyboard(self, window, key, *args):
        entrances = [
            self.ids.nome,
            self.ids.codigo,
            self.ids.prcUnidade,
            self.ids.descricao,
            self.ids.qtdProduto,
            self.ids.prc_venda,
            self.ids.vldProduto_Dia,
            self.ids.vldProduto_Mes,
            self.ids.vldProduto_Ano
        ]

        try:
            if key == 274:
                for entrance in entrances:
                    if entrance.focus == True:
                        entrance.focus = False
                        entrances[entrances.index(entrance) + 1].focus = True

                        break
            elif key == 273:
                for entrance in entrances:
                    if entrance.focus == True:
                        entrance.focus = False
                        entrances[entrances.index(entrance) - 1].focus = True

                        break

            elif key == 271 or key == 13:
                self.cadastrarProduto()

                self.ids.nome.focus = True
        except IndexError:
            entrances[0].focus = True

    def cadastrarProduto(self, *args):
        #Método para cadastrar produto Este método
        #pega as informações e guarda no banco de dados
        infosproduto=[self.ids.nome,
                      self.ids.codigo,
                      self.ids.descricao,
                      self.ids.qtdProduto,
                      self.ids.prcUnidade,
                      self.ids.vldProduto_Dia,
                      self.ids.vldProduto_Mes,
                      self.ids.vldProduto_Ano,
                      self.ids.prc_venda]

        mo = infosproduto[5].text


        for info in infosproduto:
            if info.text=='':
                return PopAlerta('Erro, por favor preencha todos os\ncampos').open()

        if mo[0] == '0':
            valor = mo.split('0')
            valor.remove('')
            infosproduto[5].text = valor[0]

        try:
            infosproduto[3]=int(infosproduto[3].text)

            if ',' in infosproduto[4].text:
                valor=list(infosproduto[4].text)
                posVirgula=valor.index(',')

                valor.remove(',')
                valor.insert(posVirgula,'.')

                newValor=''

                for item in valor:
                    newValor+=item

                infosproduto[4].text=newValor

            infosproduto[4]=float(infosproduto[4].text)

        except ValueError:
            return PopAlerta('Erro, os campos PREÇO DE CUSTO e\nQUANTIDADE aceitam apenas números').open()

        bancoDados.cadastrarProduto(infosproduto[0].text.capitalize(),infosproduto[1].text,infosproduto[2].text.capitalize(),
        infosproduto[3],infosproduto[4])#Adiciona valores no bd

        bancoDados.setValMercadoria(self.ids.codigo.text,int(self.ids.qtdProduto.text)*float(self.ids.prcUnidade.text))

        bancoDados.adicionarInfosPermanentes(
            infosproduto[1].text,
            int(infosproduto[3]),
            infosproduto[4],
            int(self.ids.qtdProduto.text)*float(self.ids.prcUnidade.text),
            (infosproduto[5].text,
            infosproduto[6].text,
            infosproduto[7].text,),
            infosproduto[8].text
        )

        infosproduto[3]=self.ids.qtdProduto
        infosproduto[4]=self.ids.prcUnidade
        for info in infosproduto:
            info.text=''

class Estoque(Screen):
    def on_enter(self,*args):
        self.ids.totProdutosCad.text+=str(bancoDados.totProdutos())

        for valor in bancoDados.mostrarProdutos():
            """
            Estrutura utlizada para colocar cada produto na tela estoque
            cada produto que está no meu banco de dados é uma lista e cada atributo dele
            tem uma posição no qual eu acesso com os indices da lista.
            """
            self.ids.box.add_widget(RotuloProduto(valor[0],valor[1],valor[2],
                str(valor[3])))

    def on_pre_leave(self, *args):
        """
        Esta função vai remover os meu produtos quando estiver saindo da tela
        isso evita a redundância de dados que pode ser causada pelo acionamento da função
        que vai ficar adicionando os produtos
        """
        self.ids.totProdutosCad.text=''
        for valor in bancoDados.mostrarProdutos():
            #vai ler todos os itens e assim movimentar a estutura que aciona uma função
            self.removerWidgets()#Função para remover os produtos(widgets) da minha tela

    def removerWidgets(self, *args):
        """
        Esta função vai remover cada produto(widget) da minha tela
        no BoxLayout os widgets filhos quando são adiconados eles
        são itens de uma lista e cada um tem um indice que posso remover
        se tirar o widget que tem o índice 0 o widget que tem indice 1 passa a ter 0
        assim da pra remover todos os widgets filhos
        """
        try:
            self.ids.box.remove_widget(self.ids.box.children[0])#o children representa o widget filho e 0 [0] a sua posição
        except IndexError:
            pass

    def detalharInfo(self,id,*args):
        #aciona um popup com as informações sobre um produto
        #infoProduto,infoEmpresa,endeEmpresa=
        #o parâmetro id é responsável por fazer a conexão entre o produto e as informações da
        #empresa e também é parte principal por mostrar as informações.
        ids=list(id.values())

        infProduto=bancoDados.mostrarInfoProduto(id['codigo'].text)
        infPermanente=bancoDados.mostrarInfosPermanentes(str(ids[1].text))

        ganho=bancoDados.mostrarValor(str(ids[1].text))
        pop=PopInfo()

        pop.receberInfo(infProduto,infPermanente,str(ganho[0][0]),str(infPermanente[0][-1]))
        pop.open()

        return True

    def detalharProd(self,*args):
        try:
            codigo=self.ids.codPesquisa.text
            infoProduto=bancoDados.mostrarInfoProduto(codigo)
            infoPermanente=bancoDados.mostrarInfosPermanentes(codigo)
            ganho=bancoDados.mostrarValor(codigo)
            pop=PopInfo()

            pop.receberInfo(infoProduto,infoPermanente,str(ganho[0][0]),infoPermanente[0][-1])
            pop.open()
        except IndexError:
            PopAlerta('Erro, o produto não está no estoque').open()
        finally:
            self.ids.codPesquisa.text = ''


        return True

    def mostrarProdutosEspecificos(self):
        produtos=bancoDados.mostrarInfosProdutoEsp(self.ids.nmeProduto.text.capitalize())

        if len(produtos)>0:
            for produto in bancoDados.mostrarProdutos():
                self.removerWidgets()

            for produto in produtos:
                self.ids.box.add_widget(RotuloProduto(produto[0],produto[1],produto[2],str(produto[3])))
        else:
            return PopAlerta('Erro, o produto não está no estoque').open()

        self.ids.nmeProduto.text = ''

class Lixeira(Screen):

    def on_pre_enter(self,*args):
        Window.bind(on_keyboard=self.voltarMenu)

    def on_pre_leave(self,*args):
        Window.unbind(on_keyboard=self.voltarMenu)

    def voltarMenu(self,Window,key,*args):
        if key==27:
            App.get_running_app().root.current='menu'

            return True

    def removerProduto(self):
        codigo=self.ids.codgo2.text

        bancoDados.removerRegistro(codigo)

        self.ids.codgo2.text=''



class ProdutosVenda(Screen):
    def on_pre_enter(self,*args):
        Window.bind(on_keyboard = self.help_keyboard)
        data="{}/{}/{}".format(date.today().day,date.today().month,date.today().year)
        self.ids.lblData.text+=data
        self.ids.codigo.focus = True

    def help_keyboard(self, window, key, *args):
        entrances = [self.ids.codigo,
                     self.ids.qtdProduto]

        if key == 273:
            if entrances[0].focus == True:
                entrances[0].focus = False
                entrances[-1].focus = True

            elif entrances[1].focus == True:
                entrances[1].focus = False
                entrances[0].focus = True


        elif key == 274:
            if entrances[0].focus == True:
                entrances[0].focus = False
                entrances[1].focus = True

            elif entrances[1].focus == True:
                entrances[1].focus = False

        elif key == 271 or key == 13:
            self.adicionarProdutoCar()

            self.ids.codigo.focus = True

    def on_pre_leave(self,*args):
        self.ids.lblData.text='Data'

    def atualizarEstoque(self,*args):
        quantidade=self.ids.qtdProduto.text
        codigo=self.ids.codigo.text

        bancoDados.atualizarQtdProdutos(codigo,quantidade)

    def adicionarProdutoCar(self,*args):
        codigo=self.ids.codigo.text

        try:
            infos=[self.ids.codigo.text,self.ids.qtdProduto.text, float(bancoDados.getPrecoVenda(self.ids.codigo.text))]

            for info in infos:
                if info=='':
                    return PopAlerta('Erro, por favor preencha todos os\ncampos').open()



            quantidade=bancoDados.getQuantidade(infos[0])

            if (quantidade-int(infos[1])<0):
                return PopAlerta('Erro, o seu estoque é: {}\ne a quantidade requerida é: {}'.format(quantidade,infos[1])).open()

            info=bancoDados.infosProduto(codigo)
            lblNome=str(info[0][0])
            lblQuantidade=self.ids.qtdProduto.text+'x'
            lblPreco=infos[2]
            lblTotProduto='{:.2f}'.format(infos[2]*float(self.ids.qtdProduto.text))
            valTotCompra=float(self.ids.lblValCompra.text)
            valTotCompra+=infos[2]*float(self.ids.qtdProduto.text)

            self.ids.lblValCompra.text=str(valTotCompra)

            bancoDados.atualizarGanho(codigo,float(lblPreco)*float(self.ids.qtdProduto.text))
            self.ids.standProdutos.add_widget(BoxStand(lblNome,lblQuantidade,str(lblPreco),lblTotProduto))

            self.atualizarEstoque()
        except ValueError:
            return PopAlerta('Erro, o campo QUANTIDADE \naceita apenas números').open()
        except IndexError:
            PopAlerta('Erro, produto não está cadastrado no\nestoque').open()
        finally:
            self.ids.qtdProduto.text=''
            self.ids.codigo.text=''
            self.ids.codigo.focus = True

    def finalizarCompra(self,*args):
        produtosVendidos=len(self.ids.standProdutos.children)
        totVenda=self.ids.lblValCompra.text
        self.ids.lblValCompra.text=''

        for produto in range(produtosVendidos):
            self.ids.standProdutos.remove_widget(self.ids.standProdutos.children[0])

        PopAlerta('O valor Total da compra foi: R${}'.format(totVenda)).open()


class ProdutoReposicao(Screen):
    def enviarInformacoes(self,*args):
        dadProduto=[self.ids.codigoRepor,
                    self.ids.quantidadeRepor,
                    self.ids.prcReposicao,
                    self.ids.dataProduto_dia.text,
                    self.ids.dataProduto_mes.text,
                    self.ids.dataProduto_ano.text]

        for dado in dadProduto:
            if dado == '':
                return PopAlerta('Erro, por favor preencha todos os\ncampos.').open()

        try:
            valor=dadProduto[1].text
            dadProduto[1]=int(valor)
            dadProduto[1]=self.ids.quantidadeRepor

            if ',' in dadProduto[2].text:
                valor=list(dadProduto[2].text)
                posVirgula=valor.index(',')

                valor.remove(',')
                valor.insert(posVirgula,'.')

                newValor=''

                for item in valor:
                    newValor+=item

                dadProduto[2].text=newValor

            validade = "{}/{}/{}".format(dadProduto[5], dadProduto[4], dadProduto[3])

            bancoDados.reporProduto(dadProduto[0].text,
                                    int(dadProduto[1].text),
                                    float(dadProduto[2].text),
                                    validade)
        except ValueError:
            return PopAlerta('Erro, os campos PREÇO DE CUSTO e\nQUANTIDADE aceitam apenas números').open()
        except IndexError:
            return PopAlerta('Erro, produto nao está cadastrado no\nestoque.').open()

        finally:
            self.ids.codigoRepor.text = ''
            self.ids.quantidadeRepor.text = ''
            self.ids.prcReposicao.text = ''
            self.ids.dataProduto_dia.text = ''
            self.ids.dataProduto_mes.text = ''
            self.ids.dataProduto_ano.text = ''


class ContaCliente(Screen):
    cont=0

    def on_pre_enter(self,*args):
        divs=bancoDados.mostrarDivClientes()

        for div in divs:
            box=Boxp()
            box.add_widget(Label(text=str(div[0]),font_size=20, color = (0, 0, 0, 1)))
            box.add_widget(Label(text=str(div[1]),font_size=20, color = (0, 0, 0, 1)))
            box.add_widget(Label(text=str(div[2]),font_size=20, color = (0, 0, 0, 1)))

            self.ids.boxClientes.add_widget(box)

    def on_pre_leave(self,*args):
        divs=bancoDados.mostrarDivClientes()
        for div in divs:
            self.removerWidget()

    def adicionarClientes(self,*args):
        nomeCliente=self.ids.nomCliente.text.capitalize()
        valorCliente=self.ids.valCliente.text

        if valorCliente=='':
            valorCliente='0'

        if ',' in valorCliente:
            valor=list(valorCliente)
            posVirgula=valor.index(',')

            valor.remove(',')
            valor.insert(posVirgula,'.')

            newValor=''

            for item in valor:
                newValor+=item

            valorCliente=newValor

        if nomeCliente!='' and float(valorCliente)>0:
            for value in bancoDados.mostrarDivClientes():
                self.removerWidget()

            bancoDados.adicionarDivCliente(nomeCliente,float(valorCliente))
        else:
            return PopAlerta('Erro, campos inválidos\n por favor corrija-os').open()

        divs=bancoDados.mostrarDivClientes()

        for div in divs:
            box=Boxp()

            box.add_widget(Label(text=str(div[0]),font_size=20))
            box.add_widget(Label(text=str(div[1]),font_size=20))
            box.add_widget(Label(text=str(div[2]),font_size=20))

            self.ids.boxClientes.add_widget(box)


        self.ids.nomCliente.text=''
        self.ids.valCliente.text=''

    def removerCliente(self,cliente):
        bancoDados.removerDivCliente(cliente.children[2].text)
        self.ids.boxClientes.remove_widget(cliente)

    def removerWidget(self):
        self.ids.boxClientes.remove_widget(self.ids.boxClientes.children[0])

    def apagarCliente(self,id,*args):
        bancoDados.removerDivCliente(int(id))

        try:
            self.ids.boxClientes.remove_widget(self.ids.boxClientes.children[id])
        except IndexError:
            pass

class Box(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

class ValidadeProdutos(Screen):
    def on_enter(self,*args):
        produtos,validades=bancoDados.retornarInfosVal()
        c=0

        for produto in produtos:
            box=Box(size_hint_y=None,height=self.height*0.15)

            box.add_widget(Label(text=produtos[c][0],font_size=18))
            box.add_widget(Label(text=produtos[c][1],font_size=18))
            box.add_widget(Label(text=validades[c][1],font_size=18))
            self.ids.boxValidade.add_widget(box)

            c+=1

    def on_pre_leave(self,*args):
        produtos, validades = bancoDados.retornarInfosVal()

        for produto in produtos:
            self.removeWidget()

    def removeWidget(self):
        self.ids.boxValidade.remove_widget(self.ids.boxValidade.children[0])

class Boxp(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

class ProdutoDevolvido(Screen):
    def devolverProduto(self):
        infos=[self.ids.codigoDevol,self.ids.quantidadeDevol,self.ids.valorProduto]

        for info in infos:
            if info.text=='':
                return PopAlerta('Erro, preencha todos os campos').open()

        try:
            valor=int(infos[1].text)

            if ',' in infos[2].text:
                valor=list(infos[2].text)
                posVirgula=valor.index(',')

                valor.remove(',')
                valor.insert(posVirgula,'.')

                newValor=''

                for item in valor:
                    newValor+=item

                infos[2].text=newValor

            valor=float(infos[2].text)
        except ValueError:
            pop = PopAlerta('Erro, os campos QUANTIDADE e\nVALOR FINAL aceitam, respectivamente, apenas\nnúmeros inteiros e decimais')
            pop.size_hint_x = 0.5

            return pop.open()

        bancoDados.devolverProduto(infos[0].text,int(infos[1].text),float(infos[2].text))

        for info in infos:
            info.text=''

class app(App):
    icon = 'logo.png'

    def build(self):
        return Gerenciador()#Retorna o gerenciador de telas, que por sua vez lança o menu


global bancoDados22

bancoDados22=BancoDados22()

global bancoDados33
bancoDados33=BancoDados33()


if __name__ == '__main__':#Condição de acionamento
    app().run()#gatilho que inicializa o app
