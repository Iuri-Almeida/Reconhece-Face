# Projeto Reconhecimento de Face - Python, OpenCV e Face Recognition
# Autor: Iuri Lopes Almeida
# Perfil GitHub: https://github.com/Iuri-Almeida
# Data: 01/06/2020
# Descrição: Esse programa foi escrito na linguagem Python e usa as bibliotecas
#            OpenCV e Face Recognition como base. Ele faz o reconheciento de faces
#            em vídeo ou imagem, no entanto, para poder fazer esse reconhecimento é
#            preciso que o usuário já tenha uma base de dados pronta e salva na pasta
#            faces-codificadas com a extensão .cod. Tudo isso pode ser criado a partir
#            do programa cria-base-de-dados.py no mesmo projeto. Após isso, o usuário
#            pode acessar o programa todo pela linha de comando (terminal), passando
#            o caminho para imagens ou vídeos que deseja fazer o reconhecimento.
# Formas de uso: python reconhece-face.py -v [VIDEO]
#                python reconhece-face.py -i [IMAGEM]


# Importações necessárias.
import face_recognition, pickle, cv2, glob, os, imutils, argparse


''' Definindo alguns parâmetros para serem passados pela linha de comando '''

# Define uma descrição sobre o que o programa faz.
parser = argparse.ArgumentParser(description='Faz o reconhecimento de faces.')

# Define uma 'flag' para poder acessar o vídeo. Caso não seja passado nenhum
# caminnho para o vídeo, o programa irá entender que é para usar a webcam.
# Ex.: python cria-base-de-dados.py -v videos/video.mp4
parser.add_argument('-v', dest='video', default=0, help='caminho para o vídeo que servirá de base')

# Define uma 'flag' para poder acessar a imagem. Caso não seja passado nenhum
# caminho para a imagem, o programa irá entender que não é para usar.
# Ex.: python cria-base-de-dados.py -i imagens/1.jpg
parser.add_argument('-i', dest='imagem', default=None, help='caminho para a imagem que servirá de base')

# Define uma váriavel que vai poder ser chamada para ter acesso aos dados que foram
# passados pela linha de comando (terminal).
args = parser.parse_args()


