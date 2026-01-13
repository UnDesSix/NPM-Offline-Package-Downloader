import json
import os
import subprocess

already_dl = set()

SIGNATURE_VALUE = "8VFGpiIQ95JnFwofNU2O73vSviUGgvRT"

def get_dependencies(package_lock_file_path):
    os.makedirs("out", exist_ok=True)

    with open(package_lock_file_path, "r") as file:
        package_lock_file = json.load(file)
        if "packages" in package_lock_file:
            for package_name, package_infos in package_lock_file["packages"].items():
                if (
                    not package_name 
                    or package_name in already_dl
                    or package_name.endswith("-cjs")
                ):
                    continue

                resolved = package_infos.get("resolved")
                if not resolved or "registry.npmjs.org" not in resolved:
                    print(f"Skipping local-only package: {package_name}")
                    continue
                if package_name != "" and package_name not in already_dl:
                    try:
                        version = package_infos.get("version")
                        pkg_name = (
                            package_name.split("node_modules/")[-1] + "@" + version
                        )
                        subprocess.run(
                            [
                                "npm",
                                "pack",
                                pkg_name,
                                "--pack-destination",
                                "out",
                            ],
                            check=True,
                        )
                        already_dl.add(package_name)
                    except Exception as e:
                        print(e)
                        print(f"The installation of {package_name} failed")

    # 2. Create the signature.key file inside the 'out' directory
    # This must be done before the 'tar' command so it is included in the archive.
    with open(os.path.join("out", "signature.key"), "w") as key_file:
        key_file.write(SIGNATURE_VALUE)

    subprocess.run(
        ["tar", "czf", "packages_npm.tar.gz", "out"],
        check=True,
    )
    subprocess.run(["mv", "packages_npm.tar.gz", "/out"], check=True)


package_lock_file_path = "./package-lock.json"
get_dependencies(package_lock_file_path)