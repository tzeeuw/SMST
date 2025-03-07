from PySide6 import QtWidgets
import os
import json
import requests






#TODO: fix this mess of a code
class create_window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("create server")
        self.ok_button = QtWidgets.QPushButton("Create server")
        self.ok_button.clicked.connect(self.download)
        self.ok_button.setEnabled(False)


        self.file_button = QtWidgets.QPushButton("choose folder")
        self.file_button.clicked.connect(self.get_file_name)
        self.folder = None


        self.centrallayout = QtWidgets.QVBoxLayout()
        
        self.setLayout(self.centrallayout)

        self.installation_dropbox = QtWidgets.QComboBox()

        self.centrallayout.addWidget(self.file_button)
        self.centrallayout.addWidget(self.installation_dropbox)

        self.version_list = json.load(open("versions.json", 'r'))

        self.installation_versions = self.version_list.keys()

        self.installation_dropbox.setPlaceholderText("--choose installation--")

        self.installation_dropbox.addItems(self.installation_versions)

        self.installation_dropbox.currentIndexChanged.connect(self.index_change)


        self.eula_hbox = QtWidgets.QHBoxLayout()
        self.eula_hbox.setContentsMargins(0,0,0,0)

        self.eula_check = QtWidgets.QCheckBox()
        self.eula_check.checkStateChanged.connect(lambda: self.ok_button.setEnabled((self.ok_button.isEnabled() + 1) % 2))


        self.eula_text = QtWidgets.QLabel()
        self.eula_text.setText('I accept the <a href="https://aka.ms/MinecraftEULA">Minecraft EULA</a>')
        self.eula_text.setOpenExternalLinks(True)

        self.eula_hbox.addWidget(self.eula_check, 0)
        self.eula_hbox.addWidget(self.eula_text, 1)

        self.version_dropbox = QtWidgets.QComboBox()
        self.centrallayout.addWidget(self.version_dropbox)
        self.version_dropbox.setPlaceholderText("--choose version--")
        self.centrallayout.addLayout(self.eula_hbox)

        self.centrallayout.addWidget(self.ok_button)
        
        self.close_button = QtWidgets.QPushButton("close")
        self.close_button.clicked.connect(self.close)
        
        self.centrallayout.addWidget(self.close_button)

    def index_change(self):
        self.version_dropbox.clear()
        installation = self.installation_dropbox.currentText()
        
        self.version_dropbox.addItems(self.version_list[installation].keys())

    def get_file_name(self):
        self.folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose folder")
        print(self.folder)


    def download(self):
        version = self.version_dropbox.currentText()
        installation = self.installation_dropbox.currentText()


        if installation in self.version_list.keys():
            if version in self.version_list[installation].keys():
                if self.folder:

                    install_path = f"{self.folder}/smst_{installation}_{version}"

                    if not os.path.exists(install_path):
                        os.makedirs(install_path)


                    url = self.get_url(installer=installation, version=version)

                    if not url:
                        print("url not found")
                        return
                    
                    query_params = {"dowloadformat": "jar"}

                    response = requests.get(url, params=query_params)
                    print(response.ok)

                    if response.ok:
                        with open(f"{install_path}/server_{installation}_{version}.jar", mode="wb") as file:
                            file.write(response.content)
                else:
                    print("no folder selected or something")

            else:
                print("not correct version or somethign idk")

        else:
            print("not allowed installation or something idk")


    def get_url(self, installer, version):
        url_version = self.version_list[installer][version]

        if installer == "forge":
            return f"https://maven.minecraftforge.net/net/minecraftforge/forge/{url_version}/forge-{url_version}-installer.jar"
        
        elif installer == "vanilla":
            return f"https://piston-data.mojang.com/v1/objects/{url_version}/server.jar"
        
        elif installer == "paper":
            return f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/{url_version}/downloads/paper-{version}-{url_version}.jar"
        
        elif installer == "fabric":
            return f"https://meta.fabricmc.net/v2/versions/loader/{version}/{url_version}/server/jar"

        return False
    