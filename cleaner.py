import os
import shutil
import time
from pathlib import Path

def clean_folder(folder_path, days=30, dry_run=True):
    """Supprime les fichiers plus vieux que 'days' jours dans 'folder_path' (Récursif)"""
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"⚠️  Dossier introuvable : {folder_path}")
        return 0

    current_time = time.time()
    deleted_count = 0
    freed_space = 0

    print(f"🔍 Analyse de : {folder_path}")
    
    # Utilisation de rglob pour tout chercher (récursif) ou walk
    # rglob('*') cherche dans le dossier ET ses sous-dossiers
    for item in folder.rglob('*'):
        if item.is_file():
            try:
                file_age = current_time - item.stat().st_mtime
                days_old = file_age / (60 * 60 * 24)

                if days_old > days:
                    size = item.stat().st_size
                    if dry_run:
                        print(f"   🗑️  Candidat : {item.relative_to(folder)} ({size/1024:.1f} KB) - {days_old:.0f} jours")
                    else:
                        item.unlink()
                        deleted_count += 1
                        freed_space += size
            except PermissionError:
                # On ignore silencieusement ou on logge en debug si on ne peut pas toucher
                # print(f"   ❌ Permission refusée : {item}")
                continue
            except Exception as e:
                print(f"   ⚠️  Erreur sur {item.name} : {e}")

    if not dry_run:
        print(f"✅ Terminé : {deleted_count} fichiers supprimés. Espace libéré : {freed_space/1024/1024:.2f} Mo")
    else:
        print(f"🔒 Mode simulation : Rien n'a été supprimé.")
    return freed_space

def main():
    print("🧹 Mac-n-Clean - Script de Nettoyage (Cache & Logs)")
    
    CACHE_PATH = os.path.expanduser("~/Library/Caches")
    LOGS_PATH = os.path.expanduser("~/Library/Logs")
    DAYS_TO_KEEP = 30

    # 1. Simulation
    print("\n--- Simulation (Aucun fichier supprimé) ---")
    clean_folder(CACHE_PATH, DAYS_TO_KEEP, dry_run=True)
    clean_folder(LOGS_PATH, DAYS_TO_KEEP, dry_run=True)

    # 2. Confirmation
    print("\n--- Exécution Réelle ---")
    # Ajout d'une vérification de 'oui' strict
    confirm = input("Voulez-vous vraiment supprimer ces fichiers ? (tapez 'oui' pour continuer) : ")
    
    if confirm.lower() == 'oui':
        print("\n🚀 Nettoyage en cours...")
        clean_folder(CACHE_PATH, DAYS_TO_KEEP, dry_run=False)
        clean_folder(LOGS_PATH, DAYS_TO_KEEP, dry_run=False)
        print("\n✨ Nettoyage terminé !")
    else:
        print("❌ Annulation du nettoyage.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Arrêté par l'utilisateur.")
