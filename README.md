# Android APK Signing Script

This Python script automates the process of signing an Android APK (Android Package) using a configuration file. It provides a convenient way to sign your APK with a keystore and generate a signed APK ready for distribution.

## Features

- Automates the APK signing process using a configuration file
- Supports creating a new configuration file with user-provided information
- Guides the user through each step of the signing process
- Logs the signing process and prints output to the terminal
- Provides instructions for adding the signing configuration to the `build.gradle` file

## Prerequisites

Before using this script, ensure that you have the following:

- Python 3.x installed on your system
- Android SDK installed and configured
- Java Development Kit (JDK) installed
- `jarsigner` and `zipalign` tools available in your system's PATH

## Usage

1. Clone the repository or download the script file to your local machine.
```sh
git clone git@github.com:charlpcronje/Android-APK-Signing-Script.git
cd Android-APK-Signing-Script
```
2. Run the script with the following command:
```sh
python sign_apk.py {app_name}
```
Replace `{app_name}` with the name of your app (without the `.sign.json` extension).

If you want to create a new configuration file, run the script with the `--new` flag:
```sh
python sign_apk.py {app_name} --new
```
The script will prompt you to enter the necessary information for the configuration file.

3. Follow the prompts and wait for the script to complete the signing process.
4. The script will log the entire signing process in the `{app_name}.log` file and print the output to the terminal.
5. The signed APK will be copied to the script's directory with the new name provided by the user.
6. At the end of the script, instructions will be provided on how to add the signing configuration to the `build.gradle` file.

## Configuration File

The configuration file (`{app_name}.sign.json`) contains the necessary information for signing the APK. It includes the following fields:

- `app_path`: Path to the app directory (e.g., the `android` directory of your project)
- `keystore_file`: Path to the keystore file relative to the app directory
- `keystore_password`: Password for the keystore
- `key_alias`: Alias of the key used for signing
- `key_password`: Password for the key

- **Example config file**

```json
{
  "app_path": "/path/to/your/android/project",
  "keystore_file": "/path/to/your/keystore/file.keystore",
  "keystore_password": "yourKeystorePassword",
  "key_alias": "yourKeyAlias",
  "key_password": "yourKeyPassword"
}
```

If you run the script with the `--new` flag, it will prompt you to enter the values for each field and create a new configuration file.

## Adding Signing Configuration to build.gradle

After signing the APK, the script provides instructions on how to add the signing configuration to the `build.gradle` file. Follow these steps:

1. Open the `build.gradle` file in your Android app module (typically located at `app/build.gradle`).

2. Add the signing configuration block within the `android` block, using the values from the configuration file:
   ```groovy
   signingConfigs {
       release {
           storeFile file('path/to/keystore.jks')
           storePassword 'keystore_password'
           keyAlias 'key_alias'
           keyPassword 'key_password'
       }
   }
   ```

3. In the `buildTypes` block, add the `signingConfig` property to the `release` block:
   ```groovy
   buildTypes {
       release {
           // ...
           signingConfig signingConfigs.release
       }
   }
   ```

4. Save the `build.gradle` file.

After adding the signing configuration, you can build a signed APK using Android Studio or the command line.

## Troubleshooting

If you encounter any issues while using the script, consider the following:

- Ensure that you have the necessary prerequisites installed and configured correctly.
- Double-check the paths provided in the configuration file and ensure they are correct.
- Verify that the keystore file and passwords are valid.
- Check the log file (`{app_name}.log`) for any error messages or additional information.

If you still face problems, please open an issue on the GitHub repository or contact the script author for assistance.

## Acknowledgements

This script was created by `Charl Cronje` and is based on the Android APK signing process described in the official Android documentation.

## Contact
For any questions or inquiries, please contact `Charl Cronje` at `charl@webally.co.za`