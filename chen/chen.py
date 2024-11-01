import sublist3r
import requests
import logging
import re
import warnings
from Wappalyzer import Wappalyzer, WebPage
from modules.misc import Colors, save_results


def run_chen(domain):
    cleaned_domain = re.sub(r"https?://|www\.|/$", "", domain) # normalize input domain to confirm to sublister, and for better control of program behavior

    subdomains = sublist3r.main(cleaned_domain, 25, savefile=False, ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None)

    alive_subdomains = []
    dead_subdomains = []

    for subdomain in subdomains:
        try:
            logging.info(f"Checking if {subdomain} is alive")
            response = requests.get(f"https://{subdomain}", timeout=4)
            status = response.status_code
            print(f"{Colors.GREEN}{subdomain} ({status}){Colors.RESET}")
            alive_subdomains.append(subdomain)

            logging.info(f"Successful check, subdomains alive")
        except (requests.ConnectionError, requests.Timeout) as e:
            print(f"{Colors.RED}{subdomain}{Colors.RESET}")
            dead_subdomains.append(subdomain)
            logging.info(f"Failed to connect to {subdomain}: {e}")

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            print(f"{Colors.RED}Unexpected error {e}{Colors.RESET}")

    full_wappy_results = []

    try:
        print(f"\n{Colors.YELLOW}Running Wappalyzer on alive subdomains~{Colors.RESET}")
        logging.info(f"Running Wappalyzer on alive subdomains")
        for subdomain in alive_subdomains:
            https_fix = f"https://{subdomain}" # wappy wants https, sublister doesn't, what can u do
            wappy_result = wappy(https_fix)
            full_wappy_results.append(f"[{subdomain}]\n{wappy_result}\n\n")
            print(f"{Colors.GREEN}\n[{subdomain}]{Colors.RESET}\n{wappy_result}")
    except Exception:
        logging.error(f"Wappalyzer failed")
        print("Wappalyzer failed")

    save_results(full_wappy_results, "chen/alive", f"{cleaned_domain}.txt")
    print(f"{Colors.YELLOW}\nResults saved in chen/alive/{cleaned_domain}.txt{Colors.RESET}")

def wappy(alive_subdomains):
    # stahp library bug from Wappalyzer
    warnings.filterwarnings("ignore", category=UserWarning)

    wappalyzer = Wappalyzer.latest()
    
    webpage = WebPage.new_from_url(alive_subdomains)
    
    technology = wappalyzer.analyze_with_versions(webpage)

    # Clean up weird formating
    wappy_results = []
    for tech, deets in technology.items():
        version = deets.get("versions")

        clean_ver = ", ".join(version) if version else ""

        wappy_results.append(f"{tech} {clean_ver}")

    return "\n".join(wappy_results)
