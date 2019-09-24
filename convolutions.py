import argparse
import pdb
import time
import cv2
import numpy as np
from skimage.exposure import rescale_intensity

# método de convulsão
def convolve(image, kernel):
	# dimensões espaciais da imagem, e do kernel
	# retorna a altura e largura da imagem em matriz
	(iH, iW) = image.shape[:2]
	(kH, kW) = kernel.shape[:2]

		# alocar memória para a imagem de saída, tendo o cuidado de
		# "acoplar" as bordas da imagem de entrada para que o espaço
		# tamanho (ou seja, largura e altura) não sejam reduzidos
		# replicando os pixels para que a img de saída tenha o mesmo tamanho
	pad = (kW - 1) // 2
	image = cv2.copyMakeBorder(image, pad, pad, pad, pad,
		cv2.BORDER_REPLICATE)
	output = np.zeros((iH, iW), dtype="float32")

		# faça um loop sobre a imagem de entrada, "deslizando" o kernel
		# cada (x, y) - coordena da esquerda para a direita e de cima para
		# inferior
	for y in np.arange(pad, iH + pad):
		for x in np.arange(pad, iW + pad):
			# extrai a area de interesse da imagem ROI, pegando o
			# *centro* das coordenadas (x, y)atuais
			roi = image[y - pad:y + pad + 1, x - pad:x + pad + 1]

						#cálculo para convolução
			k = (roi * kernel).sum()
			#print(k)
						#armazena o valor envolvido na saída (x, y) -
						#coordenada da imagem de saída
			output[y - pad, x - pad] = k
			

		# redimensionar a imagem de saída para estar no intervalo [0, 255]
	output = rescale_intensity(output, in_range=(0, 255))
	output = (output * 255).astype("uint8")

	# return a imagem de sáida
	#print(np.median(output), sep = "\n")
	
	return output

i = 1

while i > 0:
	'''
	# argumento de imagem
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True,
		help="path to the input image")
	args = vars(ap.parse_args())
	'''

	# kernels
	gabor = cv2.getGaborKernel((21,21), 5, 1, 10, 1, 0, cv2.CV_32F)
	mauricio = cv2.getGaborKernel((21,21), 15, 1, 10, 1, 0, cv2.CV_32F)
	marcelo = cv2.getGaborKernel((21,21), 25, 2, 20, 1, 0, cv2.CV_32F)
	tamires = cv2.getGaborKernel((21,21), 35, 2, 15, 1, 0, cv2.CV_32F)
	ricardo = cv2.getGaborKernel((21,21), 8, 1, 4, 3, 0, cv2.CV_32F)
	gilmar = cv2.getGaborKernel((21,21), 3, 3, 6, 3, 0, cv2.CV_32F)

	# construir o banco de kernel, uma lista de kernels que vamos
	# aplicar usando a função `convole` e a Função filter2D do OpenCV

	kernelBank = (
        ("maricio", mauricio),
        ("ricardo", ricardo),
        ("tamires", tamires),
        ("marcelo", marcelo),
        ("gilmar", gilmar)        
	)      

	# carrega a imagem de entrada e convert para escala de cinza.
	'''
	imagens:
	150x300.jpg; 300x175.jpg; 600x350.jpg; 800x476.jpg; 1200x1200.jpg; 
	'''

	image = cv2.imread('img/150x300.jpg')
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	line = 1

	for (kernelName, kernel) in kernelBank:
		try:
			# aplicando função convolve
			tempoInicial = time.time()

			convoleOutput = convolve(gray, kernel)

			tempoFinal = time.time()
			tempoExecucao = str(tempoFinal - tempoInicial)

			conteudoAux = str(line) + ' ' + tempoExecucao

			#Criação de Arquivo com os Tempos
			'''
			Arquivos de tempo:
			150x300.txt; 300x175.txt; 600x350.txt; 800x476.txt; 1200x1200.txt;
			'''
			arquivo = open('tempExec/150x300.txt', 'r') # Abra o arquivo (leitura)
			conteudo = arquivo.readlines()
			if not conteudo:
				arquivo = open('tempExec/150x300.txt', 'w') # Abre novamente o arquivo (escrita)
				arquivo.writelines(conteudoAux)    # escreva o conteúdo criado anteriormente nele.
				arquivo.close()
			else:
				conteudo.append("\n")
				conteudo.append(conteudoAux)
				arquivo = open('tempExec/150x300.txt', 'w') # Abre novamente o arquivo (escrita)
				arquivo.writelines(conteudo)    # escreva o conteúdo criado anteriormente nele.
				arquivo.close()
			int(line)
			line+=1
		except NameError:
  			print("erro processo kernel tempo")
	# aplicando função2D do openCV
	opencvOutput = cv2.filter2D(gray, -1, gabor)
	
	i-=1
