"""
Configuration management for template generation.
"""

from typing import Dict, Any


class Config:
    """Manages configuration for template generation."""
    
    # State management packages
    STATE_MANAGEMENT_PACKAGES = {
        'provider': ['provider'],
        'riverpod': ['flutter_riverpod', 'riverpod_annotation'],
        'bloc': ['flutter_bloc', 'equatable'],
        'getx': ['get'],
        'redux': ['redux', 'flutter_redux'],
    }
    
    # Database packages
    DATABASE_PACKAGES = {
        'firebase_firestore': ['cloud_firestore'],
        'sqlite': ['sqflite', 'path'],
        'rest_api_(no_local_db)': ['http', 'dio'],
        'none': [],
    }
    
    # Auth packages
    AUTH_PACKAGES = {
        'firebase_auth': ['firebase_auth', 'firebase_core'],
        'custom_auth_(rest_api)': ['http', 'dio', 'shared_preferences'],
        'local_auth_(biometric)': ['local_auth'],
    }
    
    # Routing packages
    ROUTING_PACKAGES = {
        'go_router': ['go_router'],
        'auto_route': ['auto_route', 'auto_route_generator'],
    }
    
    # Additional feature packages
    FEATURE_PACKAGES = {
        'localization': ['flutter_localizations', 'intl'],
        'analytics': ['firebase_analytics'],
        'crash_reporting': ['firebase_crashlytics'],
        'notifications': ['firebase_messaging'],
        'payments': ['in_app_purchase'],
    }
    
    # P2P/Multiplayer packages
    P2P_PACKAGES = {
        'flutter_nearby_connections': ['flutter_nearby_connections'],
        'peerdart': ['peerdart'],
        'enet_dart': ['enet'],
    }
    
    @staticmethod
    def get_dependencies(preferences: Dict[str, Any]) -> list:
        """Get list of dependencies based on preferences."""
        dependencies = []
        
        # State management
        state_mgmt = preferences.get('state_management', 'provider')
        dependencies.extend(Config.STATE_MANAGEMENT_PACKAGES.get(state_mgmt, []))
        
        # Database
        database = preferences.get('database', 'none')
        dependencies.extend(Config.DATABASE_PACKAGES.get(database, []))
        
        # Auth
        if preferences.get('has_auth', False):
            auth_provider = preferences.get('auth_provider')
            if auth_provider:
                dependencies.extend(Config.AUTH_PACKAGES.get(auth_provider, []))
        
        # Routing
        if preferences.get('has_routing', True):
            dependencies.append('go_router')
        
        # Localization
        if preferences.get('has_localization', False):
            dependencies.extend(Config.FEATURE_PACKAGES['localization'])
        
        # Analytics
        if preferences.get('has_analytics', False):
            dependencies.extend(Config.FEATURE_PACKAGES['analytics'])
        
        # Crash reporting
        if preferences.get('has_crash_reporting', False):
            dependencies.extend(Config.FEATURE_PACKAGES['crash_reporting'])
        
        # Notifications
        if preferences.get('has_notifications', False):
            dependencies.extend(Config.FEATURE_PACKAGES['notifications'])
        
        # Payments
        if preferences.get('has_payments', False):
            dependencies.extend(Config.FEATURE_PACKAGES['payments'])
        
        # Game-specific
        if preferences.get('app_category') == 'game':
            game_engine = preferences.get('game_engine', 'flame')
            if game_engine.lower() == 'flame':
                dependencies.append('flame')
            
            # P2P/Multiplayer
            if preferences.get('has_multiplayer', False):
                multiplayer_type = preferences.get('multiplayer_type')
                if multiplayer_type == 'p2p':
                    p2p_library = preferences.get('p2p_library')
                    if p2p_library:
                        dependencies.extend(Config.P2P_PACKAGES.get(p2p_library, []))
        
        # Common utilities
        dependencies.extend([
            'shared_preferences',
            'path_provider',
        ])
        
        # Remove duplicates and sort
        return sorted(list(set(dependencies)))
    
    @staticmethod
    def get_dev_dependencies(preferences: Dict[str, Any]) -> list:
        """Get list of dev dependencies based on preferences."""
        dev_dependencies = [
            'flutter_test',
            'flutter_lints',
        ]
        
        # State management dev dependencies
        state_mgmt = preferences.get('state_management', 'provider')
        if state_mgmt == 'riverpod':
            dev_dependencies.append('riverpod_generator')
            dev_dependencies.append('build_runner')
        elif state_mgmt == 'bloc':
            dev_dependencies.append('bloc_test')
        
        # Routing dev dependencies
        if preferences.get('has_routing', True):
            # go_router doesn't need dev dependencies
            pass
        
        return sorted(list(set(dev_dependencies)))