# Função resposável por fazer o reconhecimento.
# frame_ou_imagem -> é o frame (vídeo) ou imagem (foto) que será feito o reconhecimento.
# Obs.: Essa função está aqui para não haver muita repetição de código, porque a única
#       diferença, nesse caso, para imagem e vídeo é como vai ser dada a entrada do frame
#       ou da imagem.
# Obs.: Para fazer o reconhecimento, o programa escolhe a pessoa que tiver a face
#       mais próxima da face identificada.
def faz_O_Trabalho(frame_ou_imagem):

    # Converta a cor do frame_ou_imagem de BGR (padrão do OpenCV) para RGB.
    frame_ou_imagem_RGB = cv2.cvtColor(frame_ou_imagem, cv2.COLOR_BGR2RGB)

    # Função responsável por fazer a localização da face no frame_ou_imagem. É usado
    # para auxiliar na próxima função, que fará a codificação de cada detalhe
    # da face.
    # Obs.: O modelo (model) pode ser 'cnn' (Rede Neural Convolutiva) ou 'hog'
    #       (Histograma de Gradientes Orientados). O 'cnn' é mais demorado,
    #       porém com maior precisão e o 'hog' é mais rápido, porém com menor
    #       precisão.
    caixas_Face = face_recognition.face_locations(frame_ou_imagem_RGB, model='cnn')

    # Função responsável por fazer a codificação de cada detalhe da face detectada.
    codificando_Faces = face_recognition.face_encodings(frame_ou_imagem_RGB, caixas_Face)
        
    # Dicionário que será responsável por armazenar todas as codificações das
    # faces que já foram treinadas, ou seja, que possuem um arquivo .cod na pasta
    # faces-codificadas. 
    codificacoes_Treinadas = {}

    # Contagem de pessoas, número de arquivos .cod, ou seja, número de pessoas conhecidas.
    contagem_Pessoas = 0

    # Para cada arquivo com extensão .cod dentro da pasta faces-codificadas, faça:
    for arquivo in glob.glob("faces-codificadas/*.cod"):

        # Aqui vai ocorrer o processo contrário ao da criação da base de dados.
        # Vamos pegar o arquivo codificado, que contém detalhes da face da pessoa).
        # Vamos abrir, ler e carregar esse arquivo, ou seja, vamos retomar a forma
        # original do arquivo, como o dicionário que tem cada detalhe do rosto
        # identificado por um nome (nome da pessoa).
        codificacoes_Treinadas[contagem_Pessoas] = pickle.loads(open(arquivo, "rb").read())

        # Para cada interação, ou seja, para cada arquivo .cod lido é porque conhece
        # +1 pessoa.
        contagem_Pessoas += 1

    # Define uma lista que irá conter os nomes das pessoas reconhecidas.
    nomes = []

    # O nome de início será desconhecido, ou seja, caso não seja reconhecida nenhuma
    # face, será identificado como desconhecido.
    nome = "Desconhecido"

    # Para cada face desconhecida que foi encontrada no frame_ou_imagem e codificada com a função
    # face_encodings(), faça:
    # Obs.: Esse for é porque pode haver mais de uma face no frame_ou_imagem.
    for face_Desconhecida_Codificada in codificando_Faces:

        # Para cada id das pessoas conhecidas, faça:
        # Obs.: O id_Pessoa é a ordem que foram armazenadas as codificações das pessoas
        #       que são conhecidas pelo programa.
        for id_Pessoa in range(0, contagem_Pessoas):

            # Função reponsável por fazer a comparação das faces identificadas e as
            # faces que já são conhecidas.
            comparacao_Face = face_recognition.compare_faces(codificacoes_Treinadas[id_Pessoa]['codificações'], face_Desconhecida_Codificada) # , 0.6

            # Se a comparação das faces retornar True, ou seja, a face se aproxima
            # a uma das faces que já se conhece, faça:
            if True in comparacao_Face:

                # Função responsável por enumerar cada detalhe das faces detecatadas
                # que são parecidas com as faces já conhecidas.
                detalhes_Faces_Desconhecidas = [i for (i, b) in enumerate(comparacao_Face) if b]
                counts = {}

                # Para cada detalhe dentro dos detalhes das faces desconhecidas, faça:
                for detalhe in detalhes_Faces_Desconhecidas:

                    # Vai comparar cada detalhe com todos os detalhes de todas as
                    # codificações das faces que foram treinadas, para que no final
                    # seja escolhida o nome da face que mais teve comparações positivas,
                    # ou seja, para escolher o nome que mais se aproxima.
                    nome = codificacoes_Treinadas[id_Pessoa]["nomes"][detalhe]
                    counts[nome] = counts.get(nome, 0) + 1

                # Nome recebe o nome que mais se aproxima a face identificada.
                nome = max(counts, key=counts.get)

        # Armazena esse nome que mais se aproxima a face identificada.
        nomes.append(nome)

    # Para todas as coordenadas dos vértices do retângulo que contém a face e
    # para todos os nomes dentro de nomes, faça:
    for ((inicio_Y, fim_X, fim_Y, inicio_X), nome) in zip(caixas_Face, nomes):

        # Desenhe um retângulo em volta da face que foi identificada.
        cv2.rectangle(frame_ou_imagem, (inicio_X, inicio_Y), (fim_X, fim_Y), (0, 255, 0), 2)

        # Escreva na tela o nome da pessoa identificada acima da face.
        cv2.putText(frame_ou_imagem, nome, (inicio_X, inicio_Y), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 2)

    # Escreva na tela a quantidade de pessoas que tem na imagem/vídeo.
    cv2.putText(frame_ou_imagem, "Pessoa(s): {}".format(len(nomes)), (5, 15), cv2.FONT_ITALIC, 0.5, (0, 0, 255), 2)

    # Escreva na tela a quantidade de pessoas que não foram reconhecidas na imagem/vídeo.
    cv2.putText(frame_ou_imagem, "Desconhecido(s): {}".format(nomes.count("Desconhecido")), (5, 30), cv2.FONT_ITALIC, 0.5, (0, 0, 255), 2)

    # Enquanto a string "Desconhecido" estiver na lista nomes, faça:
    # Obs.: Está fazendo isso para poder fazer a contagem de pessoas que foram reconhecidas.
    while "Desconhecido" in nomes:

        # Remova a string "Desconhecido"
        nomes.remove("Desconhecido")

    # Escreva na tela a quantidade de pessoas que foram reconhecidas na imagem/vídeo.
    cv2.putText(frame_ou_imagem, "Reconhecido(s): {}".format(len(nomes)), (5, 45), cv2.FONT_ITALIC, 0.5, (0, 0, 255), 2)

    # Retorne a lista com os nomes das faces que foram reconhecidas, o/a frame/imagem
    # e o local onde foi localizado as faces.
    return nomes, frame_ou_imagem, caixas_Face


