import xmlrpc.client

class IF_ErpOdoo:
#Classe objet d'interface de l'ERP Odoo en XML-RPC
    def __init__(self, erp_ipaddr, erp_port):
    #Methode Constructeur de Classe"
        print("##IF_ErpOdoo Constructor##")
        self.mErpIpAddr = erp_ipaddr
        self.mErpIpPort = erp_port
    def __del__(self):
    #Methode Destructeur de Classe"
        print("##IF_ErpOdoo Destructor##")

    def connect(self):
    #Methode de connexion à l'ERP Odoo
        erp_url = f'http://{self.mErpIpAddr}:{self.mErpIpPort}'
        print("Connexion ODOO")
        print(f"@URL={erp_url}")

if __name__ == "__main__":
    ifOdoo = IF_ErpOdoo("192.168.0.17", "8069") 
    ifOdoo.connect()
