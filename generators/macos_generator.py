"""
macOS native app template generator.
"""

import os
from pathlib import Path
from typing import Dict, Any


class MacOSTemplateGenerator:
    """Generates macOS native app templates based on preferences."""
    
    def __init__(self, preferences: Dict[str, Any], project_name: str, output_path: Path):
        self.preferences = preferences
        self.project_name = project_name
        self.output_path = Path(output_path)
        self.app_category = preferences.get('app_category', 'desktop app')
        self.ui_framework = preferences.get('ui_framework', 'swiftui')
    
    def generate(self):
        """Generate the complete macOS template."""
        # Create directory structure
        self._create_directory_structure()
        
        # Generate Xcode project files
        self._generate_xcode_project()
        
        # Generate Swift source files
        self._generate_swift_files()
        
        # Generate configuration files
        self._generate_config_files()
        
        # Generate README
        self._generate_readme()
    
    def _create_directory_structure(self):
        """Create the macOS project directory structure."""
        # Create main project directory
        project_dir = self.output_path / self.project_name
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Create source directories
        source_dirs = [
            'Views',
            'Models',
            'ViewModels',
            'Services',
            'Utils',
            'Resources',
        ]
        
        for dir_name in source_dirs:
            (project_dir / dir_name).mkdir(parents=True, exist_ok=True)
        
        if self.preferences.get('has_auth', False):
            (project_dir / 'Auth').mkdir(parents=True, exist_ok=True)
        
        if self.preferences.get('database') != 'none':
            (project_dir / 'Data').mkdir(parents=True, exist_ok=True)
        
        # Create Xcode project directory
        (project_dir / f'{self.project_name}.xcodeproj').mkdir(parents=True, exist_ok=True)
    
    def _generate_xcode_project(self):
        """Generate basic Xcode project structure."""
        project_name = self.project_name
        bundle_id = f"com.example.{project_name.lower().replace(' ', '')}"
        
        # Generate Info.plist
        info_plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>$(DEVELOPMENT_LANGUAGE)</string>
    <key>CFBundleDisplayName</key>
    <string>{project_name}</string>
    <key>CFBundleExecutable</key>
    <string>$(EXECUTABLE_NAME)</string>
    <key>CFBundleIdentifier</key>
    <string>{bundle_id}</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>$(PRODUCT_NAME)</string>
    <key>CFBundlePackageType</key>
    <string>$(PRODUCT_BUNDLE_PACKAGE_TYPE)</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSMinimumSystemVersion</key>
    <string>$(MACOSX_DEPLOYMENT_TARGET)</string>
    <key>NSHumanReadableCopyright</key>
    <string>Copyright © 2024. All rights reserved.</string>
    <key>NSMainStoryboardFile</key>
    <string>Main</string>
    <key>NSPrincipalClass</key>
    <string>NSApplication</string>
"""
        
        if not self.preferences.get('has_dock_icon', True):
            info_plist += """    <key>LSUIElement</key>
    <true/>
"""
        
        if self.preferences.get('has_file_access', False):
            info_plist += """    <key>NSDocumentsFolderUsageDescription</key>
    <string>This app needs access to your documents folder.</string>
    <key>NSDownloadsFolderUsageDescription</key>
    <string>This app needs access to your downloads folder.</string>
"""
        
        info_plist += """</dict>
</plist>
"""
        
        (self.output_path / self.project_name / 'Info.plist').write_text(info_plist)
        
        # Generate basic project.pbxproj structure (simplified)
        # Note: Full Xcode project generation is complex, this is a basic structure
        project_pbxproj = f"""// !$*UTF8*$!
{{
    archiveVersion = 1;
    classes = {{
    }};
    objectVersion = 56;
    objects = {{
    }};
    rootObject = /* Project object */;
}}
"""
        # For a complete Xcode project, you'd need a full pbxproj file
        # This is a placeholder - users will need to create the project in Xcode
        (self.output_path / self.project_name / f'{self.project_name}.xcodeproj/project.pbxproj').write_text(project_pbxproj)
    
    def _generate_swift_files(self):
        """Generate Swift source files."""
        project_name = self.project_name
        
        if self.ui_framework == 'swiftui':
            self._generate_swiftui_app(project_name)
        else:
            self._generate_appkit_app(project_name)
        
        # Generate ContentView
        self._generate_content_view()
        
        # Generate services if needed
        if self.preferences.get('has_auth', False):
            self._generate_auth_service()
        
        if self.preferences.get('database') != 'none':
            self._generate_database_service()
    
    def _generate_swiftui_app(self, project_name: str):
        """Generate SwiftUI App file."""
        app_content = f"""import SwiftUI