# Função usada para fazer o reconhecimento da face em fotos.
def reconhece_Face_Foto():

    # Responsável por ler a imagem.
    imagem = cv2.imread(args.imagem)

    # Responsável por redimensionar a imagem. 
    imagem = imutils.resize(imagem, width=700)

    # Chamando a função que fará todo o trabalho do reconhecimento da face.
    nomes, imagem, caixas_Face = faz_O_Trabalho(imagem)

    cv2.imwrite("11.jpg", imagem)

    # Responsável por mostrar na tela.
    cv2.imshow("Imagem", imagem)

    # Responsável por esperar e identificar caso uma tecla for pressionada.
    cv2.waitKey(0) & 0xFF

    # Responsável por fechar todas as janelas que forem abertas.
    cv2.destroyAllWindows()


# Função usada para fazer o reconheceimento da face em vídeos.
def reconhece_Face_Video():

    # Inicia o vídeo.
    # Obs.: Se for passado o parâmetro '0' para a função VideoCapture(0), o
    #       OpenCV irá entender que é para abrir o vídeo pela webcam.
    captura = cv2.VideoCapture(args.video)

    # Loop infinito, até acabar o vídeo ou seja interrompido.
    # Obs.: Cada loop do while é um frame do vídeo.
    while(True):

        # frame -> recebe todo o frame do vídeo.
        # Função read() é responsável por fazer a leitura de todo frame.
        _, frame = captura.read()

        # Se frame for vazio, ou seja, não tiver frame, pare o loop.
        if frame is None:
            break

        # Responsável por redimensionar o frame.
        frame = imutils.resize(frame, width=200)

        # Chamando a função que fará todo o trabalho do reconhecimento da face.
        nomes, frame, caixas_Face = faz_O_Trabalho(frame)

        # Responsável por mostrar na tela.
        cv2.imshow("Video", frame)

        # Responsável por esperar e identificar caso uma tecla for pressionada.
        key = cv2.waitKey(1) & 0xFF

        # Se a tecla 'q' for pressionada, termine o loop.
        if key == ord('q'):
            break

    # Responsável por liberar a captura do vídeo.
    captura.release()

    # Responsável por fechar todas as janelas que forem abertas.
    cv2.destroyAllWindows()


# Função principal, responsável por chamar todas as outras funções.
def main():

    # Se o caminho para a imagem não for vazio, ou seja, tenha caminho para a imagem, faça:
    if args.imagem is not None:

        # Chamando a função para fazer o reconhecimento em foto.
        reconhece_Face_Foto()

    # Caso contrário, ou seja, tenha escolhido usar o vídeo, faça:
    else:

        # Chamando a função para fazer o reconhecimento em vídeo.
        reconhece_Face_Video()


if __name__ == "__main__":
    main()
