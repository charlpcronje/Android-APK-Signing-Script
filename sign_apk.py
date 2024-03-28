import argparse
import json
import os
import subprocess
import shutil
from datetime import datetime

def sign_apk(app_name, new_config=False):
    config_file = f"{app_name}.sign.json"

    if new_config:
        create_new_config(app_name)

    with open(config_file, "r") as file:
        config = json.load(file)

    app_path = config["app_path"]
    keystore_file = config["keystore_file"]
    keystore_password = config["keystore_password"]
    key_alias = config["key_alias"]
    key_password = config["key_password"]

    # Determine the path to the unsigned APK
    unsigned_apk = os.path.join(app_path, "app", "build", "outputs", "apk", "release", "app-release-unsigned.apk")

    log_file = f"{app_name}.log"
    with open(log_file, "a") as log:
        log.write(f"Starting APK signing process for {app_name}\n")
        log.write(f"Timestamp: {datetime.now()}\n\n")

        # Navigate to the app directory
        os.chdir(app_path)
        log_and_print(log, f"Navigating to app directory: {app_path}")
        pause_and_confirm(log, "Press Enter to continue...")

        # Sign the APK
        log_and_print(log, "Signing the APK...")
        sign_command = [
            "jarsigner",
            "-verbose",
            "-sigalg", "SHA1withRSA",
            "-digestalg", "SHA1",
            "-keystore", keystore_file,
            "-storepass", keystore_password,
            "-keypass", key_password,
            unsigned_apk,
            key_alias
        ]
        subprocess.run(sign_command, check=True)
        log_and_print(log, "APK signed successfully.")
        pause_and_confirm(log, "Press Enter to continue...")

        # Prompt the user for the signed APK name
        signed_apk_name = input("Enter a name for the signed APK: ")
        signed_apk = os.path.join(os.path.dirname(os.path.abspath(__file__)), signed_apk_name)

        # Align and copy the signed APK
        log_and_print(log, "Aligning and copying the signed APK...")
        align_command = [
            "zipalign",
            "-v", "4",
            unsigned_apk,
            signed_apk
        ]
        subprocess.run(align_command, check=True)
        log_and_print(log, f"APK aligned and copied successfully. Path: {signed_apk}")
        pause_and_confirm(log, "Press Enter to continue...")

        log.write("\n")

    # Print instructions for adding signing configuration to build.gradle
    print_gradle_instructions(log, config)

def create_new_config(app_name):
    config_file = f"{app_name}.sign.json"

    app_path = input("Enter the path to the app directory: ")
    keystore_file = input("Enter the path to the keystore file: ")
    keystore_password = input("Enter the keystore password: ")
    key_alias = input("Enter the key alias: ")
    key_password = input("Enter the key password: ")

    config = {
        "app_path": app_path,
        "keystore_file": keystore_file,
        "keystore_password": keystore_password,
        "key_alias": key_alias,
        "key_password": key_password
    }

    with open(config_file, "w") as file:
        json.dump(config, file, indent=2)

    print(f"New configuration file created: {config_file}")

def log_and_print(log, message):
    log.write(message + "\n")
    print(message)

def pause_and_confirm(log, message):
    input(message)
    log.write(message + "\n")

def print_gradle_instructions(log, config):
    keystore_file = config["keystore_file"]
    keystore_password = config["keystore_password"]
    key_alias = config["key_alias"]
    key_password = config["key_password"]

    log_and_print(log, "\nInstructions for adding signing configuration to build.gradle:")
    log_and_print(log, "1. Open the build.gradle file in your Android app module.")
    log_and_print(log, "   - Typically located at: app/build.gradle")
    log_and_print(log, "2. Add the following signing configuration block within the android block:")
    log_and_print(log, """
    signingConfigs {
        release {
            storeFile file('{}')
            storePassword '{}'
            keyAlias '{}'
            keyPassword '{}'
        }
    }
    """.format(keystore_file, keystore_password, key_alias, key_password))
    log_and_print(log, "3. In the buildTypes block, add the signingConfig property to the release block:")
    log_and_print(log, """
    buildTypes {
        release {
            // ...
            signingConfig signingConfigs.release
        }
    }
    """)
    log_and_print(log, "4. Save the build.gradle file.")
    log_and_print(log, "\nAfter adding the signing configuration, you can build a signed APK using Android Studio or the command line.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sign an Android APK")
    parser.add_argument("app_name", help="Name of the app")
    parser.add_argument("--new", action="store_true", help="Create a new configuration file")
    args = parser.parse_args()

    sign_apk(args.app_name, args.new)