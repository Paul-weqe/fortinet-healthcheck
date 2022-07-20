from netmiko import Netmiko


class FortinetException(Exception):
    pass


def create_connection(hostname: str, username: str, password: str):
    conn_details = {
        'device_type': 'fortinet',
        'host': hostname, 
        'username': username, 
        'password': password
    }
    try:
        conn = Netmiko(**conn_details)
        return conn
    except Exception as e:
        raise FortinetException(f"Unable to connect to host: {hostname}\nERROR: \n {e}")

