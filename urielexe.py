import sys
import bcrypt
import subprocess
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QMessageBox, QListWidget, QStackedWidget, QTextEdit, QFileDialog, QHBoxLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from pyfiglet import Figlet

try:
    import pyautogui
except ImportError:
    pyautogui = None

# ASCII art estilizado
ASCII_ART = Figlet(font='slant').renderText('URIEL')

# Senha hardcoded (hash bcrypt)
senha_hash = bcrypt.hashpw(b"admin123", bcrypt.gensalt())

class LoginPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        titulo = QLabel("Login - Painel de Hack Ético")
        titulo.setFont(QFont("Arial", 16))
        titulo.setAlignment(Qt.AlignCenter)

        self.label_user = QLabel("Usuário:")
        self.input_user = QLineEdit()

        self.label_pass = QLabel("Senha:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Entrar")
        self.btn_login.clicked.connect(self.check_login)

        layout.addWidget(titulo)
        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def check_login(self):
        user = self.input_user.text()
        password = self.input_pass.text().encode('utf-8')
        if user == "admin":
            if bcrypt.checkpw(password, senha_hash):
                self.parent.show_main()
            else:
                QMessageBox.warning(self, "Erro", "Senha incorreta!")
        else:
            QMessageBox.warning(self, "Erro", "Usuário incorreto!")

class MainPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        ascii_label = QLabel(ASCII_ART)
        ascii_label.setFont(QFont("Courier", 8))
        ascii_label.setAlignment(Qt.AlignCenter)

        welcome_label = QLabel("Bem-vindo ao painel de hacking ético URIEL!")
        welcome_label.setFont(QFont("Arial", 14))
        welcome_label.setAlignment(Qt.AlignCenter)

        btn_menu = QPushButton("Acessar Ferramentas Avançadas")
        btn_menu.clicked.connect(self.parent.show_menu)

        layout.addWidget(ascii_label)
        layout.addWidget(welcome_label)
        layout.addWidget(btn_menu)

        self.setLayout(layout)

class MenuPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        titulo = QLabel("Ferramentas Avançadas e Recursos Extras")
        titulo.setFont(QFont("Arial", 16))
        titulo.setAlignment(Qt.AlignCenter)

        self.opcoes = QListWidget()
        self.opcoes.addItem("Scanner de Rede")
        self.opcoes.addItem("Testar Portas")
        self.opcoes.addItem("Executar Comando System")
        self.opcoes.addItem("Captura de Tela")
        self.opcoes.addItem("Análise de Vulnerabilidades")
        self.opcoes.addItem("Automação de Tarefas")
        self.opcoes.addItem("Ver Logs Detalhados")
        self.opcoes.addItem("Estatísticas")
        self.opcoes.addItem("Verificar IP via API")
        self.opcoes.addItem("Simulação de Ataque")
        self.opcoes.addItem("Histórico de Comandos")
        self.opcoes.addItem("Sair")

        self.opcoes.itemClicked.connect(self.opcao_selecionada)

        layout.addWidget(titulo)
        layout.addWidget(self.opcoes)

        self.setLayout(layout)

    def opcao_selecionada(self, item):
        opcao = item.text()
        if opcao == "Sair":
            reply = QMessageBox.question(self, "Sair", "Deseja realmente sair?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.parent.show_login()
        elif opcao == "Scanner de Rede":
            self.parent.show_scanner()
        elif opcao == "Testar Portas":
            self.parent.show_port_scanner()
        elif opcao == "Executar Comando System":
            self.parent.show_command_executor()
        elif opcao == "Captura de Tela":
            self.parent.show_screenshot()
        elif opcao == "Análise de Vulnerabilidades":
            self.parent.show_vulnerability_analysis()
        elif opcao == "Automação de Tarefas":
            self.parent.show_task_automation()
        elif opcao == "Ver Logs Detalhados":
            self.parent.show_logs()
        elif opcao == "Estatísticas":
            self.parent.show_statistics()
        elif opcao == "Verificar IP via API":
            self.parent.show_ip_check()
        elif opcao == "Simulação de Ataque":
            self.parent.show_attack_simulation()
        elif opcao == "Histórico de Comandos":
            self.parent.show_command_history()

class ScannerPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label = QLabel("Scanner de Rede (IP ou Host):")
        self.input_ip = QLineEdit()
        btn_start = QPushButton("Iniciar Scanner")
        btn_start.clicked.connect(self.run_scan)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        btn_voltar = QPushButton("Voltar")
        btn_voltar.clicked.connect(self.parent.show_menu)

        layout.addWidget(label)
        layout.addWidget(self.input_ip)
        layout.addWidget(btn_start)
        layout.addWidget(self.output)
        layout.addWidget(btn_voltar)

        self.setLayout(layout)

    def run_scan(self):
        target = self.input_ip.text()
        if not target:
            QMessageBox.warning(self, "Aviso", "Insira um IP ou hostname válido.")
            return
        self.output.clear()
        self.output.append(f"Realizando scan de rede em: {target}\n")
        try:
            output = subprocess.check_output(["ping", "-c", "4", target], universal_newlines=True)
            self.output.append(output)
        except Exception as e:
            self.output.append(f"Erro ao executar ping: {e}")

class PortScannerPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label = QLabel("Verificar portas (ex: 80,443,22):")
        self.input_ports = QLineEdit()
        label_ip = QLabel("IP ou Host:")
        self.input_host = QLineEdit()

        btn_start = QPushButton("Iniciar Varredura de Portas")
        btn_start.clicked.connect(self.run_port_scan)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        btn_voltar = QPushButton("Voltar")
        btn_voltar.clicked.connect(self.parent.show_menu)

        layout.addWidget(label_ip)
        layout.addWidget(self.input_host)
        layout.addWidget(label)
        layout.addWidget(self.input_ports)
        layout.addWidget(btn_start)
        layout.addWidget(self.output)
        layout.addWidget(btn_voltar)

        self.setLayout(layout)

    def run_port_scan(self):
        host = self.input_host.text()
        ports = self.input_ports.text()
        if not host or not ports:
            QMessageBox.warning(self, "Aviso", "Insira IP/Host e portas.")
            return
        self.output.clear()
        port_list = [p.strip() for p in ports.split(",")]
        for port in port_list:
            self.output.append(f"Verificando porta {port} em {host}...")
            try:
                result = subprocess.check_output(["nc", "-zv", host, port], stderr=subprocess.STDOUT, universal_newlines=True)
                self.output.append(f"Porta {port}: Aberta ou Filtrada\n")
            except subprocess.CalledProcessError:
                self.output.append(f"Porta {port}: Fechada ou não acessível\n")
        self.output.append("Varredura concluída.")

class CommandExecutorPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.command_history = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label = QLabel("Digite o comando do sistema para executar:")
        self.command_input = QLineEdit()

        btn_exec = QPushButton("Executar")
        btn_exec.clicked.connect(self.execute_command)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        btn_voltar = QPushButton("Voltar")
        btn_voltar.clicked.connect(self.parent.show_menu)

        layout.addWidget(label)
        layout.addWidget(self.command_input)
        layout.addWidget(btn_exec)
        layout.addWidget(QLabel("Saída:"))
        layout.addWidget(self.output)
        layout.addWidget(btn_voltar)

        self.setLayout(layout)

    def execute_command(self):
        cmd = self.command_input.text()
        if not cmd:
            QMessageBox.warning(self, "Aviso", "Insira um comando válido.")
            return
        self.command_history.append(cmd)
        try:
            output = subprocess.check_output(cmd, shell=True, universal_newlines=True, stderr=subprocess.STDOUT)
            self.output.append(f"> {cmd}\n{output}\n")
        except Exception as e:
            self.output.append(f"> {cmd}\nErro: {e}\n")

class ScreenshotPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Captura de Tela")
        btn_capturar = QPushButton("Capturar Tela")
        btn_capturar.clicked.connect(self.take_screenshot)
        self.image_path_label = QLabel("")
        btn_voltar = QPushButton("Voltar")
        btn_voltar.clicked.connect(self.parent.show_menu)

        layout.addWidget(label)
        layout.addWidget(btn_capturar)
        layout.addWidget(self.image_path_label)
        layout.addWidget(btn_voltar)

        self.setLayout(layout)

    def take_screenshot(self):
        if pyautogui:
            path, _ = QFileDialog.getSaveFileName(self, "Salvar Captura", "", "PNG Files (*.png)")
            if path:
                screenshot = pyautogui.screenshot()
                screenshot.save(path)
                self.image_path_label.setText(f"Captura salva em: {path}")
        else:
            QMessageBox.warning(self, "Aviso", "PyAutoGUI não está instalado. Instale para usar essa função.")

class VulnerabilityAnalysisPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label = QLabel("Análise de Vulnerabilidades (Simulação)")
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        btn_analisar = QPushButton("Executar Análise")
        btn_analisar.clicked.connect(self.run_analysis)

        btn_voltar = QPushButton("Voltar")
        btn_voltar.clicked.connect(self.parent.show_menu)

        layout.addWidget(label)
        layout.addWidget(self.result_area)
        layout.addWidget(btn_analisar)
        layout.addWidget(btn_voltar)

        self.setLayout(layout)

    def run_analysis(self):
        resultados = [
            "Vuln 1: Vulnerabilidade X detectada.",
            "Vuln 2: Vulnerabilidade Y detectada.",
            "Vuln 3: Nenhuma vulnerabilidade crítica encontrada."
        ]
        self.result_area.clear()
        for r in resultados:
            self.result_area.append(r)

class AttackSimulationPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label = QLabel("Simulação de Ataque (Fictício)")
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        btn_simular = QPushButton("Iniciar Simulação")
        btn_simular.clicked.connect(self.run_simulation)

        btn_voltar = QPushButton("Voltar")
        btn_voltar.clicked.connect(self.parent.show_menu)

        layout.addWidget(label)
        layout.addWidget(self.output_area)
        layout.addWidget(btn_simular)
        layout.addWidget(btn_voltar)

        self.setLayout(layout)

    def run_simulation(self):
        mensagens = [
            "Iniciando ataque simulado...",
            "Verificando vulnerabilidades...",
            "Tentativa de invasão bem-sucedida na simulação.",
            "Ataque finalizado com sucesso na simulação."
        ]
        self.output_area.clear()
        for msg in mensagens:
            self.output_area.append(msg)

class CommandHistoryPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.commands = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label = QLabel("Histórico de Comandos Executados")
        self.history_area = QTextEdit()
        self.history_area.setReadOnly(True)

        btn_atualizar = QPushButton("Atualizar")
        btn_atualizar.clicked.connect(self.load_history)
        btn_limpar = QPushButton("Limpar")
        btn_limpar.clicked.connect(self.clear_history)
        btn_voltar = QPushButton("Voltar")
        btn_voltar.clicked.connect(self.parent.show_menu)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_atualizar)
        btn_layout.addWidget(btn_limpar)
        btn_layout.addWidget(btn_voltar)

        layout.addWidget(label)
        layout.addWidget(self.history_area)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def load_history(self):
        self.history_area.setPlainText("\n".join(self.commands))

    def clear_history(self):
        self.commands.clear()
        self.history_area.clear()

    def add_command(self, cmd):
        self.commands.append(cmd)

class IPCheckPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label = QLabel("Verificar IP via API externa")
        self.ip_input = QLineEdit()
        btn_verificar = QPushButton("Verificar IP")
        btn_verificar.clicked.connect(self.check_ip)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)

        btn_voltar = QPushButton("Voltar")
        btn_voltar.clicked.connect(self.parent.show_menu)

        layout.addWidget(label)
        layout.addWidget(self.ip_input)
        layout.addWidget(btn_verificar)
        layout.addWidget(self.result_area)
        layout.addWidget(btn_voltar)

        self.setLayout(layout)

    def check_ip(self):
        ip = self.ip_input.text()
        if not ip:
            QMessageBox.warning(self, "Aviso", "Insira um IP válido.")
            return
        try:
            response = requests.get(f"https://api.ipify.org?format=json")
            if response.status_code == 200:
                self.result_area.setPlainText(f"IP pública detectada: {response.json()['ip']}")
            else:
                self.result_area.setPlainText("Falha na verificação do IP.")
        except Exception as e:
            self.result_area.setPlainText(f"Erro na requisição: {e}")

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.stack = QStackedWidget()

        self.login_page = LoginPage(self)
        self.main_page = MainPage(self)
        self.menu_page = MenuPage(self)
        self.scanner_page = ScannerPage(self)
        self.port_scanner_page = PortScannerPage(self)
        self.command_executor_page = CommandExecutorPage(self)
        self.screenshot_page = ScreenshotPage(self)
        self.vuln_page = VulnerabilityAnalysisPage(self)
        self.attack_page = AttackSimulationPage(self)
        self.command_history_page = CommandHistoryPage(self)
        self.ip_check_page = IPCheckPage(self)

        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.main_page)
        self.stack.addWidget(self.menu_page)
        self.stack.addWidget(self.scanner_page)
        self.stack.addWidget(self.port_scanner_page)
        self.stack.addWidget(self.command_executor_page)
        self.stack.addWidget(self.screenshot_page)
        self.stack.addWidget(self.vuln_page)
        self.stack.addWidget(self.attack_page)
        self.stack.addWidget(self.command_history_page)
        self.stack.addWidget(self.ip_check_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

        self.setWindowTitle("Painel de Hack Ético - URIEL")
        self.setGeometry(100, 100, 950, 750)

        self.show_login()

    def show_login(self):
        self.stack.setCurrentWidget(self.login_page)

    def show_main(self):
        self.stack.setCurrentWidget(self.main_page)

    def show_menu(self):
        self.stack.setCurrentWidget(self.menu_page)

    def show_scanner(self):
        self.stack.setCurrentWidget(self.scanner_page)

    def show_port_scanner(self):
        self.stack.setCurrentWidget(self.port_scanner_page)

    def show_command_executor(self):
        self.stack.setCurrentWidget(self.command_executor_page)

    def show_screenshot(self):
        self.stack.setCurrentWidget(self.screenshot_page)

    def show_vulnerability_analysis(self):
        self.stack.setCurrentWidget(self.vuln_page)

    def show_attack_simulation(self):
        self.stack.setCurrentWidget(self.attack_page)

    def show_command_history(self):
        self.stack.setCurrentWidget(self.command_history_page)

    def show_ip_check(self):
        self.stack.setCurrentWidget(self.ip_check_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())