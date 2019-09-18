from skimage.exposure import rescale_intensity
import numpy as np
import argparse
import cv2
import pdb

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
	print(np.median(output), sep = "\n")
	
	return output

# argumento de imagem
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())

# kernels
smallBlur = np.ones((7, 7), dtype="float") * (1.0 / (7 * 7))
largeBlur = np.ones((21, 21), dtype="float") * (1.0 / (21 * 21))
gabor = cv2.getGaborKernel((21,21), 5, 1, 10, 1, 0, cv2.CV_32F)


sharpen = np.array((
	[0, -1, 0],
	[-1, 5, -1],
	[0, -1, 0]), dtype="int")

laplacian = np.array((
	[0, 1, 0],
	[1, -4, 1],
	[0, 1, 0]), dtype="int")

sobelX = np.array((
	[-1, 0, 1],
	[-2, 0, 2],
	[-1, 0, 1]), dtype="int")

sobelY = np.array((
	[-1, -2, -1],
	[0, 0, 0],
	[1, 2, 1]), dtype="int")

# construir o banco de kernel, uma lista de kernels que vamos
# aplicar usando a função `convole` e a Função filter2D do OpenCV

kernelBank = (
        ("gabor", gabor),
	("large_blur", largeBlur),
	("sharpen", sharpen),
	("laplacian", laplacian),
	("sobel_x", sobelX),
	("sobel_y", sobelY)        
)

# carrega a imagem de entrada e convert para escala de cinza.
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# loop over the kernels
for (kernelName, kernel) in kernelBank:
	print("[INFO] aplicando {} kernel".format(kernelName))
	# aplicando função convolve
	convoleOutput = convolve(gray, kernel)
	# aplicando função2D do openCV
	opencvOutput = cv2.filter2D(gray, -1, kernel)

	# mostrar imagens de saída
	cv2.imshow("original", gray)
	cv2.imshow("{} - convole".format(kernelName), convoleOutput)
	
	#cv2.imshow("{} - opencv".format(kernelName), opencvOutput)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
