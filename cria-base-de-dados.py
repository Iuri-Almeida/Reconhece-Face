# Projeto Reconhecimento de Face - Python, OpenCV, DLib e Face Recognition
# Autor: Iuri Lopes Almeida
# Perfil GitHub: https://github.com/Iuri-Almeida
# Data: 01/06/2020
# Descrição: Esse programa foi escrito na linguagem Python e usa as bibliotecas
#            OpenCV, DLib e Face Recognition como base. Ele faz a criação da base
# 			 de dados necessária para o reconhecimento. Aqui é criado um arquivo
# 			 que contém os detalhes da face de quem deseja reconhecer e esse
# 			 arquivo será usado pelo programa reconhece-face.py (está no mesmo projeto)
# 			 para fazer o reconhecimento em imagens/vídeo. Após isso, o usuário
# 			 pode acessar o programa pela linha de comando (terminal), passando
# 			 o caminho para o vídeo de onde deseja tirar as informações da face,
# 			 o nome da pasta onde deseja salvar as imagens e o nome da pessoa que
# 			 deseja que o programa se refira quando identificar aquela face.
# Forma de uso: python cria-base-de-dados.py -v [VIDEO] -p [PASTA] -n [NOME]


# Importações necessárias.
import cv2, dlib, imutils, face_recognition, pickle, argparse, os


''' Definindo alguns parâmetros para serem passados pela linha de comando '''

# Define uma descrição sobre o que o programa faz.
parser = argparse.ArgumentParser(description='Faz a criação de uma base de dados para reconhecimento facial.')

# Define uma 'flag' para poder passar o vídeo. Caso não seja passado nenhum
# caminnho para o vídeo, o programa irá entender que é para usar a webcam.
# Ex.: python cria-base-de-dados.py -v videos/video.mp4
parser.add_argument('-v', dest='video', default=0, help='caminho para o vídeo que servirá de base')

# Define uma 'flag' para poder passar o nome da pasta onde será salvo todas as imagens.
# Ex.: python cria-base-de-dados.py -p pasta
parser.add_argument('-p', dest='pasta', required=True, help='nome da pasta na qual deseja salvar todas as imagens')

# Define uma 'flag' para poder passar o nome que será usado para identificar a pessoa.
# Ex.: python cria-base-de-dados.py -n João
parser.add_argument('-n', dest='nome', required=True, help='nome que será usado para identificar a pessoa')

# Define uma váriavel que vai poder ser chamada para ter acesso aos dados que foram
# passados pela linha de comando (terminal).
args = parser.parse_args()


