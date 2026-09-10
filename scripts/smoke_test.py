import sys
import xml.etree.ElementTree as ET
from pathlib import Path

def validate_xml_file(filepath: Path) -> bool:
    """Valida la sintaxis XML de un archivo dado."""
    if not filepath.exists():
        print(f"[❌ NO ENCONTRADO] {filepath}")
        return False
    try:
        ET.parse(filepath)
        print(f"[✅ XML VÁLIDO] {filepath}")
        return True
    except ET.ParseError as err:
        print(f"[❌ ERROR XML] {filepath}: {err}")
        return False

def check_repository_structure() -> bool:
    """Verifica que los archivos esenciales existan en el repositorio."""
    critical_files = [
        Path("README.md"),
        Path("detection/rules/local_rules.xml"),
        Path("detection/decoders/custom_decoders.xml"),
        Path("configs/wazuh-manager/active_response.xml"),
        Path("configs/wazuh-manager/internal_options.conf"),
        Path("configs/wazuh-indexer/jvm.options"),
    ]
    
    all_ok = True
    print("--- 🔍 INICIANDO SMOKE TEST DE ESTRUCTURA Y SINTAXIS ---")
    for file_path in critical_files:
        if file_path.suffix == ".xml":
            if not validate_xml_file(file_path):
                all_ok = False
        else:
            if file_path.exists():
                print(f"[✅ OK] {file_path}")
            else:
                print(f"[❌ NO ENCONTRADO] {file_path}")
                all_ok = False
    return all_ok

if __name__ == "__main__":
    if not check_repository_structure():
        print("\n❌ Smoke test fallido: Revisa los errores antes de continuar.")
        sys.exit(1)
    print("\n✅ Smoke test completado con éxito. El repositorio está listo.")
    sys.exit(0)
