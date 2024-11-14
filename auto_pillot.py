import pyautogui
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from pynput import keyboard
import time

# Configuração do Tesseract
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Caminho padrão do Tesseract no Linux

# Variável para controlar o loop
keep_running = True

# Função para capturar a tela inteira
def capture_screen():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")  # Salva a captura para debug (opcional)
    return screenshot

# Função para pré-processar a imagem para destacar o texto branco
def preprocess_image(image):
    # Converter para escala de cinza
    gray_image = image.convert('L')

    # Aumentar o contraste
    enhancer = ImageEnhance.Contrast(gray_image)
    enhanced_image = enhancer.enhance(2)  # Ajuste o valor conforme necessário

    # Aplicar filtro de nitidez
    sharp_image = enhanced_image.filter(ImageFilter.SHARPEN)

    # Inverter a imagem para tornar o texto branco em preto e o fundo em branco
    inverted_image = sharp_image.point(lambda p: 255 - p)

    inverted_image.save("preprocessed_image.png")  # Salva a imagem pré-processada para debug (opcional)
    return inverted_image

# Função para procurar o texto apenas nos 20% da área à direita da imagem
def find_text_in_image(image, target_text):
    # Pega as dimensões da imagem
    width, height = image.size

    # Define a área de 20% à direita
    left = width * 0.8  # Começa 80% da largura (ou seja, últimos 20%)
    top = 0             # Do topo da imagem
    right = width * 0.92  # Até a largura total
    bottom = height * 0.5  # Até a altura total

    # Recorta a imagem para a área desejada
    cropped_image = image.crop((left, top, right, bottom))
    cropped_image.save("cropped_screenshot.png")  # Salva a imagem recortada para debug (opcional)

    # Converte a imagem recortada para string usando OCR
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(cropped_image, config=custom_config)
    print(f"Texto encontrado na área recortada: {text}")  # Exibe o texto detectado para debug

    return target_text in text

# Função para processar pressionamento de teclas
def on_press(key):
    global keep_running
    try:
        if key.char == 'r':
            print("Capturando a tela...")
            screenshot = capture_screen()

            # Tenta encontrar o texto nos 20% à direita da imagem
            if find_text_in_image(screenshot, target_text):
                print(f"O texto '{target_text}' foi encontrado na imagem!")
            else:
                print(f"O texto '{target_text}' NÃO foi encontrado na imagem.")

        elif key.char == 'p':
            print("Encerrando o programa...")
            keep_running = False
            return False  # Para parar o listener
    except AttributeError:
        pass  # Ignora teclas especiais (shift, ctrl, etc.)

# Código principal
if __name__ == "__main__":
    # Define o texto que você quer procurar
    target_text = "Inigo"

    # Listener de teclado
    with keyboard.Listener(on_press=on_press) as listener:
        while keep_running:
            time.sleep(0.1)
