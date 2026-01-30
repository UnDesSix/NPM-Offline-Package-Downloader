import json
import os
import subprocess
import tarfile
import shutil
import tempfile

already_dl = set()

SIGNATURE_VALUE = "8VFGpiIQ95JnFwofNU2O73vSviUGgvRT"

def sanitize_package(tgz_path):
    """
    Ouvre le tarball, supprime 'publishConfig' du package.json et le re-package.
    """
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            with tarfile.open(tgz_path, "r:gz") as tar:
                tar.extractall(temp_dir)
            
            pkg_json_path = os.path.join(temp_dir, "package", "package.json")
            
            if not os.path.exists(pkg_json_path):
                return

            modified = False
            with open(pkg_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if "publishConfig" in data:
                del data["publishConfig"]
                modified = True

            if modified:
                with open(pkg_json_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                
                with tarfile.open(tgz_path, "w:gz") as tar:
                    tar.add(os.path.join(temp_dir, "package"), arcname="package")
                
                print(f"{tgz_path}")

    except Exception as e:
        print(f"Erreur lors du nettoyage de {tgz_path}: {e}")

def get_dependencies(package_lock_file_path):
    out_dir = "out"
    os.makedirs(out_dir, exist_ok=True)

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
                        pkg_identifier = (
                            package_name.split("node_modules/")[-1] + "@" + version
                        )
                        
                        result = subprocess.run(
                            [
                                "npm",
                                "pack",
                                pkg_identifier,
                                "--pack-destination",
                                out_dir,
                            ],
                            check=True,
                            capture_output=True,
                            text=True
                        )
                        
                        filename = result.stdout.strip()
                        full_tgz_path = os.path.join(out_dir, filename)

                        if os.path.exists(full_tgz_path):
                            sanitize_package(full_tgz_path)

                        already_dl.add(package_name)
                    except subprocess.CalledProcessError as e:
                        print(f"Erreur npm pack pour {package_name}: {e.stderr}")
                    except Exception as e:
                        print(e)
                        print(f"The installation of {package_name} failed")

    # 2. Create the signature.key file inside the 'out' directory
    with open(os.path.join(out_dir, "signature.key"), "w") as key_file:
        key_file.write(SIGNATURE_VALUE)

    print("Création de l'archive finale...")
    subprocess.run(
        ["tar", "czf", "packages_npm.tar.gz", out_dir],
        check=True,
    )
    
    try:
        shutil.move("packages_npm.tar.gz", "/out/packages_npm.tar.gz")
    except Exception as e:
         print(f"Impossible de déplacer vers /out (peut-être en local?): {e}")

package_lock_file_path = "./package-lock.json"
get_dependencies(package_lock_file_path)