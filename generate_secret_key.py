#!/usr/bin/env python
"""
Script para gerar uma SECRET_KEY segura para Django
Execute: python generate_secret_key.py
"""

from django.core.management.utils import get_random_secret_key

print("=" * 70)
print("DJANGO SECRET KEY GENERATOR")
print("=" * 70)
print()
print("Cole esta chave nas variáveis de ambiente do Vercel:")
print()
print(get_random_secret_key())
print()
print("=" * 70)
print("IMPORTANTE:")
print("- Nunca compartilhe esta chave publicamente")
print("- Use uma chave diferente para cada ambiente (dev/prod)")
print("- Configure no Vercel em: Settings > Environment Variables")
print("=" * 70)
