# Minecraft-Mod-Folder-Modifier

If you play Minecraft with mods on different versions using the same .minecraft folder and don’t use CurseForge or other unofficial launchers, you know how tedious it is to switch mods depending on the version. That’s why I created this program: to switch the mods folder according to the version you want to play, with just two clicks.

### How to use it:
Before running it, you'll need to prepare a couple of things:

-   Place the executable in the `.minecraft` folder so it can function correctly. If you want, you can create a shortcut for easier access.
-   You’ll need to create several folders inside the `.minecraft` folder. One main folder called `mods_versions` (it must be named exactly this). Inside this folder, you’ll create a subfolder for each version you want to play. For example: if you want to play with mods in version 1.19.2, you’ll need to create a folder inside `mods_versions` named "1.19.2". In this folder, you can add all the mods you would normally place in the original `mods` folder. (You can also have other files and subfolders; only `.jar` files will be considered).

Now, you can run the program. It will open a small window with a list of buttons for "Fabric" or "Forge" profiles, followed by their versions. Click the one you need, and the content of the version matching that profile will be moved to the original `mods` folder. If you want to check how the execution went, a `.log` file will be created in the same folder where the executable is located.

### Unleash its maximum power 
By the way, the real need for this program was to run two active instances simultaneously with different versions and mods on the same `.minecraft` folder, which is not trivial. To achieve this, you must first open Minecraft with the older version and its mods. Then, use the **ModFolderModifier** program to select the mods for the latest version. When you launch the game again with the other Fabric or Forge profile, it will warn you that it’s already running. You will click "I understand the risks," and it will start opening. Don’t worry if there are mod incompatibilities. To fix this, I recommend using the same name for common mods between both instances. If that doesn’t work, you’ll need to check which version the mods are compatible with. If they are compatible with common versions (for example, a mod for 1.19 is compatible with 1.19.x, and the 1.19.3 version is marked as compatible for >= 1.19.2), you might get an error, and you’ll need to modify the version directly in the mod. Some mods may not work even after changing that, and that's normal. Keep in mind that this is not something planned by Mojang or mod creators. You’ll need to remove those mods. Once you bypass the compatibility issues, you’ll have successfully run two instances on different versions with mods on the same `.minecraft` folder.

**Why use this?**  
Believe it or not, when investigating bugs between versions or designing machines and farms that work across different versions, it helps a lot since you don’t have to keep opening and closing the game after each change.

**How will I use this program?**  
For most players, having to switch mod versions is tedious, especially if you play regularly between different versions. Being able to change mod versions with just 2 clicks is very convenient.

### How the code works:
The program will search for the `launcher_profiles.json` file to identify the existing Fabric or Forge profiles. Then, it will open a small window to show you all the options. Once you select a profile, it will check if there is a folder named after the version of the selected profile. If such a folder exists, it will overwrite the contents of the `mods` folder with the contents of the "1.19.2" folder inside `mods_versions`, provided you have chosen a profile for that version.