@main
struct {project_name.replace(' ', '')}App: App {{
"""
        
        if self.preferences.get('has_menu_bar', True):
            app_content += """    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
"""
        
        app_content += f"""    var body: some Scene {{
"""
        
        if self.app_category == 'menu bar app':
            app_content += """        MenuBarExtra("App", systemImage: "star") {
            ContentView()
        }
        .menuBarExtraStyle(.window)
"""
        else:
            app_content += f"""        WindowGroup {{
            ContentView()
        }}
        .windowStyle(.automatic)
"""
        
        if self.preferences.get('has_menu_bar', True):
            app_content += """
        Settings {
            SettingsView()
        }
"""
        
        app_content += """    }
}
"""
        
        (self.output_path / self.project_name / f'{project_name.replace(" ", "")}App.swift').write_text(app_content)
        
        # Generate AppDelegate if menu bar is enabled
        if self.preferences.get('has_menu_bar', True):
            app_delegate = """import AppKit
import SwiftUI

class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        // Configure app delegate here
    }
    
    func applicationWillTerminate(_ notification: Notification) {
        // Cleanup code here
    }
    
    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        return true
    }
}
"""
            (self.output_path / self.project_name / 'AppDelegate.swift').write_text(app_delegate)
    
    def _generate_appkit_app(self, project_name: str):
        """Generate AppKit App file."""
        app_content = f"""import Cocoa

@main
class AppDelegate: NSObject, NSApplicationDelegate {{
    var window: NSWindow!
    
    func applicationDidFinishLaunching(_ aNotification: Notification) {{
        // Create the window
        let contentRect = NSRect(x: 0, y: 0, width: 800, height: 600)
        let windowStyle: NSWindow.StyleMask = [.titled, .closable, .miniaturizable, .resizable]
        
        window = NSWindow(
            contentRect: contentRect,
            styleMask: windowStyle,
            backing: .buffered,
            defer: false
        )
        
        window.title = "{project_name}"
        window.center()
        window.makeKeyAndOrderFront(nil)
        
        // Set content view
        let contentView = ContentView()
        window.contentView = NSHostingView(rootView: contentView)
    }}
    
    func applicationWillTerminate(_ aNotification: Notification) {{
        // Insert code here to tear down your application
    }}
    
    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {{
        return true
    }}
}}
"""
        (self.output_path / self.project_name / 'AppDelegate.swift').write_text(app_content)
    
    def _generate_content_view(self):
        """Generate ContentView."""
        if self.ui_framework == 'swiftui':
            content_view = """import SwiftUI

struct ContentView: View {
    @State private var counter = 0
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Welcome to your macOS app!")
                .font(.largeTitle)
                .padding()
            
            Text("Counter: \\(counter)")
                .font(.title2)
            
            HStack(spacing: 20) {
                Button("Decrement") {
                    counter -= 1
                }
                .buttonStyle(.bordered)
                
                Button("Increment") {
                    counter += 1
                }
                .buttonStyle(.borderedProminent)
            }
            
            Text("Start building your app from here.")
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .frame(minWidth: 400, minHeight: 300)
        .padding()
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
"""
        else:
            content_view = """import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack {
            Text("Welcome to your macOS AppKit app!")
                .font(.largeTitle)
                .padding()
            
            Text("Start building your app from here.")
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .frame(minWidth: 400, minHeight: 300)
        .padding()
    }
}
"""
        
        (self.output_path / self.project_name / 'Views/ContentView.swift').write_text(content_view)
        
        # Generate SettingsView if menu bar is enabled
        if self.preferences.get('has_menu_bar', True) and self.ui_framework == 'swiftui':
            settings_view = """import SwiftUI

struct SettingsView: View {
    @AppStorage("showNotifications") private var showNotifications = true
    
