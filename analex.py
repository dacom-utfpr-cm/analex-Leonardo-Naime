from automata.fa.Moore import Moore
import sys, os
import string
from collections import defaultdict
import xml.etree.ElementTree as ET
from xml.dom import minidom
from myerror import MyError

error_handler = MyError('LexerErrors')

global check_cm
global check_key

# ALFABETO

alfabeto = list(string.ascii_lowercase + string.ascii_uppercase)
numeros = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
misc = ['\n', ' ', '(', ')', '[', ']', '{', '}', ';', ',', '+', '-', '/', '*', '=', '!', '<', '>']

fullList = alfabeto + numeros + misc

# ESTADOS

estadosInit = ['q0']
estados = estadosInit

estadosID = ['q_ID_1','q_ID_2','q_ID_SPACE','q_ID_LINEBREAK','q_ID_LPAREN','q_ID_RPAREN','q_ID_LBRACKETS','q_ID_RBRACKETS','q_ID_LBRACES','q_ID_RBRACES','q_ID_SEMICOLON','q_ID_COMMA','q_ID_PLUS','q_ID_MINUS','q_ID_DIVIDE','q_ID_TIMES']
estados += estadosID

estadosRETURN = ['q_RETURN_1','q_RETURN_2','q_RETURN_3','q_RETURN_4','q_RETURN_5','q_RETURN_6']
estados += estadosRETURN

estadosVOID = ['q_VOID_1','q_VOID_2','q_VOID_3','q_VOID_4']
estados += estadosVOID

estadosINT = ['q_INT_1','q_INT_2','q_INT_3']
estados += estadosINT

estadosFLOAT = ['q_FLOAT_1','q_FLOAT_2','q_FLOAT_3','q_FLOAT_4','q_FLOAT_5']
estados += estadosFLOAT

estadosIF = ['q_IF_1']
estados += estadosIF

estadosELSE = ['q_ELSE_1','q_ELSE_2','q_ELSE_3','q_ELSE_4']
estados += estadosELSE

estadosLPAREN = ['q_LPAREN']
estados += estadosLPAREN

estadosRPAREN = ['q_RPAREN']
estados += estadosRPAREN

estadosLBRACKETS = ['q_LBRACKETS']
estados += estadosLBRACKETS

estadosRBRACKETS = ['q_RBRACKETS']
estados += estadosRBRACKETS

estadosLBRACES = ['q_LBRACES']
estados += estadosLBRACES

estadosRBRACES = ['q_RBRACES']
estados += estadosRBRACES

estadosSEMICOLON = ['q_SEMICOLON']
estados += estadosSEMICOLON

estadosCOMMA = ['q_COMMA']
estados += estadosCOMMA

estadosPLUS = ['q_PLUS']
estados += estadosPLUS

estadosMINUS = ['q_MINUS']
estados += estadosMINUS

estadosDIVIDE = ['q_DIVIDE']
estados += estadosDIVIDE

estadosTIMES = ['q_TIMES']
estados += estadosTIMES

estadosEQUALS = ['q_ATTRIBUTION_1','q_ATTRIBUTION_2','q_EQUALS_1','q_EQUALS_2']
estados += estadosEQUALS

estadosLESS = ['q_LESS_1','q_LESS_2','q_LESS_EQUAL_1','q_LESS_EQUAL_2']
estados += estadosLESS

estadosGREATER = ['q_GREATER_1','q_GREATER_2','q_GREATER_EQUAL_1','q_GREATER_EQUAL_2']
estados += estadosGREATER

estadosDIFFERENT = ['q_DIFFERENT_1','q_DIFFERENT_2']
estados += estadosDIFFERENT

estadosCOMMENT = ['q_COMMENT_1','q_COMMENT_2','q_COMMENT_3','q_DIVIDE_SPACE','q_DIVIDE_LINEBREAK','q_DIVIDE_LPAREN','q_DIVIDE_RPAREN','q_DIVIDE_LBRACKETS','q_DIVIDE_RBRACKETS','q_DIVIDE_LBRACES','q_DIVIDE_RBRACES','q_DIVIDE_SEMICOLON','q_DIVIDE_COMMA','q_DIVIDE_PLUS','q_DIVIDE_MINUS','q_DIVIDE_DIVIDE','q_DIVIDE_TIMES','q_DIVIDE_NUMERO','q_DIVIDE_ID']
estados += estadosCOMMENT

estadosNUMBER = ['q_NUMERO_1','q_NUMERO_2']
estados += estadosNUMBER

# TRANSIÇÕES

# Função combinar as transições
def combine_transicoes(*transition_dicts):
    combined = defaultdict(dict)

    for transition_dict in transition_dicts:
        for estado, transicoes in transition_dict.items():
            for symbol, next_estado in transicoes.items():
                if symbol not in combined[estado]:
                    combined[estado][symbol] = next_estado

    return dict(combined)

transicoesInit = {
    'q0': {'\n': 'q0',' ' : 'q0',}
}

transicoesINT = {
    'q0':{'i':'q_INT_1'},'q_INT_1':{'n':'q_INT_2'},'q_INT_2':{'t':'q_INT_3'},'q_INT_3':{'\n':'q0',' ':'q0'}
}

transicoesFLOAT = {
    'q0':{'f':'q_FLOAT_1'},'q_FLOAT_1':{'l':'q_FLOAT_2'},'q_FLOAT_2':{'o':'q_FLOAT_3'},'q_FLOAT_3':{'a':'q_FLOAT_4'},'q_FLOAT_4':{'t':'q_FLOAT_5'},'q_FLOAT_5':{'\n':'q0',' ':'q0'}
}

transicoesVOID = {
    'q0':{'v':'q_VOID_1'},'q_VOID_1':{'o':'q_VOID_2'},'q_VOID_2':{'i':'q_VOID_3'},'q_VOID_3':{'d':'q_VOID_4'},'q_VOID_4':{'\n':'q0',' ':'q0'}
}

transicoesRETURN = {
    'q0':{'r':'q_RETURN_1'},'q_RETURN_1':{'e':'q_RETURN_2'},'q_RETURN_2':{'t':'q_RETURN_3'},'q_RETURN_3':{'u':'q_RETURN_4'},'q_RETURN_4':{'r':'q_RETURN_5'},'q_RETURN_5':{'n':'q_RETURN_6'},'q_RETURN_6':{'\n':'q0',' ':'q0'}
}

transicoesIF = {
    'q_INT_1':{'f':'q_IF_1'},'q_IF_1':{'\n':'q0',' ':'q0'}
}

transicoesELSE = {
    'q0':{'e':'q_ELSE_1'},'q_ELSE_1':{'l':'q_ELSE_2'},'q_ELSE_2':{'s':'q_ELSE_3'},'q_ELSE_3':{'e':'q_ELSE_4'},'q_ELSE_4':{'\n':'q0',' ':'q0'}
}

transicoesLPAREN = {
    'q0':{'(':'q_LPAREN'},'q_LPAREN':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},'q_INT_3':{'(':'q_LPAREN'},'q_FLOAT_5':{'(':'q_LPAREN'},'q_VOID_4':{'(':'q_LPAREN'},'q_RETURN_6':{'(':'q_LPAREN'},'q_IF_1':{'(':'q_LPAREN'},'q_ELSE_4':{'(':'q_LPAREN'},'q_NUMERO_1':{'(':'q_LPAREN'},'q_NUMERO_2':{'(':'q_LPAREN'},'q_DIVIDE_NUMERO':{'(':'q_LPAREN'},'q_ID_1':{'(':'q_LPAREN'},'q_ID_2':{'(':'q_LPAREN'},'q_DIVIDE_ID':{'(':'q_LPAREN'}
}

