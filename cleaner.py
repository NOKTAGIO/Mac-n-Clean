import os
import shutil
import time
from pathlib import Path


def get_size(path):
    """Calcule la taille d'un dossier en Mo"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total_size += os.path.getsize(fp)
            except FileNotFoundError:
                continue
    return total_size / (1024 * 1024)


def clean_folder(folder_path, days=30, dry_run=True):
    """Supprime les fichiers plus vieux que 'days' jours dans 'folder_path'"""
    if not os.path.exists(folder_path):
        print(f"⚠️  Dossier introuvable : {folder_path}")
        return 0

    folder = Path(folder_path)
    current_time = time.time()
    deleted_count = 0
    freed_space = 0

    print(f"🔍 Analyse de : {folder_path}")
    
    for item in folder.iterdir():
        try:
            # On ne touche pas aux dossiers, seulement aux fichiers pour simplifier
            if item.is_file():
                file_age = current_time - item.stat().st_mtime
                days_old = file_age / (60 * 60 * 24)

                if days_old > days:
                    size = item.stat().st_size
                    if dry_run:
                        print(f"   🗑️  Fichier candidat : {item.name} ({size/1024:.1f} KB) - {days_old:.0f} jours")
                    else:
                        item.unlink()
                        deleted_count += 1
                        freed_space += size
        except PermissionError:
            print(f"   ❌ Impossible de supprimer : {item.name} (Permission refusée)")
        except Exception as e:
            print(f"   ⚠️  Erreur sur {item.name} : {e}")

    if not dry_run:
        print(f"✅ Terminé : {deleted_count} fichiers supprimés. Espace libéré : {freed_space/1024/1024:.2f} Mo")
    else:
        print(f"🔒 Mode simulation : Rien n'a été supprimé.")


def main():
    print("🧹 Mac-n-Clean - Script de Nettoyage (Cache & Logs)")
    print("Ce script nettoie uniquement les fichiers temporaires et les logs.")
    print("⚠️  Il ne supprime PAS les fichiers système ni les Téléchargements.")
    
    # Configuration
    # Caches et Logs uniquement (Downloads retiré)
    CACHE_PATH = os.path.expanduser("~/Library/Caches")
    LOGS_PATH = os.path.expanduser("~/Library/Logs")
    DAYS_TO_KEEP = 30

    # Simulation d'abord
    print("\n--- Simulation (Aucun fichier supprimé) ---")
    clean_folder(CACHE_PATH, DAYS_TO_KEEP, dry_run=True)
    clean_folder(LOGS_PATH, DAYS_TO_KEEP, dry_run=True)

    # Demande de confirmation
    print("\n--- Exécution Réelle ---")
    confirm = input("Voulez-vous vraiment supprimer ces fichiers temporaires ? (oui/non) : ")
    
    if confirm.lower() == 'oui':
        print("\n🚀 Nettoyage en cours...")
        clean_folder(CACHE_PATH, DAYS_TO_KEEP, dry_run=False)
        clean_folder(LOGS_PATH, DAYS_TO_KEEP, dry_run=False)
        print("\n✨ Nettoyage terminé !")
    else:
        print("❌ Annulation du nettoyage.")


if __name__ == "__main__":
    main()
