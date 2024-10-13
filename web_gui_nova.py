import tkinter as tk
from tkinter import messagebox
from web_main_nova import WebMain
import re

class PhishingDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DARP 2.0")
        self.root.configure(bg="#808080")
        self.setup_ui()
        self.web_main = WebMain()

    def setup_ui(self):
        # Configura a interface
        self.window_width, self.window_height = 800, 400  # Ajuste de altura para acomodar os autores
        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x = (screen_width / 2) - (self.window_width / 2)
        y = (screen_height / 2) - (self.window_height / 2)
        self.root.geometry(f"{self.window_width}x{self.window_height}+{int(x)}+{int(y)}")

        # Frame principal
        frame = tk.Frame(self.root, bg="#808080")
        frame.pack(pady=20)

        # Título
        title = tk.Label(frame, text="DARP 2.0", pady=30, fg="silver", font=("Cambria", 26), bg="#808080")
        title.pack()

        # Entrada de URL centralizada
        input_frame = tk.Frame(frame, bg="#808080")
        input_frame.pack(pady=20)
        self.url_entry = tk.Entry(input_frame, bd=1, width=80)
        self.url_entry.pack(side=tk.TOP, padx=100, pady=10)  # Centralizando a barra de entrada

        # Botão de verificação
        submit_button = tk.Button(frame, text="Check!", command=self.check_url, bg="#d1d6d6", font=("Cambria", 12))
        submit_button.pack(pady=10)

        # Nomes dos autores
        authors_label = tk.Label(frame, text="GRUPO: \nDAVI JOSÉ LUCENA LUIZ\nANA CLARA SANTOS DANDREA\n"
                                             "RAINER TERROSO CARNEIRO\nPEDRO HENRIQUE MARINHO SALVINO",
                                 bg="#808080", fg="white", font=("Arial", 10), pady=20)
        authors_label.pack()

    def check_url(self):
        # Verifica a URL inserida e exibe o resultado
        url = self.url_entry.get()

        if self.is_valid_url(url):
            # Chama a verificação no WebMain
            features = self.web_main.test_single_url(url)
            if self.is_url_safe(features):
                # Exibir um relatório formatado para URLs seguras
                formatted_report = self.format_report(features, segura=True)
                messagebox.showinfo("Resultado", formatted_report)
            else:
                # Exibir um relatório formatado para URLs inseguras
                formatted_report = self.format_report(features, segura=False)
                messagebox.showerror("Alerta", formatted_report)
        else:
            messagebox.showerror("Erro", "Por favor, insira uma URL válida.")

    def is_valid_url(self, url):
        # Função atualizada para verificar URLs completas com ou sem http/https e caminhos adicionais
        url_regex = re.compile(
            r'^(https?://)?'  # Verifica se a URL começa com http:// ou https:// (opcional)
            r'([a-zA-Z0-9-]+(\.[a-zA-Z]{2,})+)'  # Verifica se tem um domínio válido
            r'(/.*)?$'  # Aceita qualquer caminho ou parâmetros após o domínio (opcional)
        )
        if url_regex.match(url):
            # Se a URL não tem http:// ou https://, adicionamos http:// por padrão
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "http://" + url
            return True
        return False

    def is_url_safe(self, features):
        # Valida se a URL é segura com base nos parâmetros
        url_exists = features.get('url_exists', 'Does not exist') == 'Exists'
        safe_browsing_status = features.get('safe_browsing_status', 'Error') == 'Safe'
        url_length_status = features.get('url_length_status', 'Normal') == 'Normal'
        suspicious_chars = not features.get('contains_suspicious_chars', True)
        subdomain_count = features.get('subdomain_count', 0) <= 2

        # A URL é considerada segura se passar por todas essas verificações
        return all([url_exists, safe_browsing_status, url_length_status, suspicious_chars, subdomain_count])

    def format_report(self, features, segura):
        # Função para formatar o relatório com base nos parâmetros extraídos
        url_host = features.get('url_host', 'Desconhecido')
        url_exists = "Positivo" if features.get('url_exists', 'Does not exist') == 'Exists' else "Negativo"
        safe_browsing_status = "Segura" if features.get('safe_browsing_status', 'Error') == 'Safe' else "Não Segura"
        url_length = features.get('url_length', 0)  # Agora exibindo o tamanho exato da URL
        url_length_status = f"{url_length} caracteres (Normal)" if features.get('url_length_status', 'Normal') == 'Normal' else f"{url_length} caracteres (Longa)"
        suspicious_chars = "Negativo" if not features.get('contains_suspicious_chars', True) else "Positivo"
        subdomain_count = features.get('subdomain_count', 0)

        if segura:
            # Formatar o relatório para URLs seguras
            report = (
                f"Análise da URL: {url_host}\n"
                f"A URL existe: {url_exists}\n"
                f"Status de segurança: {safe_browsing_status}\n"
                f"Comprimento da URL: {url_length_status}\n"
                f"Caracteres suspeitos: {suspicious_chars}\n"
                f"Contagem de subdomínios: {subdomain_count}"
            )
        else:
            # Formatar o relatório para URLs inseguras
            report = (
                f"Análise da URL: {url_host}\n"
                f"A URL existe: {url_exists}\n"
                f"Comprimento da URL: {url_length_status}\n"
                f"Caracteres suspeitos: {suspicious_chars}\n"
                f"Contagem de subdomínios: {subdomain_count}\n\n"
                f"*** ALERTA: Esta URL pode ser maliciosa! ***"
            )

        return report

if __name__ == "__main__":
    root = tk.Tk()
    app = PhishingDetectorGUI(root)
    root.mainloop()
