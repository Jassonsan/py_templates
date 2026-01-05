#!/usr/bin/env python3
"""
Template Generator
An interactive tool to generate app templates (Flutter, macOS, etc.) based on user preferences.
"""

import os
import sys
from pathlib import Path
from questions import QuestionHandler
from generators.flutter_generator import FlutterTemplateGenerator
from generators.macos_generator import MacOSTemplateGenerator
from config import Config


def main():
    """Main entry point for the template generator."""
    print("=" * 60)
    print("🚀 Template Generator")
    print("=" * 60)
    print()
    
    # Initialize question handler
    question_handler = QuestionHandler()
    
    # Collect user preferences
    preferences = question_handler.collect_preferences()
    
    # Display summary
    print("\n" + "=" * 60)
    print("📋 Configuration Summary")
    print("=" * 60)
    for key, value in preferences.items():
        print(f"  {key}: {value}")
    print()
    
    # Confirm before generating
    confirm = input("Proceed with template generation? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Template generation cancelled.")
        return
    
    # Get project name and path
    project_name = input("\nEnter project name: ").strip()
    if not project_name:
        print("Error: Project name cannot be empty.")
        return
    
    base_path = Path("/Users/jasson/Developer/Jotaeme")
    # Ensure base directory exists
    base_path.mkdir(parents=True, exist_ok=True)
    
    default_path = base_path / project_name
    output_path = input(f"Enter output directory (default: {default_path}): ").strip()
    if not output_path:
        output_path = default_path
    else:
        output_path = Path(output_path)
        # If relative path, make it relative to base_path
        if not output_path.is_absolute():
            output_path = base_path / output_path
        # Convert to absolute path to ensure consistency
        output_path = output_path.resolve()
    
    # Initialize generator based on app type
    if preferences['app_type'] == 'flutter':
        generator = FlutterTemplateGenerator(preferences, project_name, output_path)
    elif preferences['app_type'] == 'macos':
        generator = MacOSTemplateGenerator(preferences, project_name, output_path)
    else:
        print(f"Error: App type '{preferences['app_type']}' not yet supported.")
        return
    
    # Generate template
    try:
        print(f"\n📦 Generating template at: {output_path.absolute()}")
        generator.generate()
        print("\n✅ Template generated successfully!")
        print(f"\nNext steps:")
        if preferences['app_type'] == 'flutter':
            print(f"  cd {output_path}")
            print(f"  flutter pub get")
            print(f"  flutter run")
        elif preferences['app_type'] == 'macos':
            print(f"  cd {output_path / project_name}")
            print(f"  open {project_name}.xcodeproj")
            print(f"  # Then build and run in Xcode (Cmd+R)")
    except Exception as e:
        print(f"\n❌ Error generating template: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

