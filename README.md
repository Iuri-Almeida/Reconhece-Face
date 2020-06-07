# Reconhece Face

Programa que faz o reconhecimento de faces.

# Descrição

* Cria Base de Dados

Esse programa foi escrito na linguagem Python e usa as bibliotecas <a href="https://opencv.org/">OpenCV</a>, <a href="http://dlib.net/">DLib</a> e <a href="https://pypi.org/project/face-recognition/">Face Recognition</a> como base. Ele faz a criação da base de dados necessária para o reconhecimento. Aqui é criado um arquivo que contém os detalhes da face de quem deseja reconhecer e esse arquivo será usado pelo programa <b>reconhece-face.py</b> (está no mesmo projeto) para fazer o reconhecimento em imagens/vídeo. Após isso, o usuário pode acessar o programa pela linha de comando (terminal), passando o caminho para o vídeo de onde deseja tirar as informações da face, o nome da pasta onde deseja salvar as imagens e o nome da pessoa que deseja que o programa se refira quando identificar aquela face.

* Reconhece Face

Esse programa foi escrito na linguagem Python e usa as bibliotecas <a href="https://opencv.org/">OpenCV</a>, <a href="http://dlib.net/">DLib</a> e <a href="https://pypi.org/project/face-recognition/">Face Recognition</a> como base. Ele faz o reconheciento de faces em vídeo ou imagem, no entanto, para poder fazer esse reconhecimento é preciso que o usuário já tenha uma base de dados pronta e salva na pasta faces-codificadas com a extensão .cod. Tudo isso pode ser criado a partir do programa cria-base-de-dados.py no mesmo projeto. Após isso, o usuário pode acessar o programa todo pela linha de comando (terminal), passando o caminho para imagens ou vídeos que deseja fazer o reconhecimento.

# Como funciona?

O programa primeiro precisa criar uma base de dados (<b>cria-base-de-dados.py</b>) para que depois possa se basear no arquivo criado para fazer o reconhecimento de determinada face (<b>reconhece-face.py</b>). Para o reconhecimento, o programa reconhece a face baseado na face que mais se aproximou, dentre os arquivos que estão na base de dados, a face identificada.

# Instalação

É preciso ter o Python instalado no seu computador (<a href="https://www.python.org/downloads/">Python</a>, recomendado baixar a última versão). Para importar algumas funções usadas nesse projeto é preciso fazer a instalação de algumas bibliotecas, são elas:

* opencv-python - Forma de instalação: <b>pip install opencv-python</b>
* imutils - Forma de instalação: <b>pip install imutils</b>
* dlib - Forma de instalação: <b>pip install dlib</b>
* face-recognition - Forma de instalação: <b>pip install face-recognition</b>

<b>Obs.:</b> Essas instalações podem ser feitas pelo terminal do seu computador (necessário que já tenha o python instalado) ou pelo <a href="https://www.jetbrains.com/pt-br/pycharm/download/">PyCharm</a>, se preferir.

# Uso

Após as instalações, para começar a usar é preciso clonar esse repositório e seguir alguns parâmetros que serão passados pela linha de comando (terminal), são eles:

* Cria Base de Dados

É preciso passar o caminho para o vídeo (-v) de onde serão retiradas as informações sobre a face da pessoa que deseja armazenar para depois reconhecer, caso o caminho do vídeo não seja passado, o programa irá fazer uso da webcam para capturar as informações. Também é necessário passar o nome da pasta (-p) onde serão armazenadas as imagens que forem geradas e o nome da pessoa (-n) que o usuário deseja que o programa identifique aquela face.

<b>Ex.:</b> <i>python cria-base-de-dados.py -v videos/video.mp4 -p joao -n João</i>. Aqui o programa cria uma base de dados baseada no video <i>video.mp4</i>, armazena as imagens na pasta <i>joao</i> e identifica a face que tiver no vídeo como <i>João</i>.

* Reconhece Face

É preciso passar o caminho para o vídeo (-v) de onde serão retiradas as informações sobre a face da pessoa que deseja reconhecer, caso o caminho do vídeo não seja passado, o programa irá fazer uso da webcam para capturar as informações. Caso o usuário queira fazer o reconhecimento em uma imagem, é necessário passar o caminho para a imagem (-i). Enquanto não for passado uma imagem o programa irá sempre fazer uso do vídeo.

<b>Ex. 1:</b> <i>python reconhece-face.py</i>. Aqui o programa fará o uso da webcam para fazer o reconhecimento.

<b>Ex. 2:</b> <i>python reconhece-face.py -v videos/video.mp4</i>. Aqui o programa fará uso do vídeo <i>video.mp4</i> para fazer o reconhecimento.

<b>Ex. 3:</b> <i>python reconhece-face.py -i imagens/1.jpg</i>. Aqui o programa fará uso da imagem <i>1.jpg</i> para fazer o reconhecimento.

# Exemplos

* Reconhecendo o rosto do Willian Bonner.

![12](https://user-images.githubusercontent.com/60857927/83982109-27213700-a8fa-11ea-8540-0a6b5cee0c29.jpg)

# Referências

* <a href="https://www.youtube.com/channel/UCEn6kONg6EC_Ylh0RlInsMw">Canal YouTube - Universo Discreto</a>
* <a href="https://universodiscreto.com/">Blog - Universo Discreto</a>