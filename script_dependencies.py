import json
import os
import subprocess
import tarfile
import shutil
import tempfile
from tqdm import tqdm

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
                
                print(f"[SANITIZED] {tgz_path}")

    except Exception as e:
        print(f"[ERROR] Erreur lors du nettoyage de {tgz_path}: {e}")


def get_dependencies(package_lock_file_path):
    out_dir = "out"
    os.makedirs(out_dir, exist_ok=True)

    with open(package_lock_file_path, "r", encoding="utf-8") as file:
        package_lock_file = json.load(file)

    packages = [
        (name, info)
        for name, info in package_lock_file.get("packages", {}).items()
        if name and name not in already_dl and not name.endswith("-cjs")
    ]

    for package_name, package_infos in tqdm(packages, desc="Téléchargement packages", unit="pkg"):
        resolved = package_infos.get("resolved")
        if not resolved or "registry.npmjs.org" not in resolved:
            print(f"[SKIP] Local-only package: {package_name}")
            continue

        version = package_infos.get("version")
        pkg_identifier = package_name.split("node_modules/")[-1] + "@" + version
        print(f"[INFO] Traitement de {pkg_identifier}")

        try:
            result = subprocess.run(
                ["npm", "pack", pkg_identifier, "--pack-destination", out_dir],
                check=True,
                text=True
            )
            filename = f"{pkg_identifier.replace('/', '-')}-{version}.tgz"
            full_tgz_path = os.path.join(out_dir, filename)

            if os.path.exists(full_tgz_path):
                sanitize_package(full_tgz_path)

            already_dl.add(package_name)
            print(f"[SUCCESS] {pkg_identifier} téléchargé et nettoyé")

        except subprocess.CalledProcessError as e:
            print(f"[ERROR] npm pack pour {pkg_identifier} échoué: {e}")
        except Exception as e:
            print(f"[ERROR] Erreur inattendue pour {pkg_identifier}: {e}")

    with open(os.path.join(out_dir, "signature.key"), "w") as key_file:
        key_file.write(SIGNATURE_VALUE)

    print("[INFO] Création de l'archive finale packages_npm.tar.gz...")
    subprocess.run(["tar", "czf", "packages_npm.tar.gz", out_dir], check=True)

    try:
        shutil.move("packages_npm.tar.gz", "/out/packages_npm.tar.gz")
        print("[SUCCESS] Archive déplacée vers /out/packages_npm.tar.gz")
    except Exception as e:
        print(f"[WARN] Impossible de déplacer vers /out (peut-être en local?): {e}")


if __name__ == "__main__":
    package_lock_file_path = "./package-lock.json"
    get_dependencies(package_lock_file_path)
