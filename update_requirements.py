import requests


def update_requirements(file_path):
    with open(file_path, "r") as file:
        requirements = file.readlines()

    updated_requirements = []
    for line in requirements:
        if "==" in line and not line.startswith("#"):
            package = line.split("==")[0].strip()
            try:
                response = requests.get(f"https://pypi.org/pypi/{package}/json")
                if response.status_code == 200:
                    latest_version = response.json()["info"]["version"]
                    updated_requirements.append(f"{package}=={latest_version}")
                else:
                    updated_requirements.append(line.strip())
            except requests.RequestException:
                updated_requirements.append(line.strip())
        else:
            updated_requirements.append(line.strip())

    with open(file_path, "w") as file:
        file.write("\n".join(updated_requirements))


# Replace 'path/to/requirements.txt' with the path to your requirements.txt file
update_requirements("requirements.txt")