    var body: some View {
        Form {
            Toggle("Show Notifications", isOn: $showNotifications)
        }
        .padding()
        .frame(width: 400, height: 200)
    }
}
"""
            (self.output_path / self.project_name / 'Views/SettingsView.swift').write_text(settings_view)
    
    def _generate_auth_service(self):
        """Generate authentication service."""
        auth_provider = self.preferences.get('auth_provider', 'keychain')
        
        if auth_provider == 'keychain':
            auth_service = """import Foundation
import Security

class AuthService {
    private let service = "com.example.app"
    
    func saveCredentials(username: String, password: String) -> Bool {
        let passwordData = password.data(using: .utf8)!
        
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: username,
            kSecValueData as String: passwordData
        ]
        
        SecItemDelete(query as CFDictionary)
        let status = SecItemAdd(query as CFDictionary, nil)
        return status == errSecSuccess
    }
    
    func getCredentials(username: String) -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: username,
            kSecReturnData as String: true
        ]
        
        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)
        
        if status == errSecSuccess,
           let data = result as? Data,
           let password = String(data: data, encoding: .utf8) {
            return password
        }
        return nil
    }
    
    func deleteCredentials(username: String) -> Bool {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: username
        ]
        
        let status = SecItemDelete(query as CFDictionary)
        return status == errSecSuccess
    }
}
"""
        else:
            auth_service = """import Foundation

class AuthService {
    // TODO: Implement your authentication logic here
    
    func login(username: String, password: String) async throws -> Bool {
        // Implement login logic
        return false
    }
    
    func logout() {
        // Implement logout logic
    }
    
    var isAuthenticated: Bool {
        // Check authentication state
        return false
    }
}
"""
        
        (self.output_path / self.project_name / 'Auth/AuthService.swift').write_text(auth_service)
    
    def _generate_database_service(self):
        """Generate database service."""
        database = self.preferences.get('database', 'core_data')
        
        if database == 'core_data':
            db_service = """import CoreData
import Foundation

class DatabaseService {
    static let shared = DatabaseService()
    
    lazy var persistentContainer: NSPersistentContainer = {
        let container = NSPersistentContainer(name: "DataModel")
        container.loadPersistentStores { description, error in
            if let error = error {
                fatalError("Core Data store failed to load: \\(error.localizedDescription)")
            }
        }
        return container
    }()
    
    var viewContext: NSManagedObjectContext {
        return persistentContainer.viewContext
    }
    
    func save() {
        let context = persistentContainer.viewContext
        if context.hasChanges {
            do {
                try context.save()
            } catch {
                print("Error saving context: \\(error)")
            }
        }
    }
}
"""
        elif database == 'sqlite':
            db_service = """import Foundation
import SQLite3

class DatabaseService {
    private var db: OpaquePointer?
    private let dbPath: String
    
    init() {
        let fileManager = FileManager.default
        let urls = fileManager.urls(for: .documentDirectory, in: .userDomainMask)
        let dbURL = urls.first!.appendingPathComponent("app.db")
        dbPath = dbURL.path
        
        if sqlite3_open(dbPath, &db) != SQLITE_OK {
            print("Unable to open database")
        } else {
            createTable()
        }
    }
    
    private func createTable() {
        // TODO: Create your tables here
        // Example:
        // let createTableSQL = \"\"\"
        //     CREATE TABLE IF NOT EXISTS items (
        //         id INTEGER PRIMARY KEY AUTOINCREMENT,
        //         name TEXT NOT NULL
        //     );
        //     \"\"\"
        // sqlite3_exec(db, createTableSQL, nil, nil, nil)
    }
    
    deinit {
        sqlite3_close(db)
    }
}
"""
        else:
            db_service = """import Foundation

class DatabaseService {
    // TODO: Implement your database logic here
}
"""
        
        (self.output_path / self.project_name / 'Services/DatabaseService.swift').write_text(db_service)
    
    def _generate_config_files(self):
        """Generate configuration files."""
        # .gitignore
        gitignore = """# Xcode
#
# gitignore contributors: remember to update Global/Xcode.gitignore, Objective-C.gitignore & Swift.gitignore

## User settings
xcuserdata/

## compatibility with Xcode 8 and earlier (ignoring not required starting Xcode 9)
*.xcscmblueprint
*.xccheckout

## compatibility with Xcode 3 and earlier (ignoring not required starting Xcode 4)
build/
DerivedData/
*.moved-aside
*.pbxuser
!default.pbxuser
*.mode1v3
!default.mode1v3
*.mode2v3
!default.mode2v3
*.perspectivev3
!default.perspectivev3

