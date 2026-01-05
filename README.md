# Flutter Template Generator

An interactive Python tool to generate Flutter app templates based on your preferences. Highly scalable and extensible architecture.

## Features

- 🎮 **Game Apps**: Generate templates for Flutter games with Flame, Unity, or custom canvas support
- 💼 **Transactional Apps**: Generate templates for business/transactional applications
- 🔐 **Authentication**: Support for Firebase Auth, Custom REST API Auth, or Local Biometric Auth
- 💾 **Database Options**: Firebase Firestore, SQLite, REST API, or None
- 🎨 **State Management**: Choose from Provider, Riverpod, Bloc, GetX, or Redux
- 🧭 **Routing**: Built-in routing support with GoRouter
- 🌓 **Theme Management**: Dark/Light mode support
- 📱 **Additional Features**: Analytics, Crash Reporting, Push Notifications, Payments, Offline Mode

## Installation

No external dependencies required! Uses only Python standard library.

```bash
# Clone or download this repository
cd py_plantilla

# Make the script executable (optional)
chmod +x main.py
```

## Usage

```bash
python main.py
```

The script will guide you through an interactive questionnaire:

1. **App Type**: Choose between Game or Transactional App
2. **Authentication**: Whether you need auth and which method
3. **Database**: Select your database solution
4. **State Management**: Choose your preferred state management solution
5. **Additional Features**: Configure routing, localization, themes, analytics, etc.

## Example Workflow

```bash
$ python main.py

============================================================
🚀 Flutter Template Generator
============================================================

Let's configure your Flutter app template...

What type of app are you building?
  → 1. Game
    2. Transactional App

Select option (1-2, default: 1): 2

Does your app require authentication? (Y/n): y

Which authentication method would you like to use?
  → 1. Firebase Auth
    2. Custom Auth (REST API)
    3. Local Auth (Biometric)

Select option (1-3, default: 1): 1

...
```

## Project Structure

```
py_plantilla/
├── main.py                 # Entry point
├── questions.py            # Interactive question handler
├── config.py               # Configuration and dependency management
├── generators/             # Template generators
│   ├── __init__.py
│   └── flutter_generator.py
├── requirements.txt        # Python dependencies (none required)
└── README.md              # This file
```

## Architecture

The project is designed with scalability in mind:

- **Modular Design**: Each component (questions, config, generators) is separated
- **Extensible**: Easy to add new app types, features, or generators
- **Configuration-Driven**: Dependencies and features are managed through configuration
- **Template-Based**: Generates complete Flutter project structures

## Adding New Features

### Adding a New App Type

1. Create a new generator in `generators/` (e.g., `react_native_generator.py`)
2. Add the generator option in `questions.py`
3. Update `main.py` to handle the new generator

### Adding New Questions

1. Add question methods in `QuestionHandler` class in `questions.py`
2. Update `collect_preferences()` method
3. Handle the new preference in generators

### Adding New Dependencies

1. Update `Config` class in `config.py`
2. Add packages to appropriate dictionaries
3. Update generator logic if needed

## Generated Template Structure

The generator creates a complete Flutter project with:

- Proper directory structure
- `pubspec.yaml` with all dependencies
- `main.dart` configured with your choices
- Sample screens and services
- Configuration files (`.gitignore`, `analysis_options.yaml`)
- README with setup instructions

## Future Enhancements

- [ ] Support for React Native templates
- [ ] Support for native iOS/Android templates
- [ ] Interactive CLI with colors and better UX (using `inquirer` or `rich`)
- [ ] Template preview before generation
- [ ] Custom template injection
- [ ] Plugin system for third-party generators

## License

MIT License

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

