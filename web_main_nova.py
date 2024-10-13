from web_url_feature_nova import WebUrlFeature

class WebMain:
    def __init__(self):
        self.url_feature_extractor = WebUrlFeature()

    def test_single_url(self, url_address):
        # Verifica a URL usando a classe WebUrlFeature
        if not url_address:
            return {}
        
        # Extrai as características da URL usando a classe WebUrlFeature
        url_features = self.url_feature_extractor.extract_url_features(url_address)
        
        if not url_features:
            return {}

        # Retorna as características como um dicionário
        return url_features
