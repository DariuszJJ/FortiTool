import csv

csv_file = "users.csv"

user_group_name = "SSLVPN-users"

config_lines = ["config user local"]

group_members = []

with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)

    for row in reader:
        username = row['username']
        fortitoken = row['fortitoken']
        email = row['email']
        ldap_server = row['ldap_server']

        config_lines.append(f"""
    edit "{username}"
        set type ldap
        set two-factor fortitoken
        set fortitoken "{fortitoken}"
        set email-to "{email}"
        set ldap-server "{ldap_server}"
    next
        """)

        group_members.append(username)

config_lines.append("end")

config_lines.append(f"""
config user group
    edit "{user_group_name}"
        set member {" ".join(f'"{user}"' for user in group_members)}
    next
end
""")

output_file = "fortigate_ldap_users_and_group_config.txt"
with open(output_file, 'w') as file:
    file.writelines(config_lines)

print(f"Konfiguracja została zapisana do pliku: {output_file}")
