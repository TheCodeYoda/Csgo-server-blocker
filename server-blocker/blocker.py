from collections import defaultdict
import requests
import fire


class ServerBlock:

    def __init__(self):
        self.server_object = self.get_sdrRelayConfig()
        self.alive_regions = self.construct_alive_ip_list()

    def get_sdrRelayConfig(self):
        response = requests.get("https://raw.githubusercontent.com/SteamDatabase/SteamTracking/master/Random/NetworkDatagramConfig.json")
        return response.json()

    
    def construct_alive_ip_list(self):
        alive_regions = defaultdict(lambda:[])
        for region in self.server_object["pops"]:
            if("relays" in self.server_object["pops"][region].keys() and "desc" in self.server_object["pops"][region].keys()):
                region_name = (self.server_object["pops"][region]["desc"])
                ips = []
                for ip in self.server_object["pops"][region]["relays"]:
                    ips.append(ip["ipv4"])
                alive_regions[region_name] += ips
        return alive_regions

    def display_all_ips(self):
        for region in self.alive_regions:
            print(region)
            for ip in self.alive_regions[region]:
                print(ip)
            print("\n\n")

    #display regions
    def display_regions(self):
        return_str = ""
        for region in self.alive_regions.keys():
            return_str += f"{region}\n"
        return return_str

    #display region ips
    def display_region_ip(self, region):
        return_str = ""
        return_str += region + "\n"
        for ip in self.alive_regions[region]:
            return_str += ip+"\n"
        return return_str

    #Block particular ip
    def blockip(self, ip_address):
        import subprocess
        try:
            subprocess.run(f"netsh advfirewall firewall add rule name=\"IP Block\" dir=out interface=any action=block remoteip={ip_address}/32")
        except:
            print("Something went wrong while blocking ip")
        finally:
            print(f"Blocked ip: {ip_address}.....")


    #Block particular region
    def blockRegion(self, region_name):
        for ip in self.alive_regions[region_name]:
            self.blockip(ip)
        return f"Blocked all ips in region {region_name}....."

    #Block all except Indian Servers
    def blockDefault(self):
        for region in self.alive_regions:
            if(region!="Mumbai" and region!="Chennai"):
                self.blockRegion(region)
        return "Blocked All regions except Mumbai and Chennai"

    def help(self):
        print("Usage:")
        print("Display Commands: python3 blocker.py {CommandName}")
        print("Blocking Commands: gsudo python3 blocker.py {CommandName}\n")
        print("Commands:")
        print("display_all_ips --------------------------> Displays All IPs regionwise")
        print("display_regions --------------------------> Displays All regions")
        print("display_region_ip {region} --------------------------> Displays All IPs active in a particular region")
        print("blockip {ipAdress} --------------------------> Blocks a particular IP Address [NEEDS ADMIN PRIVELEGES]")
        print("blockRegion {region} -----------------------> Blocks a particular Region [NEEDS ADMIN PRIVELEGES]")
        print("help ---------------------------------> Help menu")
        print("blockDefault ------------------------------> Blocks All regions except \'Mumbai\' and \'Chennai\'\n")
        print("NOTE: Blocking commands need Admin Privileges use install gsudo and run [https://github.com/gerardog/gsudo].")
        print("NOTE: Scripts needs to be run only once, firewall rules persist through shutdowns.")



# REGIONS
# Atlanta
# Mumbai
# Dubai
# Buenos Aires
# Frankfurt
# Sao Paulo
# Hong Kong
# Sterling
# Johannesburg
# Los Angeles
# Lima
# Chennai
# Madrid
# Chicago
# PW Guangdong 1
# PW Hebei
# PW Wuhan
# PW Zhejiang
# Santiago
# Seoul
# Singapore
# Shanghai (sha-4) Backbone
# Stockholm (Kista)        
# Sydney
# Tokyo (North)
# Vienna
# Warsaw


#netsh advfirewall firewall add rule name="IP Block" dir=in interface=any action=block remoteip=<IP_Address>/32



if __name__ == "__main__":
    fire.Fire(ServerBlock)



