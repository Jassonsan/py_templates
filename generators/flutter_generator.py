"""
Flutter template generator.
"""

import os
from pathlib import Path
from typing import Dict, Any
from config import Config


class FlutterTemplateGenerator:
    """Generates Flutter app templates based on preferences."""
    
    def __init__(self, preferences: Dict[str, Any], project_name: str, output_path: Path):
        self.preferences = preferences
        self.project_name = project_name
        self.output_path = Path(output_path)
        self.app_category = preferences.get('app_category', 'transactional app')
    
    def generate(self):
        """Generate the complete Flutter template."""
        # Create directory structure
        self._create_directory_structure()
        
        # Generate pubspec.yaml
        self._generate_pubspec()
        
        # Generate main.dart
        self._generate_main_dart()
        
        # Generate app structure
        self._generate_app_structure()
        
        # Generate configuration files
        self._generate_config_files()
        
        # Generate README
        self._generate_readme()
    
    def _create_directory_structure(self):
        """Create the Flutter project directory structure."""
        directories = [
            'lib',
            'lib/models',
            'lib/services',
            'lib/repositories',
            'lib/screens',
            'lib/widgets',
            'lib/utils',
            'lib/constants',
            'test',
            'assets',
            'assets/images',
            'assets/icons',
        ]
        
        # Category-specific directories
        if self.app_category == 'game':
            directories.extend([
                'lib/game',
                'lib/game/components',
                'lib/game/systems',
                'assets/sprites',
                'assets/sounds',
            ])
        else:  # transactional app
            directories.extend([
                'lib/features',
                'lib/providers',
            ])
        
        # Auth directories
        if self.preferences.get('has_auth', False):
            directories.extend([
                'lib/auth',
                'lib/screens/auth',
            ])
        
        # Create directories
        for directory in directories:
            (self.output_path / directory).mkdir(parents=True, exist_ok=True)
    
    def _generate_pubspec(self):
        """Generate pubspec.yaml file."""
        dependencies = Config.get_dependencies(self.preferences)
        dev_dependencies = Config.get_dev_dependencies(self.preferences)
        
        # SDK packages that need 'sdk: flutter'
        sdk_packages = ['flutter_localizations']
        sdk_dev_packages = ['flutter_test']
        
        # Separate SDK packages from regular packages
        sdk_deps = [d for d in dependencies if d in sdk_packages]
        regular_deps = [d for d in dependencies if d not in sdk_packages]
        
        sdk_dev_deps = [d for d in dev_dependencies if d in sdk_dev_packages]
        regular_dev_deps = [d for d in dev_dependencies if d not in sdk_dev_packages]
        
        pubspec_content = f"""name: {self.project_name.lower().replace(' ', '_')}
description: A Flutter {self.app_category} template.
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
"""
        
        # Add SDK packages first
        for dep in sdk_deps:
            pubspec_content += f"  {dep}:\n    sdk: flutter\n"
        # Add regular packages
        for dep in regular_deps:
            pubspec_content += f"  {dep}:\n"
        
        pubspec_content += "\ndev_dependencies:\n"
        # Add SDK dev packages first
        for dep in sdk_dev_deps:
            pubspec_content += f"  {dep}:\n    sdk: flutter\n"
        # Add regular dev packages
        for dep in regular_dev_deps:
            pubspec_content += f"  {dep}:\n"
        
        pubspec_content += """
flutter:
  uses-material-design: true
  
  assets:
    - assets/images/
    - assets/icons/
"""
        
        if self.app_category == 'game':
            pubspec_content += """    - assets/sprites/
    - assets/sounds/
"""
        
        (self.output_path / 'pubspec.yaml').write_text(pubspec_content)
    
    def _generate_main_dart(self):
        """Generate main.dart file."""
        state_mgmt = self.preferences.get('state_management', 'provider')
        has_routing = self.preferences.get('has_routing', True)
        has_theme = self.preferences.get('has_theme', True)
        
        imports = ["import 'package:flutter/material.dart';"]
        
        if state_mgmt == 'provider':
            imports.append("import 'package:provider/provider.dart';")
        elif state_mgmt == 'riverpod':
            imports.append("import 'package:flutter_riverpod/flutter_riverpod.dart';")
        elif state_mgmt == 'bloc':
            imports.append("import 'package:flutter_bloc/flutter_bloc.dart';")
        
        if has_routing:
            imports.append("import 'package:go_router/go_router.dart';")
        
        imports.append("import 'screens/home_screen.dart';")
        
        if has_theme:
            imports.append("import 'utils/theme.dart';")
        
        main_content = "\n".join(imports) + "\n\n"
        
        if state_mgmt == 'riverpod':
            main_content += """void main() {
  runApp(
    const ProviderScope(
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
"""
        elif state_mgmt == 'provider':
            main_content += """void main() {
  runApp(
    MultiProvider(
      providers: [
        // Add your providers here
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
"""
        else:
            main_content += """void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
"""
        
        if has_routing:
            main_content += f"""    return MaterialApp.router(
      title: '{self.project_name}',
      debugShowCheckedModeBanner: false,
"""
            if has_theme:
                main_content += """      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system,
"""
            main_content += """      routerConfig: _router,
    );
  }
}

final GoRouter _router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
    ),
    // Add more routes here
  ],
);
"""
        else:
            main_content += f"""    return MaterialApp(
      title: '{self.project_name}',
      debugShowCheckedModeBanner: false,
"""
            if has_theme:
                main_content += """      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system,
"""
            main_content += """      home: const HomeScreen(),
    );
  }
}
"""
        
        (self.output_path / 'lib' / 'main.dart').write_text(main_content)
    
    def _generate_app_structure(self):
        """Generate app structure files."""
        # Home screen
        self._generate_home_screen()
        
        # Theme file
        if self.preferences.get('has_theme', True):
            self._generate_theme_file()
        
        # Auth files
        if self.preferences.get('has_auth', False):
            self._generate_auth_files()
        
        # Database files
        database = self.preferences.get('database', 'none')
        if database != 'none':
            self._generate_database_files(database)
        
        # Category-specific files
        if self.app_category == 'game':
            self._generate_game_files()
        else:
            self._generate_transactional_files()
    
    def _generate_home_screen(self):
        """Generate home screen."""
        content = """import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
      ),
      body: const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Welcome to your Flutter app!',
              style: TextStyle(fontSize: 24),
            ),
            SizedBox(height: 20),
            Text(
              'Start building your app from here.',
              style: TextStyle(fontSize: 16, color: Colors.grey),
            ),
          ],
        ),
      ),
    );
  }
}
"""
        (self.output_path / 'lib' / 'screens' / 'home_screen.dart').write_text(content)
    
    def _generate_theme_file(self):
        """Generate theme configuration file."""
        content = """import 'package:flutter/material.dart';

class AppTheme {
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
      appBarTheme: const AppBarTheme(
        centerTitle: true,
        elevation: 0,
      ),
    );
  }

  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: Colors.blue,
        brightness: Brightness.dark,
      ),
      appBarTheme: const AppBarTheme(
        centerTitle: true,
        elevation: 0,
      ),
    );
  }
}
"""
        (self.output_path / 'lib' / 'utils' / 'theme.dart').write_text(content)
    
    def _generate_auth_files(self):
        """Generate authentication-related files."""
        auth_provider = self.preferences.get('auth_provider', 'firebase_auth')
        
        # Auth service
        if 'firebase' in auth_provider:
            content = """import 'package:firebase_auth/firebase_auth.dart';

class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;

  Stream<User?> get authStateChanges => _auth.authStateChanges();

  Future<UserCredential?> signInWithEmailAndPassword(
    String email,
    String password,
  ) async {
    try {
      return await _auth.signInWithEmailAndPassword(
        email: email,
        password: password,
      );
    } catch (e) {
      print('Sign in error: $e');
      return null;
    }
  }

  Future<UserCredential?> signUpWithEmailAndPassword(
    String email,
    String password,
  ) async {
    try {
      return await _auth.createUserWithEmailAndPassword(
        email: email,
        password: password,
      );
    } catch (e) {
      print('Sign up error: $e');
      return null;
    }
  }

  Future<void> signOut() async {
    await _auth.signOut();
  }

  User? get currentUser => _auth.currentUser;
}
"""
        else:
            content = """class AuthService {
  // Implement your custom auth logic here
  Future<bool> signIn(String email, String password) async {
    // TODO: Implement authentication
    return false;
  }

  Future<bool> signUp(String email, String password) async {
    // TODO: Implement registration
    return false;
  }

  Future<void> signOut() async {
    // TODO: Implement sign out
  }

  bool get isAuthenticated => false; // TODO: Check auth state
}
"""
        
        (self.output_path / 'lib' / 'auth' / 'auth_service.dart').write_text(content)
        
        # Login screen
        login_screen = """import 'package:flutter/material.dart';
import '../auth/auth_service.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _authService = AuthService();
  bool _isLoading = false;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _handleLogin() async {
    if (_formKey.currentState!.validate()) {
      setState(() => _isLoading = true);
      // TODO: Implement login logic
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              TextFormField(
                controller: _emailController,
                decoration: const InputDecoration(
                  labelText: 'Email',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter your email';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _passwordController,
                obscureText: true,
                decoration: const InputDecoration(
                  labelText: 'Password',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter your password';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: _isLoading ? null : _handleLogin,
                child: _isLoading
                    ? const CircularProgressIndicator()
                    : const Text('Login'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
"""
        (self.output_path / 'lib' / 'screens' / 'auth' / 'login_screen.dart').write_text(login_screen)
    
    def _generate_database_files(self, database: str):
        """Generate database-related files."""
        if database == 'sqlite':
            content = """import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

class DatabaseService {
  static Database? _database;
  static const String _databaseName = 'app_database.db';
  static const int _databaseVersion = 1;

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    String path = join(await getDatabasesPath(), _databaseName);
    return await openDatabase(
      path,
      version: _databaseVersion,
      onCreate: _onCreate,
    );
  }

  Future<void> _onCreate(Database db, int version) async {
    // TODO: Create your tables here
    // Example:
    // await db.execute('''
    //   CREATE TABLE items (
    //     id INTEGER PRIMARY KEY AUTOINCREMENT,
    //     name TEXT NOT NULL,
    //     created_at INTEGER NOT NULL
    //   )
    // ''');
  }

  Future<void> close() async {
    final db = await database;
    await db.close();
  }
}
"""
            (self.output_path / 'lib' / 'services' / 'database_service.dart').write_text(content)
        
        elif database == 'firebase_firestore':
            content = """import 'package:cloud_firestore/cloud_firestore.dart';

class FirestoreService {
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;

  // Example: Get a collection
  Stream<QuerySnapshot> getCollection(String collectionName) {
    return _firestore.collection(collectionName).snapshots();
  }

  // Example: Add a document
  Future<void> addDocument(String collectionName, Map<String, dynamic> data) async {
    await _firestore.collection(collectionName).add(data);
  }

  // Example: Update a document
  Future<void> updateDocument(
    String collectionName,
    String documentId,
    Map<String, dynamic> data,
  ) async {
    await _firestore.collection(collectionName).doc(documentId).update(data);
  }

  // Example: Delete a document
  Future<void> deleteDocument(String collectionName, String documentId) async {
    await _firestore.collection(collectionName).doc(documentId).delete();
  }
}
"""
            (self.output_path / 'lib' / 'services' / 'firestore_service.dart').write_text(content)
    
    def _generate_game_files(self):
        """Generate game-specific files."""
        game_engine = self.preferences.get('game_engine', 'flame')
        
        if game_engine.lower() == 'flame':
            content = """import 'package:flame/game.dart';
import 'package:flutter/material.dart';

class MyGame extends FlameGame {
  @override
  Future<void> onLoad() async {
    // TODO: Initialize your game components
    super.onLoad();
  }

  @override
  void update(double dt) {
    // TODO: Update game logic
    super.update(dt);
  }

  @override
  void render(Canvas canvas) {
    // TODO: Render game elements
    super.render(canvas);
  }
}
"""
            (self.output_path / 'lib' / 'game' / 'my_game.dart').write_text(content)
        
        # Generate P2P multiplayer service if enabled
        if self.preferences.get('has_multiplayer', False) and self.preferences.get('multiplayer_type') == 'p2p':
            self._generate_p2p_service()
    
    def _generate_p2p_service(self):
        """Generate P2P multiplayer service."""
        p2p_library = self.preferences.get('p2p_library', 'flutter_nearby_connections')
        
        if p2p_library == 'flutter_nearby_connections':
            content = """import 'package:flutter_nearby_connections/flutter_nearby_connections.dart';

class P2PService {
  final FlutterNearbyConnections _nearbyConnections = FlutterNearbyConnections();
  List<Device> _devices = [];
  Device? _connectedDevice;
  bool _isAdvertising = false;
  bool _isDiscovering = false;

  // Callbacks
  Function(Device)? onDeviceFound;
  Function(Device)? onDeviceConnected;
  Function(String)? onMessageReceived;
  Function(String)? onDisconnected;

  /// Start advertising (host mode)
  Future<void> startAdvertising(String deviceName) async {
    try {
      await _nearbyConnections.startAdvertising(
        deviceName,
        strategy: Strategy.P2P_STAR,
        onConnectionInitiated: (String endpointId, ConnectionInfo info) {
          // Accept connection automatically
          _nearbyConnections.acceptConnection(endpointId, onPayLoadRecieved: (endpointId, payload) {
            if (payload.type == PayloadType.BYTES) {
              final message = String.fromCharCodes(payload.bytes!);
              onMessageReceived?.call(message);
            }
          }, onPayloadTransferUpdate: (endpointId, payloadTransferUpdate) {
            // Handle transfer updates if needed
          });
        },
        onConnectionResult: (String endpointId, Status status) {
          if (status == Status.CONNECTED) {
            final device = _devices.firstWhere((d) => d.deviceId == endpointId);
            _connectedDevice = device;
            onDeviceConnected?.call(device);
          } else if (status == Status.DISCONNECTED) {
            _connectedDevice = null;
            onDisconnected?.call(endpointId);
          }
        },
        onDisconnected: (String endpointId) {
          _connectedDevice = null;
          onDisconnected?.call(endpointId);
        },
      );
      _isAdvertising = true;
    } catch (e) {
      print('Error starting advertising: $e');
    }
  }

  /// Start discovering (client mode)
  Future<void> startDiscovering() async {
    try {
      await _nearbyConnections.startDiscovery(
        'Game',
        strategy: Strategy.P2P_STAR,
        onDeviceFound: (String endpointId, Device device) {
          if (!_devices.any((d) => d.deviceId == device.deviceId)) {
            _devices.add(device);
            onDeviceFound?.call(device);
          }
        },
        onDeviceLost: (String endpointId) {
          _devices.removeWhere((d) => d.deviceId == endpointId);
        },
      );
      _isDiscovering = true;
    } catch (e) {
      print('Error starting discovery: $e');
    }
  }

  /// Connect to a discovered device
  Future<void> connectToDevice(Device device) async {
    try {
      await _nearbyConnections.requestConnection(
        device.deviceId,
        deviceName: device.deviceName,
        onConnectionInitiated: (String endpointId, ConnectionInfo info) {
          _nearbyConnections.acceptConnection(endpointId, onPayLoadRecieved: (endpointId, payload) {
            if (payload.type == PayloadType.BYTES) {
              final message = String.fromCharCodes(payload.bytes!);
              onMessageReceived?.call(message);
            }
          }, onPayloadTransferUpdate: (endpointId, payloadTransferUpdate) {
            // Handle transfer updates if needed
          });
        },
        onConnectionResult: (String endpointId, Status status) {
          if (status == Status.CONNECTED) {
            _connectedDevice = device;
            onDeviceConnected?.call(device);
          }
        },
        onDisconnected: (String endpointId) {
          _connectedDevice = null;
          onDisconnected?.call(endpointId);
        },
      );
    } catch (e) {
      print('Error connecting to device: $e');
    }
  }

  /// Send message to connected device
  Future<void> sendMessage(String message) async {
    if (_connectedDevice == null) {
      print('No device connected');
      return;
    }

    try {
      await _nearbyConnections.sendPayload(
        _connectedDevice!.deviceId,
        PayloadType.BYTES,
        message.codeUnits,
      );
    } catch (e) {
      print('Error sending message: $e');
    }
  }

  /// Stop advertising and discovery
  Future<void> stop() async {
    if (_isAdvertising) {
      await _nearbyConnections.stopAdvertising();
      _isAdvertising = false;
    }
    if (_isDiscovering) {
      await _nearbyConnections.stopDiscovery();
      _isDiscovering = false;
    }
    if (_connectedDevice != null) {
      await _nearbyConnections.disconnect(_connectedDevice!.deviceId);
      _connectedDevice = null;
    }
    _devices.clear();
  }

  List<Device> get devices => _devices;
  Device? get connectedDevice => _connectedDevice;
  bool get isConnected => _connectedDevice != null;
}
"""
        elif p2p_library == 'peerdart':
            content = """import 'package:peerdart/peerdart.dart';

class P2PService {
  Peer? _peer;
  DataConnection? _connection;
  String? _peerId;

  // Callbacks
  Function(String)? onConnected;
  Function(String)? onMessageReceived;
  Function()? onDisconnected;

  /// Initialize peer connection
  Future<void> initialize({String? peerId}) async {
    try {
      _peer = Peer(id: peerId);
      _peerId = _peer!.id;
      
      _peer!.on('open', (id) {
        print('Peer ID: $id');
      });

      _peer!.on('connection', (conn) {
        _connection = conn as DataConnection;
        _setupConnection();
        onConnected?.call(conn.peer);
      });

      _peer!.on('error', (error) {
        print('Peer error: $error');
      });
    } catch (e) {
      print('Error initializing peer: $e');
    }
  }

  /// Connect to another peer
  Future<void> connectToPeer(String peerId) async {
    if (_peer == null) {
      await initialize();
    }

    try {
      _connection = _peer!.connect(peerId) as DataConnection;
      _setupConnection();
    } catch (e) {
      print('Error connecting to peer: $e');
    }
  }

  void _setupConnection() {
    _connection!.on('open', () {
      onConnected?.call(_connection!.peer);
    });

    _connection!.on('data', (data) {
      if (data is String) {
        onMessageReceived?.call(data);
      }
    });

    _connection!.on('close', () {
      _connection = null;
      onDisconnected?.call();
    });
  }

  /// Send message to connected peer
  void sendMessage(String message) {
    if (_connection == null) {
      print('No connection established');
      return;
    }

    _connection!.send(message);
  }

  /// Get current peer ID
  String? get peerId => _peerId;

  /// Disconnect and cleanup
  void disconnect() {
    _connection?.close();
    _peer?.destroy();
    _connection = null;
    _peer = null;
    _peerId = null;
  }

  bool get isConnected => _connection != null;
}
"""
        else:  # enet_dart or default
            content = """import 'dart:typed_data';
// Note: ENet implementation may vary. This is a basic structure.
// Refer to the enet package documentation for specific implementation.

class P2PService {
  // TODO: Implement ENet-based P2P connection
  // ENet provides low-latency UDP networking suitable for real-time games
  
  bool _isConnected = false;
  String? _hostAddress;
  int? _port;

  // Callbacks
  Function(String)? onConnected;
  Function(String)? onMessageReceived;
  Function()? onDisconnected;

  /// Start hosting a game
  Future<void> startHost({int port = 7777}) async {
    // TODO: Implement ENet host creation
    _port = port;
    _isConnected = true;
    onConnected?.call('Host started on port $port');
  }

  /// Connect to a host
  Future<void> connectToHost(String address, {int port = 7777}) async {
    // TODO: Implement ENet connection to host
    _hostAddress = address;
    _port = port;
    _isConnected = true;
    onConnected?.call(address);
  }

  /// Send message/data
  Future<void> sendMessage(String message) async {
    if (!_isConnected) {
      print('Not connected');
      return;
    }
    // TODO: Implement ENet message sending
    // Convert string to bytes and send via ENet
  }

  /// Disconnect
  void disconnect() {
    // TODO: Implement ENet disconnection
    _isConnected = false;
    _hostAddress = null;
    _port = null;
    onDisconnected?.call();
  }

  bool get isConnected => _isConnected;
}
"""
        
        (self.output_path / 'lib' / 'services' / 'p2p_service.dart').write_text(content)
    
    def _generate_transactional_files(self):
        """Generate transactional app-specific files."""
        # Example: Create a sample feature
        content = """// Example feature structure for transactional apps
// Organize your features in the lib/features directory

class FeatureExample {
  // TODO: Implement your feature logic here
}
"""
        (self.output_path / 'lib' / 'features' / 'example_feature.dart').write_text(content)
    
    def _generate_config_files(self):
        """Generate configuration files."""
        # .gitignore
        gitignore = """# Miscellaneous
*.class
*.log
*.pyc
*.swp
.DS_Store
.atom/
.buildlog/
.history
.svn/
migrate_working_dir/

# IntelliJ related
*.iml
*.ipr
*.iws
.idea/

# VS Code
.vscode/

# Flutter/Dart/Pub related
**/doc/api/
**/ios/Flutter/.last_build_id
.dart_tool/
.flutter-plugins
.flutter-plugins-dependencies
.packages
.pub-cache/
.pub/
/build/

# Symbolication related
app.*.symbols

# Obfuscation related
app.*.map.json

# Android Studio will place build artifacts here
/android/app/debug
/android/app/profile
/android/app/release

# iOS
**/ios/**/*.mode1v3
**/ios/**/*.mode2v3
**/ios/**/*.moved-aside
**/ios/**/*.pbxuser
**/ios/**/*.perspectivev3
**/ios/**/*sync/
**/ios/**/.sconsign.dblite
**/ios/**/.tags*
**/ios/**/.vagrant/
**/ios/**/DerivedData/
**/ios/**/Icon?
**/ios/**/Pods/
**/ios/**/.symlinks/
**/ios/**/profile
**/ios/**/xcuserdata
**/ios/.generated/
**/ios/Flutter/App.framework
**/ios/Flutter/Flutter.framework
**/ios/Flutter/Flutter.podspec
**/ios/Flutter/Generated.xcconfig
**/ios/Flutter/ephemeral
**/ios/Flutter/app.flx
**/ios/Flutter/app.zip
**/ios/Flutter/flutter_assets/
**/ios/Flutter/flutter_export_environment.sh
**/ios/ServiceDefinitions.json
**/ios/Runner/GeneratedPluginRegistrant.*

# Firebase
**/ios/firebase_app_id_file.json
**/android/app/google-services.json
"""
        (self.output_path / '.gitignore').write_text(gitignore)
        
        # Analysis options
        analysis_options = """include: package:flutter_lints/flutter.yaml

linter:
  rules:
    - prefer_const_constructors
    - prefer_const_literals_to_create_immutables
    - avoid_print
    - prefer_single_quotes
    - require_trailing_commas

analyzer:
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
"""
        (self.output_path / 'analysis_options.yaml').write_text(analysis_options)
    
    def _generate_readme(self):
        """Generate README.md file."""
        readme = f"""# {self.project_name}

A Flutter {self.app_category} template generated with Flutter Template Generator.

## Features

- **App Type**: {self.preferences.get('app_category', 'N/A').title()}
- **State Management**: {self.preferences.get('state_management', 'N/A').title()}
- **Database**: {self.preferences.get('database', 'N/A').replace('_', ' ').title()}
- **Authentication**: {'Yes' if self.preferences.get('has_auth', False) else 'No'}
- **Routing**: {'Yes' if self.preferences.get('has_routing', True) else 'No'}
- **Theme Management**: {'Yes' if self.preferences.get('has_theme', True) else 'No'}

## Getting Started

1. Install Flutter dependencies:
   ```bash
   flutter pub get
   ```

2. Run the app:
   ```bash
   flutter run
   ```

## Project Structure

```
lib/
├── auth/              # Authentication logic
├── models/            # Data models
├── screens/           # UI screens
├── services/          # Business logic services
├── widgets/           # Reusable widgets
├── utils/             # Utility functions
└── constants/         # App constants
```

## Configuration

### Firebase Setup (if using Firebase)

1. Add your `google-services.json` to `android/app/`
2. Add your `GoogleService-Info.plist` to `ios/Runner/`
3. Follow Firebase setup instructions for Flutter

### Database Setup

{'Configure your SQLite database in `lib/services/database_service.dart`' if self.preferences.get('database') == 'sqlite' else 'Configure your database connection in the respective service files.'}

## Development

This template provides a solid foundation for your Flutter app. Customize it according to your needs.

## License

MIT License
"""
        (self.output_path / 'README.md').write_text(readme)