# Acrescentar conexões de q_LPAREN --> q_ID_1 com todas as letras do alfabeto
transicoesLPAREN['q_LPAREN'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_LPAREN --> q_NUMERO_1 com todos os numeros
transicoesLPAREN['q_LPAREN'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_LPAREN --> 'i': 'q_INT_1'
transicoesLPAREN['q_LPAREN'].update({'i': 'q_INT_1'})

# Alterar conexões de q_LPAREN --> 'f': 'q_FLOAT_1'
transicoesLPAREN['q_LPAREN'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_LPAREN --> 'v': 'q_VOID_1'
transicoesLPAREN['q_LPAREN'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_LPAREN --> 'r': 'q_RETURN_1'
transicoesLPAREN['q_LPAREN'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_LPAREN --> 'e': 'q_ELSE_1'
transicoesLPAREN['q_LPAREN'].update({'e': 'q_ELSE_1'})

transicoesRPAREN = {
    'q0': {')':'q_RPAREN'},
    'q_RPAREN': {'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_INT_3': {')':'q_RPAREN'},
    'q_IF_1': {')':'q_RPAREN'},
    'q_ELSE_1': {')':'q_RPAREN'},
    'q_FLOAT_5': {')':'q_RPAREN'},
    'q_VOID_4': {')':'q_RPAREN'},
    'q_RETURN_6': {')':'q_RPAREN'},
    'q_NUMERO_1': {')':'q_RPAREN'},
    'q_NUMERO_2': {')':'q_RPAREN'},
    'q_DIVIDE_NUMERO': {')':'q_RPAREN'},
    'q_ID_1': {')':'q_RPAREN'},
    'q_ID_2': {')':'q_RPAREN'},
    'q_DIVIDE_ID': {')':'q_RPAREN'}
}

# Acrescentar conexões de q_RPAREN --> q_ID_1 com todas as letras do alfabeto
transicoesRPAREN['q_RPAREN'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_RPAREN --> q_NUMERO_1 com todos os numeros
transicoesRPAREN['q_RPAREN'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_RPAREN --> 'i': 'q_INT_1'
transicoesRPAREN['q_RPAREN'].update({'i': 'q_INT_1'})

# Alterar conexões de q_RPAREN --> 'f': 'q_FLOAT_1'
transicoesRPAREN['q_RPAREN'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_RPAREN --> 'v': 'q_VOID_1'
transicoesRPAREN['q_RPAREN'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_RPAREN --> 'r': 'q_RETURN_1'
transicoesRPAREN['q_RPAREN'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_RPAREN --> 'e': 'q_ELSE_1'
transicoesRPAREN['q_RPAREN'].update({'e': 'q_ELSE_1'})

transicoesLBRACKETS = {
    'q0':{'[':'q_LBRACKETS'},
    'q_LBRACKETS':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_INT_3':{'[':'q_LBRACKETS'},
    'q_FLOAT_5':{'[':'q_LBRACKETS'},
    'q_VOID_4':{'[':'q_LBRACKETS'},
    'q_RETURN_6':{'[':'q_LBRACKETS'},
    'q_IF_1':{'[':'q_LBRACKETS'},
    'q_ELSE_4':{'[':'q_LBRACKETS'},
    'q_NUMERO_1':{'[':'q_LBRACKETS'},
    'q_NUMERO_2':{'[':'q_LBRACKETS'},
    'q_DIVIDE_NUMERO':{'[':'q_LBRACKETS'},
    'q_ID_1':{'[':'q_LBRACKETS'},
    'q_ID_2':{'[':'q_LBRACKETS'},
    'q_DIVIDE_ID':{'[':'q_LBRACKETS'}
}

# Acrescentar conexões de q_LBRACKETS --> q_ID_1 com todas as letras do alfabeto
transicoesLBRACKETS['q_LBRACKETS'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_LBRACKETS --> q_NUMERO_1 com todos os numeros
transicoesLBRACKETS['q_LBRACKETS'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_LBRACKETS --> 'i': 'q_INT_1'
transicoesLBRACKETS['q_LBRACKETS'].update({'i': 'q_INT_1'})

# Alterar conexões de q_LBRACKETS --> 'f': 'q_FLOAT_1'
transicoesLBRACKETS['q_LBRACKETS'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_LBRACKETS --> 'v': 'q_VOID_1'
transicoesLBRACKETS['q_LBRACKETS'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_LBRACKETS --> 'r': 'q_RETURN_1'
transicoesLBRACKETS['q_LBRACKETS'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_LBRACKETS --> 'e': 'q_ELSE_1'
transicoesLBRACKETS['q_LBRACKETS'].update({'e': 'q_ELSE_1'})

transicoesRBRACKETS = {
    'q0':{']':'q_RBRACKETS'},'q_RBRACKETS':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},'q_INT_3':{']':'q_RBRACKETS'},'q_IF_1':{']':'q_RBRACKETS'},'q_ELSE_1':{']':'q_RBRACKETS'},'q_FLOAT_5':{']':'q_RBRACKETS'},'q_VOID_4':{']':'q_RBRACKETS'},'q_RETURN_6':{']':'q_RBRACKETS'},'q_NUMERO_1':{']':'q_RBRACKETS'},'q_NUMERO_2':{']':'q_RBRACKETS'},'q_DIVIDE_NUMERO':{']':'q_RBRACKETS'},'q_ID_1':{']':'q_RBRACKETS'},'q_ID_2':{']':'q_RBRACKETS'},'q_DIVIDE_ID':{']':'q_RBRACKETS'}
}

# Acrescentar conexões de q_RBRACKETS --> q_ID_1 com todas as letras do alfabeto
transicoesRBRACKETS['q_RBRACKETS'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_RBRACKETS --> q_NUMERO_1 com todos os numeros
transicoesRBRACKETS['q_RBRACKETS'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_RBRACKETS --> 'i': 'q_INT_1'
transicoesRBRACKETS['q_RBRACKETS'].update({'i': 'q_INT_1'})

# Alterar conexões de q_RBRACKETS --> 'f': 'q_FLOAT_1'
transicoesRBRACKETS['q_RBRACKETS'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_RBRACKETS --> 'v': 'q_VOID_1'
transicoesRBRACKETS['q_RBRACKETS'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_RBRACKETS --> 'r': 'q_RETURN_1'
transicoesRBRACKETS['q_RBRACKETS'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_RBRACKETS --> 'e': 'q_ELSE_1'
transicoesRBRACKETS['q_RBRACKETS'].update({'e': 'q_ELSE_1'})

transicoesLBRACES = {
    'q0':{'{':'q_LBRACES'},'q_LBRACES':{'\n':'q0',' ':'q0'}
}

transicoesRBRACES = {
    'q0':{'}':'q_RBRACES'},'q_RBRACES':{'\n':'q0',' ':'q0'}
}

transicoesSEMICOLON = {
    'q0':{';':'q_SEMICOLON'},'q_SEMICOLON':{'\n':'q0',' ':'q0'},'q_INT_3':{';':'q_SEMICOLON'},'q_IF_1':{';':'q_SEMICOLON'},'q_ELSE_1':{';':'q_SEMICOLON'},'q_FLOAT_5':{';':'q_SEMICOLON'},'q_VOID_4':{';':'q_SEMICOLON'},'q_RETURN_6':{';':'q_SEMICOLON'},'q_NUMERO_1':{';':'q_SEMICOLON'},'q_NUMERO_2':{';':'q_SEMICOLON'},'q_DIVIDE_NUMERO':{';':'q_SEMICOLON'},'q_ID_1':{';':'q_SEMICOLON'},'q_ID_2':{';':'q_SEMICOLON'},'q_DIVIDE_ID':{';':'q_SEMICOLON'}
}

transicoesCOMMA = {
    'q0':{',':'q_COMMA'},'q_COMMA':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},'q_INT_3':{',':'q_COMMA'},'q_IF_1':{';':'q_SEMICOLON'},'q_ELSE_1':{';':'q_SEMICOLON'},'q_FLOAT_5':{',':'q_COMMA'},'q_VOID_4':{',':'q_COMMA'},'q_RETURN_6':{',':'q_COMMA'},'q_NUMERO_1':{',':'q_COMMA'},'q_NUMERO_2':{',':'q_COMMA'},'q_DIVIDE_NUMERO':{',':'q_COMMA'},'q_ID_1':{',':'q_COMMA'},'q_ID_2':{',':'q_COMMA'},'q_DIVIDE_ID':{',':'q_COMMA'}
}

# Acrescentar conexões de q_COMMA --> q_ID_1 com todas as letras do alfabeto
transicoesCOMMA['q_COMMA'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_COMMA --> q_NUMERO_1 com todos os numeros
transicoesCOMMA['q_COMMA'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_COMMA --> 'i': 'q_INT_1'
transicoesCOMMA['q_COMMA'].update({'i': 'q_INT_1'})

# Alterar conexões de q_COMMA --> 'f': 'q_FLOAT_1'
transicoesCOMMA['q_COMMA'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_COMMA --> 'v': 'q_VOID_1'
transicoesCOMMA['q_COMMA'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_COMMA --> 'r': 'q_RETURN_1'
transicoesCOMMA['q_COMMA'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_COMMA --> 'e': 'q_ELSE_1'
transicoesCOMMA['q_COMMA'].update({'e': 'q_ELSE_1'})

transicoesPLUS = {
    'q0':{'+' : 'q_PLUS'},'q_PLUS':{'\n':'q0',' ' :'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',' :'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},'q_INT_3':{'+' : 'q_PLUS'},'q_IF_1':{'+' : 'q_PLUS'},'q_ELSE_1':{'+' : 'q_PLUS'},'q_FLOAT_5':{'+' : 'q_PLUS'},'q_VOID_4':{'+' : 'q_PLUS'},'q_RETURN_6':{'+' : 'q_PLUS'},'q_NUMERO_1':{'+' : 'q_PLUS'},'q_NUMERO_2':{'+' : 'q_PLUS'},'q_DIVIDE_NUMERO':{'+' : 'q_PLUS'},'q_ID_1':{'+' : 'q_PLUS'},'q_ID_2':{'+' : 'q_PLUS'},'q_DIVIDE_ID':{'+' : 'q_PLUS'}
}

# Acrescentar conexões de q_PLUS --> q_ID_1 com todas as letras do alfabeto
transicoesPLUS['q_PLUS'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_PLUS --> q_NUMERO_1 com todos os numeros
transicoesPLUS['q_PLUS'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_PLUS --> 'i': 'q_INT_1'
transicoesPLUS['q_PLUS'].update({'i': 'q_INT_1'})

# Alterar conexões de q_PLUS --> 'f': 'q_FLOAT_1'
transicoesPLUS['q_PLUS'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_PLUS --> 'v': 'q_VOID_1'
transicoesPLUS['q_PLUS'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_PLUS --> 'r': 'q_RETURN_1'
transicoesPLUS['q_PLUS'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_PLUS --> 'e': 'q_ELSE_1'
transicoesPLUS['q_PLUS'].update({'e': 'q_ELSE_1'})

transicoesMINUS = {
    'q0':{'-':'q_MINUS'},'q_MINUS':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},'q_INT_3':{'-':'q_MINUS'},'q_IF_1':{'-':'q_MINUS'},'q_ELSE_1':{'-':'q_MINUS'},'q_FLOAT_5':{'-':'q_MINUS'},'q_VOID_4':{'-':'q_MINUS'},'q_RETURN_6':{'-':'q_MINUS'},'q_NUMERO_1':{'-':'q_MINUS'},'q_NUMERO_2':{'-':'q_MINUS'},'q_DIVIDE_NUMERO':{'-':'q_MINUS'},'q_ID_1':{'-':'q_MINUS'},'q_ID_2':{'-':'q_MINUS'},'q_DIVIDE_ID':{'-':'q_MINUS'}
}

# Acrescentar conexões de q_MINUS --> q_ID_1 com todas as letras do alfabeto
transicoesMINUS['q_MINUS'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_MINUS --> q_NUMERO_1 com todos os numeros
transicoesMINUS['q_MINUS'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_MINUS --> 'i': 'q_INT_1'
transicoesMINUS['q_MINUS'].update({'i': 'q_INT_1'})

# Alterar conexões de q_MINUS --> 'f': 'q_FLOAT_1'
transicoesMINUS['q_MINUS'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_MINUS --> 'v': 'q_VOID_1'
transicoesMINUS['q_MINUS'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_MINUS --> 'r': 'q_RETURN_1'
transicoesMINUS['q_MINUS'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_MINUS --> 'e': 'q_ELSE_1'
transicoesMINUS['q_MINUS'].update({'e': 'q_ELSE_1'})

transicoesDIVIDE = {
    'q_DIVIDE':{'\\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_INT_3':{'/':'q_COMMENT_1'},
    'q_IF_1':{'/':'q_COMMENT_1'},
    'q_ELSE_1':{'/':'q_COMMENT_1'},
    'q_FLOAT_5':{'/':'q_COMMENT_1'},
    'q_VOID_4':{'/':'q_COMMENT_1'},
    'q_RETURN_6':{'/':'q_COMMENT_1'},
    'q_NUMERO_1':{'/':'q_COMMENT_1'},
    'q_NUMERO_2':{'/':'q_COMMENT_1'},
    'q_DIVIDE_NUMERO':{'/':'q_COMMENT_1'},
    'q_ID_1':{'/':'q_COMMENT_1'},
    'q_ID_2':{'/':'q_COMMENT_1'},
    'q_DIVIDE_ID':{'/':'q_COMMENT_1'}
}

# Acrescentar conexões de q_DIVIDE --> q_ID_1 com todas as letras do alfabeto
transicoesDIVIDE['q_DIVIDE'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_DIVIDE --> q_NUMERO_1 com todos os numeros
transicoesDIVIDE['q_DIVIDE'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_DIVIDE --> 'i': 'q_INT_1'
transicoesDIVIDE['q_DIVIDE'].update({'i': 'q_INT_1'})

# Alterar conexões de q_DIVIDE --> 'f': 'q_FLOAT_1'
transicoesDIVIDE['q_DIVIDE'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_DIVIDE --> 'v': 'q_VOID_1'
transicoesDIVIDE['q_DIVIDE'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_DIVIDE --> 'r': 'q_RETURN_1'
transicoesDIVIDE['q_DIVIDE'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_DIVIDE --> 'e': 'q_ELSE_1'
transicoesDIVIDE['q_DIVIDE'].update({'e': 'q_ELSE_1'})

transicoesTIMES = {
    'q0':{'*':'q_TIMES'},
    'q_TIMES':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_INT_3':{'*':'q_TIMES'},
    'q_IF_1':{'*':'q_TIMES'},
    'q_ELSE_1':{'*':'q_TIMES'},
    'q_FLOAT_5':{'*':'q_TIMES'},
    'q_VOID_4':{'*':'q_TIMES'},
    'q_RETURN_6':{'*':'q_TIMES'},
    'q_NUMERO_1':{'*':'q_TIMES'},
    'q_NUMERO_2':{'*':'q_TIMES'},
    'q_DIVIDE_NUMERO':{'*':'q_TIMES'},
    'q_ID_1':{'*':'q_TIMES'},
    'q_ID_2':{'*':'q_TIMES'},
    'q_DIVIDE_ID':{'*':'q_TIMES'}
}

# Acrescentar conexões de q_TIMES --> q_ID_1 com todas as letras do alfabeto
transicoesTIMES['q_TIMES'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_TIMES --> q_NUMERO_1 com todos os numeros
transicoesTIMES['q_TIMES'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_TIMES --> 'i': 'q_INT_1'
transicoesTIMES['q_TIMES'].update({'i': 'q_INT_1'})

# Alterar conexões de q_TIMES --> 'f': 'q_FLOAT_1'
transicoesTIMES['q_TIMES'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_TIMES --> 'v': 'q_VOID_1'
transicoesTIMES['q_TIMES'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_TIMES --> 'r': 'q_RETURN_1'
transicoesTIMES['q_TIMES'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_TIMES --> 'e': 'q_ELSE_1'
transicoesTIMES['q_TIMES'].update({'e': 'q_ELSE_1'})

transicoesEQUALS = {
    'q0':{'=':'q_ATTRIBUTION_1'},
    'q_ATTRIBUTION_1':{'\n':'q_ATTRIBUTION_2',' ':'q_ATTRIBUTION_2','=':'q_EQUALS_1'},
    'q_ATTRIBUTION_2':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_EQUALS_1':{'\n':'q_EQUALS_2',' ':'q_EQUALS_2'},
    'q_EQUALS_2':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'}
}

"""
    Busca por todas as opções possiveis após q_ATTRIBUTION_2
"""

# Acrescentar conexões de q_ATTRIBUTION_2 --> q_ID_1 com todas as letras do alfabeto
transicoesEQUALS['q_ATTRIBUTION_2'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_ATTRIBUTION_2 --> q_NUMERO_1 com todos os numeros
transicoesEQUALS['q_ATTRIBUTION_2'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_ATTRIBUTION_2 --> 'i': 'q_INT_1'
transicoesEQUALS['q_ATTRIBUTION_2'].update({'i': 'q_INT_1'})

# Alterar conexões de q_ATTRIBUTION_2 --> 'f': 'q_FLOAT_1'
transicoesEQUALS['q_ATTRIBUTION_2'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_ATTRIBUTION_2 --> 'v': 'q_VOID_1'
transicoesEQUALS['q_ATTRIBUTION_2'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_ATTRIBUTION_2 --> 'r': 'q_RETURN_6'
transicoesEQUALS['q_ATTRIBUTION_2'].update({'r': 'q_RETURN_6'})

"""
    Busca por todas as opções possiveis após q_EQUALS_2
"""

# Acrescentar conexões de q_EQUALS_2 --> q_ID_1 com todas as letras do alfabeto
transicoesEQUALS['q_EQUALS_2'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_EQUALS_2 --> q_NUMERO_1 com todos os numeros
transicoesEQUALS['q_EQUALS_2'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_EQUALS_2 --> 'i': 'q_INT_1'
transicoesEQUALS['q_EQUALS_2'].update({'i': 'q_INT_1'})

# Alterar conexões de q_EQUALS_2 --> 'f': 'q_FLOAT_1'
transicoesEQUALS['q_EQUALS_2'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_EQUALS_2 --> 'v': 'q_VOID_1'
transicoesEQUALS['q_EQUALS_2'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_EQUALS_2 --> 'r': 'q_RETURN_6'
transicoesEQUALS['q_EQUALS_2'].update({'r': 'q_RETURN_6'})

transicoesLESS = {
    'q0':{'<':'q_LESS_1'},
    'q_LESS_1':{'\n':'q_LESS_2',' ':'q_LESS_2','=':'q_LESS_EQUAL_1'},
    'q_LESS_2':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_LESS_EQUAL_1':{'\n':'q_LESS_EQUAL_2',' ':'q_LESS_EQUAL_2'},
    'q_LESS_EQUAL_2':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'}
}

"""
    Busca por todas as opções possiveis após q_LESS_2
"""

# Acrescentar conexões de q_LESS_2 --> q_ID_1 com todas as letras do alfabeto
transicoesLESS['q_LESS_2'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_LESS_2 --> q_NUMERO_1 com todos os numeros
transicoesLESS['q_LESS_2'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_LESS_2 --> 'i': 'q_INT_1'
transicoesLESS['q_LESS_2'].update({'i': 'q_INT_1'})

# Alterar conexões de q_LESS_2 --> 'f': 'q_FLOAT_1'
transicoesLESS['q_LESS_2'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_LESS_2 --> 'v': 'q_VOID_1'
transicoesLESS['q_LESS_2'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_LESS_2 --> 'r': 'q_RETURN_6'
transicoesLESS['q_LESS_2'].update({'r': 'q_RETURN_6'})

"""
    Busca por todas as opções possiveis após q_LESS_EQUAL_2
"""

# Acrescentar conexões de q_LESS_EQUAL_2 --> q_ID_1 com todas as letras do alfabeto
transicoesLESS['q_LESS_EQUAL_2'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_LESS_EQUAL_2 --> q_NUMERO_1 com todos os numeros
transicoesLESS['q_LESS_EQUAL_2'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_LESS_EQUAL_2 --> 'i': 'q_INT_1'
transicoesLESS['q_LESS_EQUAL_2'].update({'i': 'q_INT_1'})

# Alterar conexões de q_LESS_EQUAL_2 --> 'f': 'q_FLOAT_1'
transicoesLESS['q_LESS_EQUAL_2'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_LESS_EQUAL_2 --> 'v': 'q_VOID_1'
transicoesLESS['q_LESS_EQUAL_2'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_LESS_EQUAL_2 --> 'r': 'q_RETURN_6'
transicoesLESS['q_LESS_EQUAL_2'].update({'r': 'q_RETURN_6'})

transicoesGREATER = {
    'q0':{'>':'q_GREATER_1'},
    'q_GREATER_1':{'\n':'q_GREATER_2',' ':'q_GREATER_2','=':'q_GREATER_EQUAL_1'},
    'q_GREATER_2':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_GREATER_EQUAL_1':{'\n':'q_GREATER_EQUAL_2',' ':'q_GREATER_EQUAL_2'},
    'q_GREATER_EQUAL_2':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'}
}

"""
    Busca por todas as opções possiveis após q_GREATER_2
"""

# Acrescentar conexões de q_GREATER_2 --> q_ID_1 com todas as letras do alfabeto
transicoesGREATER['q_GREATER_2'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_GREATER_2 --> q_NUMERO_1 com todos os numeros
transicoesGREATER['q_GREATER_2'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_GREATER_2 --> 'i': 'q_INT_1'
transicoesGREATER['q_GREATER_2'].update({'i': 'q_INT_1'})

# Alterar conexões de q_GREATER_2 --> 'f': 'q_FLOAT_1'
transicoesGREATER['q_GREATER_2'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_GREATER_2 --> 'v': 'q_VOID_1'
transicoesGREATER['q_GREATER_2'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_GREATER_2 --> 'r': 'q_RETURN_6'
transicoesGREATER['q_GREATER_2'].update({'r': 'q_RETURN_6'})

"""
    Busca por todas as opções possiveis após q_GREATER_EQUAL_2
"""

# Acrescentar conexões de q_GREATER_EQUAL_2 --> q_ID_1 com todas as letras do alfabeto
transicoesGREATER['q_GREATER_EQUAL_2'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_GREATER_EQUAL_2 --> q_NUMERO_1 com todos os numeros
transicoesGREATER['q_GREATER_EQUAL_2'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_GREATER_EQUAL_2 --> 'i': 'q_INT_1'
transicoesGREATER['q_GREATER_EQUAL_2'].update({'i': 'q_INT_1'})

# Alterar conexões de q_GREATER_EQUAL_2 --> 'f': 'q_FLOAT_1'
transicoesGREATER['q_GREATER_EQUAL_2'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_GREATER_EQUAL_2 --> 'v': 'q_VOID_1'
transicoesGREATER['q_GREATER_EQUAL_2'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_GREATER_EQUAL_2 --> 'r': 'q_RETURN_6'
transicoesGREATER['q_GREATER_EQUAL_2'].update({'r': 'q_RETURN_6'})

transicoesDIFFERENT = {
    'q0':{'!':'q_DIFFERENT_1'},
    'q_DIFFERENT_1':{'=':'q_DIFFERENT_2'},
    'q_DIFFERENT_2':{' ':'q0','\n':'q0'}
}

transicoesCOMMENT = {
    'q0':{'/':'q_COMMENT_1'},
    'q_COMMENT_1':{'*':'q_COMMENT_2',' ':'q_DIVIDE_SPACE','\n':'q_DIVIDE_LINEBREAK','(':'q_DIVIDE_LPAREN',')':'q_DIVIDE_RPAREN','[':'q_DIVIDE_LBRACKETS',']':'q_DIVIDE_RBRACKETS','{':'q_DIVIDE_LBRACES','}':'q_DIVIDE_RBRACES',';':'q_DIVIDE_SEMICOLON',',':'q_DIVIDE_COMMA','+':'q_DIVIDE_PLUS','-':'q_DIVIDE_MINUS','/':'q_DIVIDE_DIVIDE'},
    'q_COMMENT_2':{'*':'q_COMMENT_3'},
    'q_COMMENT_3':{'/':'q0'},
    'q_DIVIDE_SPACE':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_DIVIDE_LINEBREAK':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_DIVIDE_LPAREN':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_DIVIDE_RPAREN':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_DIVIDE_LBRACKETS':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_DIVIDE_RBRACKETS':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_DIVIDE_LBRACES':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_DIVIDE_RBRACES':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_DIVIDE_SEMICOLON':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_DIVIDE_COMMA':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_DIVIDE_PLUS':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_DIVIDE_MINUS':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_DIVIDE_DIVIDE':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_DIVIDE_TIMES':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_DIVIDE_NUMERO':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_DIVIDE_ID':{'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'}
}


# Acrescentar conexões de q_COMMENT_2 --> q_COMMENT_2 com todos os numeros
transicoesCOMMENT['q_COMMENT_2'].update({item: 'q_COMMENT_2' for item in fullList})

# Acrescentar conexões de q_COMMENT_2 --> '*': 'q_COMMENT_3'
transicoesCOMMENT['q_COMMENT_2'].update({'*': 'q_COMMENT_3'})

# Acrescentar conexões de q_COMMENT_3 --> q_COMMENT_2 com todos os numeros
transicoesCOMMENT['q_COMMENT_3'].update({item: 'q_COMMENT_2' for item in fullList})

# Acrescentar conexões de q_COMMENT_3 --> '*': 'q_COMMENT_3'
transicoesCOMMENT['q_COMMENT_3'].update({'*': 'q_COMMENT_3'})

# Acrescentar conexões de q_COMMENT_3 --> '/': 'q0'
transicoesCOMMENT['q_COMMENT_3'].update({'/': 'q0'})

"""
    DIVIDE seguido de SPACE
"""

# Acrescentar conexões de q_DIVIDE_SPACE --> q_ID_1 com todas as letras do alfabeto
transicoesCOMMENT['q_DIVIDE_SPACE'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_DIVIDE_SPACE --> q_NUMERO_1 com todos os numeros
transicoesCOMMENT['q_DIVIDE_SPACE'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_DIVIDE_SPACE --> 'i': 'q_INT_1'
transicoesCOMMENT['q_DIVIDE_SPACE'].update({'i': 'q_INT_1'})

# Alterar conexões de q_DIVIDE_SPACE --> 'f': 'q_FLOAT_1'
transicoesCOMMENT['q_DIVIDE_SPACE'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_DIVIDE_SPACE --> 'v': 'q_VOID_1'
transicoesCOMMENT['q_DIVIDE_SPACE'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_DIVIDE_SPACE --> 'r': 'q_RETURN_1'
transicoesCOMMENT['q_DIVIDE_SPACE'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_DIVIDE_SPACE --> 'e': 'q_ELSE_1'
transicoesCOMMENT['q_DIVIDE_SPACE'].update({'e': 'q_ELSE_1'})

"""
    DIVIDE seguido de LINEBREAK
"""

# Acrescentar conexões de q_DIVIDE_LINEBREAK --> q_ID_1 com todas as letras do alfabeto
transicoesCOMMENT['q_DIVIDE_LINEBREAK'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_DIVIDE_LINEBREAK --> q_NUMERO_1 com todos os numeros
transicoesCOMMENT['q_DIVIDE_LINEBREAK'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_DIVIDE_LINEBREAK --> 'i': 'q_INT_1'
transicoesCOMMENT['q_DIVIDE_LINEBREAK'].update({'i': 'q_INT_1'})

# Alterar conexões de q_DIVIDE_LINEBREAK --> 'f': 'q_FLOAT_1'
transicoesCOMMENT['q_DIVIDE_LINEBREAK'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_DIVIDE_LINEBREAK --> 'v': 'q_VOID_1'
transicoesCOMMENT['q_DIVIDE_LINEBREAK'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_DIVIDE_LINEBREAK --> 'r': 'q_RETURN_1'
transicoesCOMMENT['q_DIVIDE_LINEBREAK'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_DIVIDE_LINEBREAK --> 'e': 'q_ELSE_1'
transicoesCOMMENT['q_DIVIDE_LINEBREAK'].update({'e': 'q_ELSE_1'})

"""
    DIVIDE seguido de LPAREN
"""

# Acrescentar conexões de q_DIVIDE_LPAREN --> q_ID_1 com todas as letras do alfabeto
transicoesCOMMENT['q_DIVIDE_LPAREN'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_DIVIDE_LPAREN --> q_NUMERO_1 com todos os numeros
transicoesCOMMENT['q_DIVIDE_LPAREN'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_DIVIDE_LPAREN --> 'i': 'q_INT_1'
transicoesCOMMENT['q_DIVIDE_LPAREN'].update({'i': 'q_INT_1'})

# Alterar conexões de q_DIVIDE_LPAREN --> 'f': 'q_FLOAT_1'
transicoesCOMMENT['q_DIVIDE_LPAREN'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_DIVIDE_LPAREN --> 'v': 'q_VOID_1'
transicoesCOMMENT['q_DIVIDE_LPAREN'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_DIVIDE_LPAREN --> 'r': 'q_RETURN_1'
transicoesCOMMENT['q_DIVIDE_LPAREN'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_DIVIDE_LPAREN --> 'e': 'q_ELSE_1'
transicoesCOMMENT['q_DIVIDE_LPAREN'].update({'e': 'q_ELSE_1'})

"""
    DIVIDE seguido de RPAREN
"""

# Acrescentar conexões de q_DIVIDE_RPAREN --> q_ID_1 com todas as letras do alfabeto
transicoesCOMMENT['q_DIVIDE_RPAREN'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_DIVIDE_RPAREN --> q_NUMERO_1 com todos os numeros
transicoesCOMMENT['q_DIVIDE_RPAREN'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_DIVIDE_RPAREN --> 'i': 'q_INT_1'
transicoesCOMMENT['q_DIVIDE_RPAREN'].update({'i': 'q_INT_1'})

# Alterar conexões de q_DIVIDE_RPAREN --> 'f': 'q_FLOAT_1'
transicoesCOMMENT['q_DIVIDE_RPAREN'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_DIVIDE_RPAREN --> 'v': 'q_VOID_1'
transicoesCOMMENT['q_DIVIDE_RPAREN'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_DIVIDE_RPAREN --> 'r': 'q_RETURN_1'
transicoesCOMMENT['q_DIVIDE_RPAREN'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_DIVIDE_RPAREN --> 'e': 'q_ELSE_1'
transicoesCOMMENT['q_DIVIDE_RPAREN'].update({'e': 'q_ELSE_1'})

"""
    DIVIDE seguido de COMMA
"""

# Acrescentar conexões de q_DIVIDE_COMMA --> q_ID_1 com todas as letras do alfabeto
transicoesCOMMENT['q_DIVIDE_COMMA'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_DIVIDE_COMMA --> q_NUMERO_1 com todos os numeros
transicoesCOMMENT['q_DIVIDE_COMMA'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_DIVIDE_COMMA --> 'i': 'q_INT_1'
transicoesCOMMENT['q_DIVIDE_COMMA'].update({'i': 'q_INT_1'})

# Alterar conexões de q_DIVIDE_COMMA --> 'f': 'q_FLOAT_1'
transicoesCOMMENT['q_DIVIDE_COMMA'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_DIVIDE_COMMA --> 'v': 'q_VOID_1'
transicoesCOMMENT['q_DIVIDE_COMMA'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_DIVIDE_COMMA --> 'e': 'q_ELSE_1'
transicoesCOMMENT['q_DIVIDE_COMMA'].update({'e': 'q_ELSE_1'})

"""
    DIVIDE seguido de PLUS
"""

# Acrescentar conexões de q_DIVIDE_PLUS --> q_ID_1 com todas as letras do alfabeto
transicoesCOMMENT['q_DIVIDE_PLUS'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_DIVIDE_PLUS --> q_NUMERO_1 com todos os numeros
transicoesCOMMENT['q_DIVIDE_PLUS'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_DIVIDE_PLUS --> 'i': 'q_INT_1'
transicoesCOMMENT['q_DIVIDE_PLUS'].update({'i': 'q_INT_1'})

# Alterar conexões de q_DIVIDE_PLUS --> 'f': 'q_FLOAT_1'
transicoesCOMMENT['q_DIVIDE_PLUS'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_DIVIDE_PLUS --> 'v': 'q_VOID_1'
transicoesCOMMENT['q_DIVIDE_PLUS'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_DIVIDE_PLUS --> 'r': 'q_RETURN_1'
transicoesCOMMENT['q_DIVIDE_PLUS'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_DIVIDE_PLUS --> 'e': 'q_ELSE_1'
transicoesCOMMENT['q_DIVIDE_PLUS'].update({'e': 'q_ELSE_1'})

"""
    DIVIDE seguido de MINUS
"""

# Acrescentar conexões de q_DIVIDE_MINUS --> q_ID_1 com todas as letras do alfabeto
transicoesCOMMENT['q_DIVIDE_MINUS'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_DIVIDE_MINUS --> q_NUMERO_1 com todos os numeros
transicoesCOMMENT['q_DIVIDE_MINUS'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_DIVIDE_MINUS --> 'i': 'q_INT_1'
transicoesCOMMENT['q_DIVIDE_MINUS'].update({'i': 'q_INT_1'})

# Alterar conexões de q_DIVIDE_MINUS --> 'f': 'q_FLOAT_1'
transicoesCOMMENT['q_DIVIDE_MINUS'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_DIVIDE_MINUS --> 'v': 'q_VOID_1'
transicoesCOMMENT['q_DIVIDE_MINUS'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_DIVIDE_MINUS --> 'r': 'q_RETURN_1'
transicoesCOMMENT['q_DIVIDE_MINUS'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_DIVIDE_MINUS --> 'e': 'q_ELSE_1'
transicoesCOMMENT['q_DIVIDE_MINUS'].update({'e': 'q_ELSE_1'})

"""
    DIVIDE seguido de DIVIDE
"""

# Acrescentar conexões de q_DIVIDE_DIVIDE --> q_ID_1 com todas as letras do alfabeto
transicoesCOMMENT['q_DIVIDE_DIVIDE'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_DIVIDE_DIVIDE --> q_NUMERO_1 com todos os numeros
transicoesCOMMENT['q_DIVIDE_DIVIDE'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_DIVIDE_DIVIDE --> 'i': 'q_INT_1'
transicoesCOMMENT['q_DIVIDE_DIVIDE'].update({'i': 'q_INT_1'})

# Alterar conexões de q_DIVIDE_DIVIDE --> 'f': 'q_FLOAT_1'
transicoesCOMMENT['q_DIVIDE_DIVIDE'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_DIVIDE_DIVIDE --> 'v': 'q_VOID_1'
transicoesCOMMENT['q_DIVIDE_DIVIDE'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_DIVIDE_DIVIDE --> 'r': 'q_RETURN_1'
transicoesCOMMENT['q_DIVIDE_DIVIDE'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_DIVIDE_DIVIDE --> 'e': 'q_ELSE_1'
transicoesCOMMENT['q_DIVIDE_DIVIDE'].update({'e': 'q_ELSE_1'})

"""
    DIVIDE seguido de TIMES
"""

# Acrescentar conexões de q_DIVIDE_TIMES --> q_ID_1 com todas as letras do alfabeto
transicoesCOMMENT['q_DIVIDE_TIMES'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_DIVIDE_TIMES --> q_NUMERO_1 com todos os numeros
transicoesCOMMENT['q_DIVIDE_TIMES'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_DIVIDE_TIMES --> 'i': 'q_INT_1'
transicoesCOMMENT['q_DIVIDE_TIMES'].update({'i': 'q_INT_1'})

# Alterar conexões de q_DIVIDE_TIMES --> 'f': 'q_FLOAT_1'
transicoesCOMMENT['q_DIVIDE_TIMES'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_DIVIDE_TIMES --> 'v': 'q_VOID_1'
transicoesCOMMENT['q_DIVIDE_TIMES'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_DIVIDE_TIMES --> 'r': 'q_RETURN_1'
transicoesCOMMENT['q_DIVIDE_TIMES'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_DIVIDE_TIMES --> 'e': 'q_ELSE_1'
transicoesCOMMENT['q_DIVIDE_TIMES'].update({'e': 'q_ELSE_1'})

"""
    DIVIDE seguido de NUMBER
"""

# Acrescentar conexões de q_COMMENT_1 --> q_NUMERO_1 com todos os numeros
transicoesCOMMENT['q_COMMENT_1'].update({number: 'q_DIVIDE_NUMERO' for number in numeros})

# Acrescentar conexões de q_DIVIDE_NUMERO --> q_NUMERO_2 com todos os numeros
transicoesCOMMENT['q_DIVIDE_NUMERO'].update({number: 'q_NUMERO_2' for number in numeros})

"""
    DIVIDE seguido de ID
"""

# Acrescentar conexões de q_COMMENT_1 --> DIVIDE_ID com todas as letras do alfabeto
transicoesCOMMENT['q_COMMENT_1'].update({letter: 'q_DIVIDE_ID' for letter in alfabeto})

# Acrescentar conexões de q_DIVIDE_ID --> q_ID_2 com todas as letras do alfabeto e todos os numeros
transicoesCOMMENT['q_DIVIDE_ID'].update({letter: 'q_ID_2' for letter in alfabeto})
transicoesCOMMENT['q_DIVIDE_ID'].update({number: 'q_ID_2' for number in numeros})

transicoesNUMBER = {
    'q0': {},
    'q_NUMERO_1': {'\n': 'q0',' ' : 'q0',},
    'q_NUMERO_2': {'\n': 'q0',' ' : 'q0',}
}

# Acrescentar conexões de q0 --> q_NUMERO_1 com todos os numeros
transicoesNUMBER['q0'].update({number: 'q_NUMERO_1' for number in numeros})

# Acrescentar conexões de q_NUMERO_1 --> q_NUMERO_2 com todos os numeros
transicoesNUMBER['q_NUMERO_1'].update({number: 'q_NUMERO_2' for number in numeros})

# Acrescentar conexões de q_NUMERO_2 --> q_NUMERO_2 com todos os numeros
transicoesNUMBER['q_NUMERO_2'].update({number: 'q_NUMERO_2' for number in numeros})

transicoesID = {
    'q0': {},
    'q_ID_1': {'\n':'q0',' ':'q0'},
    'q_ID_2': {'\n':'q0',' ':'q0'},
    'q_ID_SPACE': {'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_ID_LINEBREAK': {'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_ID_LPAREN': {'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_ID_RPAREN': {'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_ID_LBRACES': {'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_ID_RBRACES': {'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_ID_SEMICOLON': {'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_ID_COMMA': {'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_ID_PLUS': {'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_ID_MINUS': {'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_ID_DIVIDE': {'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_ID_TIMES': {'\n':'q0',' ':'q0','(':'q_LPAREN',')':'q_RPAREN','[':'q_LBRACKETS',']':'q_RBRACKETS','{':'q_LBRACES','}':'q_RBRACES',';':'q_SEMICOLON',',':'q_COMMA','+':'q_PLUS','-':'q_MINUS','/':'q_COMMENT_1','*':'q_TIMES','=':'q_ATTRIBUTION_1','<':'q_LESS_1','>':'q_GREATER_1'},
    'q_INT_1': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_INT_2': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_INT_3': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_IF_1': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_ELSE_1': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_ELSE_2': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_ELSE_3': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_ELSE_4': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_FLOAT_1': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_FLOAT_2': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_FLOAT_3': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_FLOAT_4': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_FLOAT_5': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_VOID_1': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_VOID_2': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_VOID_3': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_VOID_4': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_RETURN_1': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_RETURN_2': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_RETURN_3': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_RETURN_4': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_RETURN_5': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'},
    'q_RETURN_6': {' ':'q_ID_SPACE','\n':'q_ID_LINEBREAK','(':'q_ID_LPAREN',')':'q_ID_RPAREN','[':'q_ID_LBRACKETS',']':'q_ID_RBRACKETS','{':'q_ID_LBRACES','}':'q_ID_RBRACES',';':'q_ID_SEMICOLON',',':'q_ID_COMMA','+':'q_ID_PLUS','-':'q_ID_MINUS','/':'q_ID_DIVIDE','*':'q_ID_TIMES'}
}

# Acrescentar conexões de q0 --> q_ID_1 com todas as letras do alfabeto
transicoesID['q0'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_ID_1 --> q_ID_2 com todas as letras do alfabeto e todos os numeros
transicoesID['q_ID_1'].update({letter: 'q_ID_2' for letter in alfabeto})
transicoesID['q_ID_1'].update({number: 'q_ID_2' for number in numeros})

# Acrescentar conexões de q_ID_2 --> q_ID_2 com todas as letras do alfabeto e todos os numeros
transicoesID['q_ID_2'].update({letter: 'q_ID_2' for letter in alfabeto})
transicoesID['q_ID_2'].update({number: 'q_ID_2' for number in numeros})

"""
    Busca de ID em meio a busca INT
"""

# Acrescentar conexões de q_INT_1 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_INT_1'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_INT_1'].update({number: 'q_ID_1' for number in numeros})

# Acrescentar conexões de q_INT_2 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_INT_2'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_INT_2'].update({number: 'q_ID_1' for number in numeros})

# Acrescentar conexões de q_INT_3 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_INT_3'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_INT_3'].update({number: 'q_ID_1' for number in numeros})

"""
    Busca de ID em meio a busca FLOAT
"""

# Acrescentar conexões de q_FLOAT_1 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_FLOAT_1'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_FLOAT_1'].update({number: 'q_ID_1' for number in numeros})

# Acrescentar conexões de q_FLOAT_2 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_FLOAT_2'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_FLOAT_2'].update({number: 'q_ID_1' for number in numeros})

# Acrescentar conexões de q_FLOAT_3 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_FLOAT_3'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_FLOAT_3'].update({number: 'q_ID_1' for number in numeros})

# Acrescentar conexões de q_FLOAT_4 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_FLOAT_4'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_FLOAT_4'].update({number: 'q_ID_1' for number in numeros})

# Acrescentar conexões de q_FLOAT_5 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_FLOAT_5'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_FLOAT_5'].update({number: 'q_ID_1' for number in numeros})

"""
    Busca de ID em meio a busca VOID
"""

# Acrescentar conexões de q_VOID_1 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_VOID_1'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_VOID_1'].update({number: 'q_ID_1' for number in numeros})

# Acrescentar conexões de q_VOID_2 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_VOID_2'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_VOID_2'].update({number: 'q_ID_1' for number in numeros})

# Acrescentar conexões de q_VOID_3 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_VOID_3'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_VOID_3'].update({number: 'q_ID_1' for number in numeros})

# Acrescentar conexões de q_VOID_4 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_VOID_4'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_VOID_4'].update({number: 'q_ID_1' for number in numeros})

"""
    Busca de ID em meio a busca RETURN
"""

# Acrescentar conexões de q_RETURN_1 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_RETURN_1'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_RETURN_1'].update({number: 'q_ID_1' for number in numeros})

# Acrescentar conexões de q_RETURN_2 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_RETURN_2'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_RETURN_2'].update({number: 'q_ID_1' for number in numeros})

# Acrescentar conexões de q_RETURN_3 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_RETURN_3'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_RETURN_3'].update({number: 'q_ID_1' for number in numeros})

# Acrescentar conexões de q_RETURN_4 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_RETURN_4'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_RETURN_4'].update({number: 'q_ID_1' for number in numeros})

# Acrescentar conexões de q_RETURN_5 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_RETURN_5'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_RETURN_5'].update({number: 'q_ID_1' for number in numeros})

# Acrescentar conexões de q_RETURN_6 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_RETURN_6'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_RETURN_6'].update({number: 'q_ID_1' for number in numeros})

"""
    Busca de ID em meio a busca IF
"""

# Acrescentar conexões de q_IF_1 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_IF_1'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_IF_1'].update({number: 'q_ID_1' for number in numeros})

"""
    Busca de ID em meio a busca ELSE
"""

# Acrescentar conexões de q_ELSE_1 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_ELSE_1'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_ELSE_1'].update({number: 'q_ID_1' for number in numeros})

# Acrescentar conexões de q_ELSE_2 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_ELSE_2'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_ELSE_2'].update({number: 'q_ID_1' for number in numeros})

# Acrescentar conexões de q_ELSE_3 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_ELSE_3'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_ELSE_3'].update({number: 'q_ID_1' for number in numeros})

# Acrescentar conexões de q_ELSE_4 --> q_ID_1 com todas as letras do alfabeto e todos os numeros
transicoesID['q_ELSE_4'].update({letter: 'q_ID_1' for letter in alfabeto})
transicoesID['q_ELSE_4'].update({number: 'q_ID_1' for number in numeros})

"""
    ID seguido de SPACE
"""

# Acrescentar conexões de q_ID_SPACE --> q_ID_1 com todas as letras do alfabeto
transicoesID['q_ID_SPACE'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_ID_SPACE --> q_NUMERO_1 com todos os numeros
transicoesID['q_ID_SPACE'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_ID_SPACE --> 'i': 'q_INT_1'
transicoesID['q_ID_SPACE'].update({'i': 'q_INT_1'})

# Alterar conexões de q_ID_SPACE --> 'f': 'q_FLOAT_1'
transicoesID['q_ID_SPACE'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_ID_SPACE --> 'v': 'q_VOID_1'
transicoesID['q_ID_SPACE'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_ID_SPACE --> 'r': 'q_RETURN_1'
transicoesID['q_ID_SPACE'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_ID_SPACE --> 'e': 'q_ELSE_1'
transicoesID['q_ID_SPACE'].update({'e': 'q_ELSE_1'})

"""
    ID seguido de LINEBREAK
"""

# Acrescentar conexões de q_ID_LINEBREAK --> q_ID_1 com todas as letras do alfabeto
transicoesID['q_ID_LINEBREAK'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_ID_LINEBREAK --> q_NUMERO_1 com todos os numeros
transicoesID['q_ID_LINEBREAK'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_ID_LINEBREAK --> 'i': 'q_INT_1'
transicoesID['q_ID_LINEBREAK'].update({'i': 'q_INT_1'})

# Alterar conexões de q_ID_LINEBREAK --> 'f': 'q_FLOAT_1'
transicoesID['q_ID_LINEBREAK'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_ID_LINEBREAK --> 'v': 'q_VOID_1'
transicoesID['q_ID_LINEBREAK'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_ID_LINEBREAK --> 'r': 'q_RETURN_1'
transicoesID['q_ID_LINEBREAK'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_ID_LINEBREAK --> 'e': 'q_ELSE_1'
transicoesID['q_ID_LINEBREAK'].update({'e': 'q_ELSE_1'})

"""
    ID seguido de LPAREN
"""

# Acrescentar conexões de q_ID_LPAREN --> q_ID_1 com todas as letras do alfabeto
transicoesID['q_ID_LPAREN'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_ID_LPAREN --> q_NUMERO_1 com todos os numeros
transicoesID['q_ID_LPAREN'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_ID_LPAREN --> 'i': 'q_INT_1'
transicoesID['q_ID_LPAREN'].update({'i': 'q_INT_1'})

# Alterar conexões de q_ID_LPAREN --> 'f': 'q_FLOAT_1'
transicoesID['q_ID_LPAREN'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_ID_LPAREN --> 'v': 'q_VOID_1'
transicoesID['q_ID_LPAREN'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_ID_LPAREN --> 'r': 'q_RETURN_1'
transicoesID['q_ID_LPAREN'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_ID_LPAREN --> 'e': 'q_ELSE_1'
transicoesID['q_ID_LPAREN'].update({'e': 'q_ELSE_1'})

"""
    ID seguido de RPAREN
"""

# Acrescentar conexões de q_ID_RPAREN --> q_ID_1 com todas as letras do alfabeto
transicoesID['q_ID_RPAREN'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_ID_RPAREN --> q_NUMERO_1 com todos os numeros
transicoesID['q_ID_RPAREN'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_ID_RPAREN --> 'i': 'q_INT_1'
transicoesID['q_ID_RPAREN'].update({'i': 'q_INT_1'})

# Alterar conexões de q_ID_RPAREN --> 'f': 'q_FLOAT_1'
transicoesID['q_ID_RPAREN'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_ID_RPAREN --> 'v': 'q_VOID_1'
transicoesID['q_ID_RPAREN'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_ID_RPAREN --> 'r': 'q_RETURN_1'
transicoesID['q_ID_RPAREN'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_ID_RPAREN --> 'e': 'q_ELSE_1'
transicoesID['q_ID_RPAREN'].update({'e': 'q_ELSE_1'})

"""
    ID seguido de COMMA
"""

# Acrescentar conexões de q_ID_COMMA --> q_ID_1 com todas as letras do alfabeto
transicoesID['q_ID_COMMA'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_ID_COMMA --> q_NUMERO_1 com todos os numeros
transicoesID['q_ID_COMMA'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_ID_COMMA --> 'i': 'q_INT_1'
transicoesID['q_ID_COMMA'].update({'i': 'q_INT_1'})

# Alterar conexões de q_ID_COMMA --> 'f': 'q_FLOAT_1'
transicoesID['q_ID_COMMA'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_ID_COMMA --> 'v': 'q_VOID_1'
transicoesID['q_ID_COMMA'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_ID_COMMA --> 'r': 'q_RETURN_1'
transicoesID['q_ID_COMMA'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_ID_COMMA --> 'e': 'q_ELSE_1'
transicoesID['q_ID_COMMA'].update({'e': 'q_ELSE_1'})

"""
    ID seguido de PLUS
"""

# Acrescentar conexões de q_ID_PLUS --> q_ID_1 com todas as letras do alfabeto
transicoesID['q_ID_PLUS'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_ID_PLUS --> q_NUMERO_1 com todos os numeros
transicoesID['q_ID_PLUS'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_ID_PLUS --> 'i': 'q_INT_1'
transicoesID['q_ID_PLUS'].update({'i': 'q_INT_1'})

# Alterar conexões de q_ID_PLUS --> 'f': 'q_FLOAT_1'
transicoesID['q_ID_PLUS'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_ID_PLUS --> 'v': 'q_VOID_1'
transicoesID['q_ID_PLUS'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_ID_PLUS --> 'r': 'q_RETURN_1'
transicoesID['q_ID_PLUS'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_ID_PLUS --> 'e': 'q_ELSE_1'
transicoesID['q_ID_PLUS'].update({'e': 'q_ELSE_1'})

"""
    ID seguido de MINUS
"""

# Acrescentar conexões de q_ID_MINUS --> q_ID_1 com todas as letras do alfabeto
transicoesID['q_ID_MINUS'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_ID_MINUS --> q_NUMERO_1 com todos os numeros
transicoesID['q_ID_MINUS'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_ID_MINUS --> 'i': 'q_INT_1'
transicoesID['q_ID_MINUS'].update({'i': 'q_INT_1'})

# Alterar conexões de q_ID_MINUS --> 'f': 'q_FLOAT_1'
transicoesID['q_ID_MINUS'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_ID_MINUS --> 'v': 'q_VOID_1'
transicoesID['q_ID_MINUS'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_ID_MINUS --> 'r': 'q_RETURN_1'
transicoesID['q_ID_MINUS'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_ID_MINUS --> 'e': 'q_ELSE_1'
transicoesID['q_ID_MINUS'].update({'e': 'q_ELSE_1'})

"""
    ID seguido de DIVIDE
"""

# Acrescentar conexões de q_ID_DIVIDE --> q_ID_1 com todas as letras do alfabeto
transicoesID['q_ID_DIVIDE'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_ID_DIVIDE --> q_NUMERO_1 com todos os numeros
transicoesID['q_ID_DIVIDE'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_ID_DIVIDE --> 'i': 'q_INT_1'
transicoesID['q_ID_DIVIDE'].update({'i': 'q_INT_1'})

# Alterar conexões de q_ID_DIVIDE --> 'f': 'q_FLOAT_1'
transicoesID['q_ID_DIVIDE'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_ID_DIVIDE --> 'v': 'q_VOID_1'
transicoesID['q_ID_DIVIDE'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_ID_DIVIDE --> 'r': 'q_RETURN_1'
transicoesID['q_ID_DIVIDE'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_ID_DIVIDE --> 'e': 'q_ELSE_1'
transicoesID['q_ID_DIVIDE'].update({'e': 'q_ELSE_1'})

"""
    ID seguido de TIMES
"""

# Acrescentar conexões de q_ID_TIMES --> q_ID_1 com todas as letras do alfabeto
transicoesID['q_ID_TIMES'].update({letter: 'q_ID_1' for letter in alfabeto})

# Acrescentar conexões de q_ID_TIMES --> q_NUMERO_1 com todos os numeros
transicoesID['q_ID_TIMES'].update({number: 'q_NUMERO_1' for number in numeros})

# Alterar conexões de q_ID_TIMES --> 'i': 'q_INT_1'
transicoesID['q_ID_TIMES'].update({'i': 'q_INT_1'})

# Alterar conexões de q_ID_TIMES --> 'f': 'q_FLOAT_1'
transicoesID['q_ID_TIMES'].update({'f': 'q_FLOAT_1'})

# Alterar conexões de q_ID_TIMES --> 'v': 'q_VOID_1'
transicoesID['q_ID_TIMES'].update({'v': 'q_VOID_1'})

# Alterar conexões de q_ID_TIMES --> 'r': 'q_RETURN_1'
transicoesID['q_ID_TIMES'].update({'r': 'q_RETURN_1'})

# Alterar conexões de q_ID_TIMES --> 'e': 'q_ELSE_1'
transicoesID['q_ID_TIMES'].update({'e': 'q_ELSE_1'})

transicoes = combine_transicoes(
    transicoesInit,
    transicoesINT,
    transicoesFLOAT,
    transicoesVOID,
    transicoesRETURN,
    transicoesIF,
    transicoesELSE,
    transicoesLPAREN, 
    transicoesRPAREN,
    transicoesLBRACKETS,
    transicoesRBRACKETS,
    transicoesLBRACES,
    transicoesRBRACES,
    transicoesSEMICOLON,
    transicoesCOMMA,
    transicoesPLUS,
    transicoesMINUS,
    transicoesDIVIDE,
    transicoesTIMES,
    transicoesEQUALS,
    transicoesLESS,
    transicoesGREATER,
    transicoesDIFFERENT,
    transicoesCOMMENT,
    transicoesNUMBER,
    transicoesID
)

#print(transicoes)

# TOKENS

tokens = ['INT','FLOAT','VOID','RETURN','IF','ELSE','LPAREN','RPAREN','LBRACKETS','RBRACKETS','LBRACES','RBRACES','SEMICOLON','COMMA','PLUS','MINUS','DIVIDE','TIMES','ATTRIBUTION','EQUALS','LESS','LESS_EQUAL','GREATER','GREATER_EQUAL','NUMBER','ID']

# SAÍDAS

saidasInit = {'q0':''}

saidasINT = {'q_INT_1':'','q_INT_2':'','q_INT_3':'INT\n'}

saidasFLOAT = {'q_FLOAT_1':'','q_FLOAT_2':'','q_FLOAT_3':'','q_FLOAT_4':'','q_FLOAT_5':'FLOAT\n'}

saidasVOID = {'q_VOID_1':'','q_VOID_2':'','q_VOID_3':'','q_VOID_4':'VOID\n'}

saidasRETURN = {'q_RETURN_1':'','q_RETURN_2':'','q_RETURN_3':'','q_RETURN_4':'','q_RETURN_5':'','q_RETURN_6':'RETURN\n'}

saidasIF = {'q_IF_1':'IF\n'}

saidasELSE = {'q_ELSE_1':'','q_ELSE_2':'','q_ELSE_3':'','q_ELSE_4':'ELSE\n'}

saidasLPAREN = {'q_LPAREN':'LPAREN\n'}

saidasRPAREN = {'q_RPAREN':'RPAREN\n'}

saidasLBRACKETS = {'q_LBRACKETS':'LBRACKETS\n'}

saidasRBRACKETS = {'q_RBRACKETS':'RBRACKETS\n'}

saidasLBRACES = {'q_LBRACES':'LBRACES\n'}

saidasRBRACES = {'q_RBRACES':'RBRACES\n'}

saidasSEMICOLON = {'q_SEMICOLON':'SEMICOLON\n'}

saidasCOMMA = {'q_COMMA':'COMMA\n'}

saidasPLUS = {'q_PLUS':'PLUS\n'}

saidasMINUS = {'q_MINUS':'MINUS\n'}

saidasDIVIDE = {'q_DIVIDE':'DIVIDE\n'}

saidasTIMES = {'q_TIMES':'TIMES\n'}

saidasEQUALS = {'q_ATTRIBUTION_1':'','q_ATTRIBUTION_2':'ATTRIBUTION\n','q_EQUALS_1':'EQUALS\n','q_EQUALS_2':''}

saidasLESS = {'q_LESS_1':'','q_LESS_2':'LESS\n','q_LESS_EQUAL_1':'LESS_EQUAL\n','q_LESS_EQUAL_2':''}

saidasGREATER = {'q_GREATER_1':'','q_GREATER_2':'GREATER\n','q_GREATER_EQUAL_1':'GREATER_EQUAL\n','q_GREATER_EQUAL_2':''}

saidasDIFFERENT = {'q_DIFFERENT_1':'','q_DIFFERENT_2':'DIFFERENT\n'}

saidasCOMMENT = {'q_COMMENT_1':'','q_COMMENT_2':'','q_COMMENT_3':'','q_DIVIDE_SPACE':'DIVIDE\n','q_DIVIDE_LINEBREAK':'DIVIDE\n','q_DIVIDE_LPAREN':'DIVIDE\nLPAREN\n','q_DIVIDE_RPAREN':'DIVIDE\nRPAREN\n','q_DIVIDE_LBRACKETS':'DIVIDE\nLBRACKETS\n','q_DIVIDE_RBRACKETS':'DIVIDE\nRBRACKETS\n','q_DIVIDE_LBRACES':'DIVIDE\nLBRACES\n','q_DIVIDE_RBRACES':'DIVIDE\nRBRACES\n','q_DIVIDE_SEMICOLON':'DIVIDE\nSEMICOLON\n','q_DIVIDE_COMMA':'DIVIDE\nCOMMA\n','q_DIVIDE_PLUS':'DIVIDE\nPLUS\n','q_DIVIDE_MINUS':'DIVIDE\nMINUS\n','q_DIVIDE_DIVIDE':'DIVIDE\nDIVIDE\n','q_DIVIDE_TIMES':'DIVIDE\nTIMES\n','q_DIVIDE_ID':'DIVIDE\nID\n'}

saidasNUMBER = {'q_NUMERO_1':'NUMBER\n','q_NUMERO_2':''}

saidasID = {'q_ID_1':'ID\n','q_ID_2':'','q_ID_SPACE':'ID\n','q_ID_LINEBREAK':'ID\n','q_ID_LPAREN':'ID\nLPAREN\n','q_ID_RPAREN':'ID\nRPAREN\n','q_ID_LBRACKETS':'ID\nLBRACKETS\n','q_ID_RBRACKETS':'ID\nRBRACKETS\n','q_ID_LBRACES':'ID\nLBRACES\n','q_ID_RBRACES':'ID\nRBRACES\n','q_ID_SEMICOLON':'ID\nSEMICOLON\n','q_ID_COMMA':'ID\nCOMMA\n','q_ID_PLUS':'ID\nPLUS\n','q_ID_MINUS':'ID\nMINUS\n','q_ID_DIVIDE':'ID\nDIVIDE\n','q_ID_TIMES':'ID\nTIMES\n'}

saidas = saidasInit.copy()
saidas.update(saidasINT)
saidas.update(saidasFLOAT)
saidas.update(saidasVOID)
saidas.update(saidasRETURN)
saidas.update(saidasIF)
saidas.update(saidasELSE)
saidas.update(saidasLPAREN)
saidas.update(saidasLBRACKETS)
saidas.update(saidasRBRACKETS)
saidas.update(saidasRPAREN)
saidas.update(saidasLBRACES)
saidas.update(saidasRBRACES)
saidas.update(saidasSEMICOLON)
saidas.update(saidasCOMMA)
saidas.update(saidasPLUS)
saidas.update(saidasMINUS)
saidas.update(saidasDIVIDE)
saidas.update(saidasTIMES)
saidas.update(saidasEQUALS)
saidas.update(saidasLESS)
saidas.update(saidasGREATER)
saidas.update(saidasDIFFERENT)
saidas.update(saidasCOMMENT)
saidas.update(saidasNUMBER)
saidas.update(saidasID)

# MOORE MACHINE

moore = Moore(estados,
              fullList,
              tokens,
              transicoes,
              'q0',
              saidas
              )

def moore_to_jflap(estados, alfabeto, tokens, transicoes, initial_estado, saidas, saida_file):
    # Substitui '\n' por ' ' nos saidas sem modificar o dicionário original
    sanitized_saidas = {estado: saidas.get(estado, '').replace('\n', ' ') for estado in estados}

    # Cria a estrutura XML
    structure = ET.Element('structure')
    automaton_type = ET.SubElement(structure, 'type')
    automaton_type.text = 'moore'
    automaton = ET.SubElement(structure, 'automaton')

    # Mapeia os estados --> IDs
    estado_map = {estado: str(i) for i, estado in enumerate(estados)}

    # Adiciona os estados ao XML
    for estado in estados:
        estado_element = ET.SubElement(automaton, 'estado', id=estado_map[estado], name=estado)
        
        # Define posições X e Y fictícias
        x = ET.SubElement(estado_element, 'x')
        y = ET.SubElement(estado_element, 'y')
        x.text = str(100 + 150 * (int(estado_map[estado]) % 10))  # Posição X
        y.text = str(100 + 150 * (int(estado_map[estado]) // 10))  # Posição Y

        # Marca o estado inicial
        if estado == initial_estado:
            ET.SubElement(estado_element, 'initial')

        # Adiciona a saída do estado
        saida = ET.SubElement(estado_element, 'saida')
        saida.text = sanitized_saidas[estado]  # Garante que nunca será None

    # Adiciona as transições ao XML
    for from_estado, edges in transicoes.items():
        if from_estado not in estado_map:
            print(f"Erro: Estado de origem '{from_estado}' não encontrado em 'estados'.")
            return  # Interrompe --> evitar inconsistência no XML

        for symbol, to_estado in edges.items():
            if to_estado not in estado_map:
                print(f"Erro: Estado de destino '{to_estado}' não encontrado em 'estados'.")
                return  # Interrompe --> evitar inconsistência no XML

            transition = ET.SubElement(automaton, 'transition')
            from_element = ET.SubElement(transition, 'from')
            to_element = ET.SubElement(transition, 'to')
            read = ET.SubElement(transition, 'read')
            transout = ET.SubElement(transition, 'transout')

            from_element.text = estado_map[from_estado]
            to_element.text = estado_map[to_estado]
            read.text = symbol

            # Adiciona a saída associado ao estado de destino
            transout.text = sanitized_saidas[to_estado]

    # Escreve o XML no arquivo
    try:
        tree = ET.ElementTree(structure)
        tree.write(saida_file, encoding='utf-8', xml_declaration=True)
        #print(f"Arquivo '{saida_file}' gerado com sucesso!")
    except Exception as e:
        print(f"Erro ao gerar o arquivo XML: {e}")

def main():
    check_cm = False
    check_key = False

    if(len(sys.argv) < 2):
        raise TypeError(error_handler.newError(check_key, 'ERR-LEX-USE'))
    
    for idx, arg in enumerate(sys.argv):
        aux = arg.split('.')
        if aux[-1] == 'cm':
            check_cm = True
            idx_cm = idx
        if(arg == "-k"):
            check_key = True
    
    if check_key and len(sys.argv) < 3:
        raise TypeError(error_handler.newError(check_key, 'ERR-LEX-USE'))
    elif not check_cm:
      raise IOError(error_handler.newError(check_key, 'ERR-LEX-NOT-CM'))
    elif not os.path.exists(sys.argv[idx_cm]):
        raise IOError(error_handler.newError(check_key, 'ERR-LEX-FILE-NOT-EXISTS'))
    else:
        data = open(sys.argv[idx_cm])
        source_file = data.read()

        try:
            if not check_key:
                print("Definição da Máquina:")
                print(moore)
                print("Entrada:")
                print(source_file)
                print("Lista de Tokens:")
            print(moore.get_output_from_string(source_file).rstrip('\n'))
            moore_to_jflap(estados, fullList, tokens, transicoes, 'q0', saidas, 'jflap/moore_machine.jff')
            
        except Exception as e:
            error_msg = str(e)
            for i, char in enumerate(source_file):
                try:
                    moore.get_output_from_string(source_file[:i+1])
                except Exception:
                    error_index = i
                    break
            else:
                error_index = None
            if error_index is not None:
                line = source_file[:error_index].count('\n') + 1
                last_newline = source_file[:error_index].rfind('\n')
                column = (error_index - last_newline) if last_newline != -1 else error_index + 1
                raise IOError(error_handler.newError(check_key, 'ERR-LEX-INV-CHAR', line, column, valor=e))
            else:
                line, column = "Desconhecido", "Desconhecido"

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    except (ValueError, TypeError):
        print(e)