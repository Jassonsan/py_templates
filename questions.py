"""
Question handler module for collecting user preferences.
"""


class QuestionHandler:
    """Handles interactive questions for template generation."""
    
    def __init__(self):
        self.preferences = {}
    
    def _ask_yes_no(self, question: str, default: bool = True) -> bool:
        """Ask a yes/no question and return boolean."""
        default_str = "Y/n" if default else "y/N"
        response = input(f"{question} ({default_str}): ").strip().lower()
        
        if not response:
            return default
        
        return response in ['y', 'yes']
    
    def _ask_choice(self, question: str, choices: list, default: int = 0) -> str:
        """Ask user to choose from a list of options."""
        print(f"\n{question}")
        for i, choice in enumerate(choices, 1):
            marker = "→" if i == default + 1 else " "
            print(f"  {marker} {i}. {choice}")
        
        while True:
            try:
                response = input(f"\nSelect option (1-{len(choices)}, default: {default + 1}): ").strip()
                
                if not response:
                    return choices[default]
                
                choice_num = int(response)
                if 1 <= choice_num <= len(choices):
                    return choices[choice_num - 1]
                else:
                    print(f"Please enter a number between 1 and {len(choices)}")
            except ValueError:
                print("Please enter a valid number")
    
    def collect_preferences(self) -> dict:
        """Collect all user preferences through interactive questions."""
        # First ask for platform/framework
        platform = self._ask_choice(
            "What platform/framework are you building for?",
            ["Flutter (Cross-platform)", "macOS (Native Swift/SwiftUI)"],
            default=0
        )
        self.preferences['platform'] = platform.lower()
        
        if 'macos' in platform.lower():
            # macOS-specific questions
            return self._collect_macos_preferences()
        else:
            # Flutter-specific questions
            return self._collect_flutter_preferences()
    
    def _collect_macos_preferences(self) -> dict:
        """Collect preferences for macOS native apps."""
        print("Let's configure your macOS app template...\n")
        
        # App type
        app_category = self._ask_choice(
            "What type of app are you building?",
            ["Desktop App", "Menu Bar App", "Command Line Tool"],
            default=0
        )
        self.preferences['app_category'] = app_category.lower()
        
        # UI Framework
        ui_framework = self._ask_choice(
            "Which UI framework?",
            ["SwiftUI", "AppKit"],
            default=0
        )
        self.preferences['ui_framework'] = ui_framework.lower()
        
        # Authentication
        has_auth = self._ask_yes_no("Does your app require authentication?", default=False)
        self.preferences['has_auth'] = has_auth
        
        if has_auth:
            auth_provider = self._ask_choice(
                "Which authentication method?",
                ["Keychain", "OAuth", "Custom"],
                default=0
            )
            self.preferences['auth_provider'] = auth_provider.lower()
        else:
            self.preferences['auth_provider'] = None
        
        # Database
        database_choice = self._ask_choice(
            "Which database would you like to use?",
            ["Core Data", "SQLite", "Realm", "None"],
            default=0
        )
        self.preferences['database'] = database_choice.lower().replace(' ', '_')
        
        # Additional features
        print("\nAdditional features:")
        self.preferences['has_menu_bar'] = self._ask_yes_no("  Include menu bar?", default=True)
        self.preferences['has_dock_icon'] = self._ask_yes_no("  Show dock icon?", default=True)
        self.preferences['has_notifications'] = self._ask_yes_no("  Include notifications?", default=False)
        self.preferences['has_file_access'] = self._ask_yes_no("  Include file system access?", default=False)
        
        self.preferences['app_type'] = 'macos'
        return self.preferences
    
    def _collect_flutter_preferences(self) -> dict:
        """Collect preferences for Flutter apps."""
        print("Let's configure your Flutter app template...\n")
        
        # App type (game or transactional)
        app_category = self._ask_choice(
            "What type of app are you building?",
            ["Game", "Transactional App"],
            default=1
        )
        self.preferences['app_category'] = app_category.lower()
        
        # Authentication
        has_auth = self._ask_yes_no("Does your app require authentication?", default=True)
        self.preferences['has_auth'] = has_auth
        
        auth_provider = None
        if has_auth:
            auth_provider = self._ask_choice(
                "Which authentication method would you like to use?",
                ["Firebase Auth", "Custom Auth (REST API)", "Local Auth (Biometric)"],
                default=0
            )
        self.preferences['auth_provider'] = auth_provider.lower().replace(' ', '_') if auth_provider else None
        
        # Database
        database_choice = self._ask_choice(
            "Which database would you like to use?",
            ["Firebase Firestore", "SQLite", "REST API (No local DB)", "None"],
            default=0
        )
        self.preferences['database'] = database_choice.lower().replace(' ', '_')
        
        # State management
        print("\n" + "=" * 60)
        print("State Management Explanation:")
        print("=" * 60)
        print("State management helps you manage data that changes in your app.")
        print("For example: user login status, shopping cart items, game scores, etc.")
        print("\nQuick guide:")
        print("  • Provider: Simple, recommended for beginners (official Flutter)")
        print("  • Riverpod: Modern, type-safe, great for larger apps")
        print("  • Bloc: Pattern-based, good for complex business logic")
        print("  • GetX: All-in-one solution, very popular")
        print("  • Redux: Predictable state container, from web development")
        print("=" * 60)
        state_management = self._ask_choice(
            "Which state management solution would you like to use?",
            ["Provider (Recommended for beginners)", "Riverpod (Modern & type-safe)", "Bloc (Pattern-based)", "GetX (All-in-one)", "Redux (Predictable)"],
            default=0
        )
        # Extract the actual name (remove description in parentheses)
        state_mgmt_name = state_management.split('(')[0].strip().lower()
        self.preferences['state_management'] = state_mgmt_name
        
        # Additional features
        print("\nAdditional features:")
        
        # Context-aware routing explanation
        if self.preferences['app_category'] == 'game':
            print("\n" + "-" * 60)
            print("Routing/Navigation for Games:")
            print("-" * 60)
            print("Routing helps you navigate between different screens:")
            print("  ✓ Main Menu → Game Screen → Game Over → Settings")
            print("  ✓ Level Selection → Game → Pause Menu")
            print("  ✓ Leaderboard, Shop, Profile screens")
            print("\nWithout routing: You'd manage all screens manually")
            print("With routing: Clean navigation between screens")
            print("\nSimple single-screen games might not need routing.")
            print("Games with menus, levels, or multiple screens benefit from it.")
            print("-" * 60)
            self.preferences['has_routing'] = self._ask_yes_no("  Use routing/navigation?", default=True)
        else:
            print("\nRouting/Navigation: Helps navigate between screens")
            print("  (e.g., Login → Home → Profile → Settings)")
            self.preferences['has_routing'] = self._ask_yes_no("  Use routing/navigation?", default=True)
        self.preferences['has_localization'] = self._ask_yes_no("  Include localization (i18n)?", default=False)
        self.preferences['has_theme'] = self._ask_yes_no("  Include theme management (dark/light mode)?", default=True)
        self.preferences['has_analytics'] = self._ask_yes_no("  Include analytics?", default=False)
        self.preferences['has_crash_reporting'] = self._ask_yes_no("  Include crash reporting?", default=False)
        
        # Game-specific questions
        if self.preferences['app_category'] == 'game':
            self.preferences['game_engine'] = self._ask_choice(
                "Which game engine/framework?",
                ["Flame", "Unity (via flutter_unity_widget)", "Custom Canvas"],
                default=0
            )
            self.preferences['has_multiplayer'] = self._ask_yes_no("  Support multiplayer?", default=False)
            
            if self.preferences['has_multiplayer']:
                multiplayer_type = self._ask_choice(
                    "What type of multiplayer?",
                    ["Peer-to-Peer (P2P) - No server needed", "Online (requires server)"],
                    default=0
                )
                self.preferences['multiplayer_type'] = 'p2p' if 'peer' in multiplayer_type.lower() else 'online'
                
                if self.preferences['multiplayer_type'] == 'p2p':
                    print("\n" + "=" * 60)
                    print("P2P Library Selection:")
                    print("=" * 60)
                    print("For long-distance play (over internet):")
                    print("  → peerdart (WebRTC) - Works worldwide, recommended!")
                    print("\nFor local play only (same WiFi/Bluetooth):")
                    print("  → flutter_nearby_connections - Local network only")
                    print("\nFor advanced low-latency games:")
                    print("  → ENet Dart - Requires server setup")
                    print("=" * 60)
                    p2p_library = self._ask_choice(
                        "Which P2P library? (Choose peerdart for long-distance)",
                        ["peerdart (WebRTC - Works over internet, recommended)", "flutter_nearby_connections (Local WiFi/Bluetooth only)", "ENet Dart (UDP - Advanced, needs server)"],
                        default=0
                    )
                    # Extract library name
                    lib_name = p2p_library.lower().split('(')[0].strip().replace(' ', '_')
                    self.preferences['p2p_library'] = lib_name
                    
                    # Add note about signaling for peerdart
                    if lib_name == 'peerdart':
                        print("\n" + "⚠️  Note: peerdart (WebRTC) may need a signaling server")
                        print("   for initial connection setup. You can use free services")
                        print("   like PeerJS cloud or set up your own simple server.")
                        print("   The generated code includes basic P2P setup.")
            else:
                self.preferences['multiplayer_type'] = None
                self.preferences['p2p_library'] = None
        
        # Transactional app-specific questions
        if self.preferences['app_category'] == 'transactional app':
            self.preferences['has_payments'] = self._ask_yes_no("  Include payment integration?", default=False)
            self.preferences['has_notifications'] = self._ask_yes_no("  Include push notifications?", default=True)
            self.preferences['has_offline_mode'] = self._ask_yes_no("  Support offline mode?", default=True)
        
        # App type identifier for generator
        self.preferences['app_type'] = 'flutter'
        
        return self.preferences

