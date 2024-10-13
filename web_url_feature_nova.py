import re
import urllib.parse
import logging
import requests

class WebUrlFeature:
    def __init__(self):
        self.feature_extracted = {}
        self.google_api_key = 'AIzaSyACgG0seIVAz_knLQqqWWOn8DCjpGRvuVE'  # Chave API do Google Safebrowsing

    def extract_url_features(self, url_address):
        try:
            url_host = self.get_url_host(url_address)
            self.feature_extracted['url_host'] = url_host

            # Verificar se a URL realmente existe
            existence_status = self.check_url_existence(url_host)
            self.feature_extracted['url_exists'] = existence_status
            
            # Verificação usando a Google Safe Browsing API
            safe_browsing_result = self.check_safe_browsing(url_address)
            self.feature_extracted['safe_browsing_status'] = safe_browsing_result
            
            # Verificações heurísticas adicionais
            heuristics = self.heuristic_url_analysis(url_address)
            self.feature_extracted.update(heuristics)

        except Exception as e:
            logging.error(f"Erro ao extrair características da URL {url_address}: {e}")
            return {}
        
        return self.feature_extracted

    def get_url_host(self, url_address):
        # Simples extração do host de uma URL usando urllib.parse
        try:
            parsed_url = urllib.parse.urlparse(url_address)
            if not parsed_url.netloc:
                return url_address
            return parsed_url.netloc
        except Exception as e:
            logging.error(f"Erro ao extrair host da URL {url_address}: {e}")
            return None

    def check_url_existence(self, url_host):
        # Verifica se a URL realmente existe tentando resolvê-la
        try:
            # Tentar fazer uma requisição HEAD para verificar se o domínio responde
            response = requests.head(f"http://{url_host}", timeout=5)
            if response.status_code < 400:
                return "Exists"
            else:
                return "Does not exist"
        except requests.RequestException:
            return "Does not exist"

    def check_safe_browsing(self, url_address):
        # Verifica a URL usando a API Google Safe Browsing
        try:
            endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={self.google_api_key}"
            payload = {
                "client": {
                    "clientId": "yourcompanyname",
                    "clientVersion": "1.5.2"
                },
                "threatInfo": {
                    "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
                    "platformTypes": ["ANY_PLATFORM"],
                    "threatEntryTypes": ["URL"],
                    "threatEntries": [{"url": url_address}]
                }
            }
            response = requests.post(endpoint, json=payload)

            if response.status_code == 200:
                if response.json().get('matches'):
                    return "Malicious"
                else:
                    return "Safe"
            else:
                logging.error(f"Erro na consulta à API Google Safe Browsing para {url_address}: {response.status_code}")
                return "Error"
        except Exception as e:
            logging.error(f"Erro ao consultar Google Safe Browsing para {url_address}: {e}")
            return "Error"

    def heuristic_url_analysis(self, url_address):
        # Análise heurística básica da URL
        heuristics = {}

        # Verificar se a URL tem muitos subdomínios
        parsed_url = urllib.parse.urlparse(url_address)
        subdomains = parsed_url.netloc.split('.')
        heuristics['subdomain_count'] = len(subdomains) - 2  # Descontando o domínio e TLD

        # Verificar comprimento da URL
        heuristics['url_length'] = len(url_address)
        heuristics['url_length_status'] = "Long" if len(url_address) > 75 else "Normal"

        # Verificar presença de caracteres suspeitos
        suspicious_chars = ['-', '_', '%', '@', '!', '~', '#']
        heuristics['contains_suspicious_chars'] = any(char in url_address for char in suspicious_chars)

        return heuristics




'''import re
import urllib.parse
import logging
import requests

class WebUrlFeature:
    def __init__(self):
        self.feature_extracted = {}
        self.google_api_key = 'AIzaSyACgG0seIVAz_knLQqqWWOn8DCjpGRvuVE'  # Coloque sua chave de API aqui

    def extract_url_features(self, url_address):
        try:
            url_host = self.get_url_host(url_address)
            self.feature_extracted['url_host'] = url_host

            # Verificação usando a Google Safe Browsing API
            safe_browsing_result = self.check_safe_browsing(url_address)
            self.feature_extracted['safe_browsing_status'] = safe_browsing_result
            
            # Verificações heurísticas adicionais
            heuristics = self.heuristic_url_analysis(url_address)
            self.feature_extracted.update(heuristics)

        except Exception as e:
            logging.error(f"Erro ao extrair características da URL {url_address}: {e}")
            return {}
        
        return self.feature_extracted

    def get_url_host(self, url_address):
        """ Simples extração do host de uma URL usando urllib.parse """
        try:
            parsed_url = urllib.parse.urlparse(url_address)
            if not parsed_url.netloc:
                return url_address
            return parsed_url.netloc
        except Exception as e:
            logging.error(f"Erro ao extrair host da URL {url_address}: {e}")
            return None

    def check_safe_browsing(self, url_address):
        """ Verifica a URL usando a API Google Safe Browsing """
        try:
            endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={self.google_api_key}"
            payload = {
                "client": {
                    "clientId": "yourcompanyname",
                    "clientVersion": "1.5.2"
                },
                "threatInfo": {
                    "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
                    "platformTypes": ["ANY_PLATFORM"],
                    "threatEntryTypes": ["URL"],
                    "threatEntries": [{"url": url_address}]
                }
            }
            response = requests.post(endpoint, json=payload)

            if response.status_code == 200:
                if response.json().get('matches'):
                    return "Malicious"
                else:
                    return "Safe"
            else:
                logging.error(f"Erro na consulta à API Google Safe Browsing para {url_address}: {response.status_code}")
                return "Error"
        except Exception as e:
            logging.error(f"Erro ao consultar Google Safe Browsing para {url_address}: {e}")
            return "Error"

    def heuristic_url_analysis(self, url_address):
        """ Análise heurística básica da URL """
        heuristics = {}

        # Verificar se a URL tem muitos subdomínios
        parsed_url = urllib.parse.urlparse(url_address)
        subdomains = parsed_url.netloc.split('.')
        heuristics['subdomain_count'] = len(subdomains) - 2  # Descontando o domínio e TLD

        # Verificar comprimento da URL
        heuristics['url_length'] = len(url_address)
        heuristics['url_length_status'] = "Long" if len(url_address) > 75 else "Normal"

        # Verificar presença de caracteres suspeitos
        suspicious_chars = ['-', '_', '%', '@', '!', '~', '#']
        heuristics['contains_suspicious_chars'] = any(char in url_address for char in suspicious_chars)

        return heuristics
'''