# Função responsável por fazer a criação da base de dados para reconhecimento.
def cria_Base_De_Dados():

	# Inicia o vídeo.
	# Obs.: Se for passado o parâmetro '0' para a função VideoCapture(0), o
	# 		OpenCV irá entender que é para abrir o vídeo pela webcam.
	captura = cv2.VideoCapture(args.video)

	# landmarks = "cnn/shape_predictor_68_face_landmarks.dat"

	# Função reponsável por varrer toda a imagem procurando em que local dela
	# tem uma face.
	detector = dlib.get_frontal_face_detector()

	# predictor = dlib.shape_predictor(landmarks)

	# Contador de frames.
	numero_Frame = 0

	# Array responsável por armazenar toda a codificação do rosto da pessoa.
	detalhes_Cod_Faces = []

	# Array responsável por armazenar o nome da pessoa.
	# Obs.: É preciso esse array para podermos dizer que cada codificação no
	# 		array detalhes_Cod_Faces está relacionada a um nome (nome da pessoa).
	nome_Cod_Faces = []

	# Loop infinito, até acabar o vídeo ou seja interrompido.
	# Obs.: Cada loop do while é um frame do vídeo.
	while True:
		
		# frame -> recebe todo o frame do vídeo.
		# Função read() é responsável por fazer a leitura de todo frame.
		_, frame = captura.read()

		# Se frame for vazio, ou seja, não tiver frame, pare o loop.
		if frame is None:
			break

		# Responsável por redimensionar o frame.
		frame = imutils.resize(frame, width=500)

		# Aqui é onde a função get_frontal_face_detector() entra em ação. Ela
		# varre todo o frame buscando por uma face e armazena informações como
		# o retângulo onde encontrou a face e a numeração para cada face encontrada.
		# O parâmetro '1' representa a quantidade de zoom que o programa vai dar
		# para procurar por um rosto (caso o rosto esteja bem pequeno). Esse
		# parâmetro afeda diretamente no processamento, ou seja, quanto maior
		# o valor mais demorado, no entanto, mais precisão.
		faces = detector(frame, 1)

		# Se o tamanho de faces for igual a 0, ou seja, se não for encontrada
		# nenhuma face no frame, vá para o próximo frame. Para evitar que codifique
		# imagens que não tem o rosto da pessoa.
		if len(faces) == 0:
			continue

		# k -> número de identificação de cada face.
		# retangulo -> retângulo onde a face se encontra.
		# Função enumerate() é responsável por enumerar cada face com seu
		# respectivo número de identificação.
		for k, retangulo in enumerate(faces):

			# shape = predictor(frame, retangulo)

			# Diferente da função detectMultiScale() da biblioteca OpenCV,
			# a função get_frontal_face_detector() não retorna os vértices
			# do retângulo onde está a face. Por isso é preciso fazer esses
			# passos para recuperar o exato local dos vértices.
			x = retangulo.left()
			y = retangulo.top()
			l = retangulo.right() - x
			a = retangulo.bottom() - y

			# Organização das coordenadas.
			inicio_X = x
			inicio_Y = y
			fim_X = x + l
			fim_Y = y + a
			cor = (0, 0, 255)
			grossura_Linha = 2

			# Responsável por desenhar o retângulo na tela para que possamos ver.
			cv2.rectangle(frame, (inicio_X, inicio_Y), (fim_X, fim_Y), cor, grossura_Linha)

		# Se não existir uma pasta com o nome que o usuário definiu dentro da pasta
		# imagens, crie.
		if (os.path.exists("imagens/" + str(args.pasta)) == False):
			os.mkdir("imagens/" + str(args.pasta))

		# Salve cada frame na pasta que o usuário escolheu.
		cv2.imwrite("imagens/" + str(args.pasta) + "/" + str(numero_Frame) + ".jpg", frame)

		print("imagens/" + str(args.pasta) + "/" + str(numero_Frame) + ".jpg")

		# Converta a cor do frame de BGR (padrão do OpenCV) para RGB.
		frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		# Função responsável por fazer a localização da face no frame. É usado
		# para auxiliar na próxima função, que fará a codificação de cada detalhe
		# da face.
		# Obs.: O modelo (model) pode ser 'cnn' (Rede Neural Convolutiva) ou 'hog'
		# 		(Histograma de Gradientes Orientados). O 'cnn' é mais demorado,
		# 		porém com maior precisão e o 'hog' é mais rápido, porém com menor
		# 		precisão.
		caixas_Face = face_recognition.face_locations(frame_RGB, model="cnn")

		# Função responsável por fazer a codificação de cada detalhe da face detectada.
		codificando_Faces = face_recognition.face_encodings(frame_RGB, caixas_Face)

		# Para cada detalhe dentro de todos os detalhes da face, faça:
		for cod in codificando_Faces:

			# Coloque cada detalhe dentro do array responsável por armazenar as
			# codifiações de cada face.
			detalhes_Cod_Faces.append(cod)

			# Coloque o nome da pessoa dentro do array responsável por armazenar
			# o nome da pessoa. A ideia é que cada detalhe da face tenha um identificador
			# dizendo que aquele detalhe é de determinada pessoa.
			nome_Cod_Faces.append(str(args.nome))

		# Contagem do número de frames.
		numero_Frame += 1

		# Responsável por mostrar cada frame na tela.
		cv2.imshow("Teste", frame)

		# Responsável por ficar esperando para ver se alguma tecla vai ser pressionada.
		key = cv2.waitKey(1) & 0xFF

		# Se a tecla 'q' for precionada, para o loop.
		if key == ord('q'):
			break

	# Crie um dicíonário que terá como valor todos os detalhes da face
	# e cada um desse está relacionado ao nome da pessoa.
	data = {"codificações": detalhes_Cod_Faces, "nomes": nome_Cod_Faces}

	# Crie um arquivo dentro da pasta 'faces-codificadas' para armazenar as codificações.
	# Obs.: 'wb' significa que será um arquivo que vamos escrever ('w' -> write) e na
	# 		forma de binário ('b').
	arquivo = open("faces-codificadas/" + str(args.nome) + ".cod", "wb")

	# Escreva nesse arquivo o dicionário que contém as codificações da face.
	# Obs.: O 'pickle' é uma forma de escrita para poder criar um arquivo parecido com
	# 		o .xml, por exemplo.
	arquivo.write(pickle.dumps(data))

	# Feche esse arquivo.
	arquivo.close()

	# Libere a captura do vídeo.
	captura.release()

	# Feche todas as janelas abertas.
	cv2.destroyAllWindows()


# Função principal, responsável por chamar todas as outras funções.
def main():

	# Chamando a função que fará a criação da base de dados.
	cria_Base_De_Dados()


if __name__ == "__main__":
	main()