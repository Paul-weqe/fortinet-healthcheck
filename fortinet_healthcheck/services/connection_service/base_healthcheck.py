from netmiko.fortinet.fortinet_ssh import FortinetSSH


class BaseHealthCheck:
    
    def __init__(self, connection: FortinetSSH):
        self.connection = connection
    
    def run_single_command(self, command):
        output = self.connection.send_command(command)
        return output

    def check_result(self, output: str, expected_substrings: list, check_type: str):
        if check_type == "and":
            return self.check_and_in_output(output, expected_substrings)
        elif check_type == "or":
            return self.check_or_in_output(output, expected_substrings)
        elif check_type == "not":
            return self.check_not_in_output(output, expected_substrings)
        return None

    # check_or_in_output('some string output', ['', '', ''])
    @staticmethod
    def check_or_in_output(output: str, expected_substrings: list):
        is_healthy = False
        for substring in expected_substrings:
            if substring in output:
                is_healthy = True
                break
        return is_healthy
    
    @staticmethod
    def check_and_in_output(output: str, expected_substrings: list):
        for substring in expected_substrings:
            if substring not in output:
                return False

        return True

    @staticmethod
    def check_not_in_output(output: str, expected_substrings: list):
        is_healthy = True
        for substring in expected_substrings:
            if substring in output:
                is_healthy = False
                break
        return is_healthy


# conn = create_connection('176.9.42.123', 'admin', 'Insoft123!')
# health_check = BaseHealthCheck(conn)
# output = health_check.run_single_command("show system global")
# print(health_check.check_or_in_output(output, ["set timezone 04", 'set alias "Fortigate-VM64"']))
