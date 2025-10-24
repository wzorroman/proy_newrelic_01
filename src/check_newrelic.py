#!/usr/bin/env python3
"""Script para verificar la configuración de NewRelic"""
import os
import sys

# Agregar el directorio src al path
sys.path.append(os.path.dirname(__file__))

from app.config.config import settings
from app.config.newrelic_config import NewRelicConfig

def main():
    print("🔍 Verificando configuración de NewRelic")
    print("=" * 50)

    # Verificar configuración básica
    print("📋 Configuración de la aplicación:")
    print(f"   Environment: {settings.fastapi_env}")
    print(f"   App Name: {settings.new_relic_app_name}")
    print(f"   License Key: {'✅ CONFIGURADO' if NewRelicConfig.is_license_valid() else '❌ NO CONFIGURADO'}")

    if NewRelicConfig.is_license_valid():
        print(f"   License Preview: {settings.new_relic_license_key[:8]}...{settings.new_relic_license_key[-8:]}")

    print("\n🌍 Variables de entorno:")
    for key in ['NEW_RELIC_LICENSE_KEY', 'NEW_RELIC_APP_NAME']:
        value = os.getenv(key)
        if value:
            masked = value[:8] + '...' + value[-8:] if len(value) > 16 else value
            print(f"   {key}: {masked}")
        else:
            print(f"   {key}: ❌ NO DEFINIDA")

    print("\n📊 Estado de NewRelic:")
    status = NewRelicConfig.get_config_status()
    print(f"   License Configured: {'✅' if status['license_configured'] else '❌'}")
    print(f"   App Name: {status['app_name']}")
    print(f"   Environment: {status['environment']}")

    if status['license_configured']:
        print("   🚀 NewRelic debería funcionar correctamente")
    else:
        print("   ⚠️  Configura una LICENSE_KEY válida en el archivo .env")

if __name__ == "__main__":
    main()