## Obj-C/Swift specific
*.hmap

## App packaging
*.ipa
*.dSYM.zip
*.dSYM

## Playgrounds
timeline.xctimeline
playground.xcworkspace

# Swift Package Manager
#
# Add this line if you want to avoid checking in source code from Swift Package Manager dependencies.
# Packages/
# Package.pins
# Package.resolved
# *.xcodeproj
#
# Xcode automatically generates this directory with a .xcworkspacedata file and xcuserdata
# hence it is not needed unless you have added a package configuration file to your project
# .swiftpm

.build/

# CocoaPods
#
# We recommend against adding the Pods directory to your .gitignore. However
# you should judge for yourself, the pros and cons are mentioned at:
# https://guides.cocoapods.org/using/using-cocoapods.html#should-i-check-the-pods-directory-into-source-control
#
# Pods/
#
# Add this line if you want to avoid checking in source code from the Xcode workspace
# *.xcworkspace

# Carthage
#
# Add this line if you want to avoid checking in source code from Carthage dependencies.
# Carthage/Checkouts

Carthage/Build/

# Accio dependency management
Dependencies/
.accio/

# fastlane
#
# It is recommended to not store the screenshots in the git repo.
# Instead, use fastlane to re-generate the screenshots whenever they are needed.
# For more information about the recommended setup visit:
# https://docs.fastlane.tools/best-practices/source-control/#source-control

fastlane/report.xml
fastlane/Preview.html
fastlane/screenshots/**/*.png
fastlane/test_output

# Code Injection
#
# After new code Injection tools there's a generated folder /iOSInjectionProject
# https://github.com/johnno1962/injectionforxcode

iOSInjectionProject/

# macOS
.DS_Store
.AppleDouble
.LSOverride

# Thumbnails
._*

# Files that might appear in the root of a volume
.DocumentRevisions-V100
.fseventsd
.Spotlight-V100
.TemporaryItems
.Trashes
.VolumeIcon.icns
.com.apple.timemachine.donotpresent

# Directories potentially created on remote AFP share
.AppleDB
.AppleDesktop
Network Trash Folder
Temporary Items
.apdisk
"""
        (self.output_path / self.project_name / '.gitignore').write_text(gitignore)
    
    def _generate_readme(self):
        """Generate README.md file."""
        project_name = self.project_name
        ui_framework = self.preferences.get('ui_framework', 'swiftui').upper()
        app_category = self.preferences.get('app_category', 'desktop app').title()
        
        readme = f"""# {project_name}

A macOS native app template generated with Template Generator.

## Features

- **Platform**: macOS Native
- **UI Framework**: {ui_framework}
- **App Type**: {app_category}
- **Database**: {self.preferences.get('database', 'none').replace('_', ' ').title()}
- **Authentication**: {'Yes' if self.preferences.get('has_auth', False) else 'No'}

## Getting Started

### Prerequisites

- macOS 11.0 or later
- Xcode 14.0 or later
- Swift 5.7 or later

### Setup

1. Open the project in Xcode:
   ```bash
   open {project_name}/{project_name}.xcodeproj
   ```

2. Configure your bundle identifier in the project settings

3. Build and run:
   - Press `Cmd + R` in Xcode, or
   - Use Product > Run from the menu

## Project Structure

```
{project_name}/
├── {project_name}/
│   ├── Views/          # SwiftUI views
│   ├── Models/         # Data models
│   ├── ViewModels/     # View models (MVVM)
│   ├── Services/       # Business logic services
│   ├── Auth/           # Authentication logic
│   ├── Data/           # Database/data layer
│   └── Utils/          # Utility functions
└── {project_name}.xcodeproj/
```

## Configuration

### Bundle Identifier

Update the bundle identifier in `Info.plist` to match your organization:
```
com.example.{project_name.lower().replace(' ', '')}
```

### Database Setup

{'Configure your Core Data model in Xcode' if self.preferences.get('database') == 'core_data' else 'Configure your database connection in the respective service files.'}

## Development

This template provides a solid foundation for your macOS app. Customize it according to your needs.

## License

MIT License
"""
        (self.output_path / self.project_name / 'README.md').write_text(readme)

