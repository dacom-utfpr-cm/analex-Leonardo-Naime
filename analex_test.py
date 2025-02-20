import pytest
import subprocess
import shlex
import os, fnmatch

import analex

# Lista de casos de teste com arquivos e argumentos
test_cases = [("", "-k"), ("teste.c", "-k"), ("notexists.cm", "-k")]

# Adiciona arquivos cm encontrados no diretório 'tests'
for file in fnmatch.filter(os.listdir('tests'), '*.cm'):
    test_cases.append((file, "-k"))

@pytest.mark.parametrize("input_file, args", test_cases)
def test_execute(input_file, args):
    if(input_file != ''):
        path_file = 'tests/' + input_file
    else:
        path_file = ""
    
    # Executa o comando com subprocess
    cmd = "python3 analex.py {0} {1}".format(args, path_file)
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    stdout, stderr = process.communicate()

    # Captura apenas a parte relevante da saída (os tokens ou mensagens de erro)
    output_lines = stdout.decode("utf-8").strip().split("\r\n")
    generated_output = "\n".join(output_lines)  # Certifique-se de juntar as linhas corretamente

    # Agora lê o arquivo de saída esperado
    path_file = 'tests/' + input_file
    expected_output_file = path_file + ".lex.out"

    # Verifica se o arquivo de saída esperado existe, caso contrário, ajusta o fluxo de comparação
    if os.path.exists(expected_output_file):
        with open(expected_output_file, "r") as output_file:
            expected_output = output_file.read().strip()
    else:
        # Caso o arquivo de saída esperado não exista, a saída esperada será o erro
        expected_output = stderr.decode("utf-8").strip()

    # Impressão para debug
    print("Generated output:")
    print(generated_output)
    print("Expected output:")
    print(expected_output)

    # Comparar a saída gerada com a esperada (token ou erro)
    assert generated_output == expected_output