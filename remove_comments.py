import os
import re
import glob
from colorama import init, Fore, Style  # type: ignore # Renkli çıktı için eklenen kütüphane

# Colorama'nın başlatılması
init(autoreset=True)

def remove_comments(file_path):
    """Belirtilen dosyadaki yorumları kaldırır."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        # Yorumları kaldırma işlemi
        modified_content = re.sub(r'(?<!@)//(?! @| @duzenleme\b| @fixme\b).*', '', content)
        modified_content = re.sub(r'(?<!@)/\*(?:(?! @| @duzenleme\b| @fixme\b)[\s\S])*?\*/', '', modified_content)

        # Dosya içeriği değiştiyse yeniden yaz
        if modified_content != content:
            with open(file_path, 'w') as file:
                file.write(modified_content)
            print(f"{Fore.GREEN}Başarılı:{Style.RESET_ALL} {file_path} dosyasından yorumlar kaldırıldı.")
        else:
            print(f"{Fore.YELLOW}Değişiklik yapılmadı:{Style.RESET_ALL} {file_path} dosyasında zaten yorumlar bulunmamaktadır.")
    except OSError as e:
        print(f"{Fore.RED}Hata:{Style.RESET_ALL} {e.strerror}. Dosya işlenemedi: {file_path}")

def display_directories():
    """Mevcut klasörleri listeler."""
    try:
        directories = [d for d in os.listdir() if os.path.isdir(d)]
        print("Mevcut klasörler:")
        for idx, directory in enumerate(directories, 1):
            print(f"{idx}. {directory}")
        return directories
    except OSError as e:
        print(f"{Fore.RED}Hata:{Style.RESET_ALL} {e.strerror}. Klasörler listelenemedi.")
        return []

def select_directory():
    """Kullanıcıdan klasör seçmesini sağlar, 'q' tuşu ile ana menüye dönebilir."""
    while True:
        directories = display_directories()
        if not directories:
            return None
        
        choice = input("\nİşlemek istediğiniz klasörün numarasını seçin veya geri dönmek için 'q' tuşlayın: ")
        
        if choice.lower() == 'q':
            print(f"{Fore.YELLOW}Ana menüye dönülüyor...{Style.RESET_ALL}")
            return None
        
        try:
            dir_choice = int(choice) - 1
            if 0 <= dir_choice < len(directories):
                selected_directory = directories[dir_choice]
                return selected_directory
            else:
                print(f"{Fore.YELLOW}Geçersiz numara.{Style.RESET_ALL} Lütfen tekrar deneyin.")
        except ValueError:
            print(f"{Fore.YELLOW}Geçersiz giriş.{Style.RESET_ALL} Lütfen bir numara girin veya çıkmak için 'q' tuşlayın.")

def get_extensions():
    """Kullanıcıdan işlem yapılacak dosya uzantılarını seçmesini sağlar."""
    while True:
        extensions_input = input("\nİşlemek istediğiniz dosya uzantılarını seçin (örn: .h, .cpp, .c): ")
        if extensions_input.lower() == 'q':
            print(f"{Fore.YELLOW}Ana menüye dönülüyor...{Style.RESET_ALL}")
            return None
        
        extensions = [ext.strip() for ext in extensions_input.split(',')]
        if all(ext.startswith('.') for ext in extensions):
            return extensions
        else:
            print(f"{Fore.YELLOW}Geçersiz uzantılar.{Style.RESET_ALL} Uzantılar . [.cpp, .h, .c] ile başlamalıdır. Tekrar deneyin.")

def process_files(directory, extensions):
    """Belirtilen klasördeki belirtilen uzantılara sahip dosyalardan yorumları kaldırır."""
    print(f"\n'{directory}' klasöründe aşağıdaki dosyalardan yorumlar kaldırılıyor:")
    try:
        for ext in extensions:
            files = glob.glob(os.path.join(directory, f"*{ext}"))
            if files:
                print(f"\n{ext} uzantılı dosyalar:")
                for file_path in files:
                    remove_comments(file_path)
            else:
                print(f"{ext} uzantılı dosya bulunamadı.")
    except OSError as e:
        print(f"{Fore.RED}Hata:{Style.RESET_ALL} {e.strerror}. Dosyalar işlenemedi.")

def main():
    """Ana işlem döngüsü."""
    print("Yorumları kaldırmak için klasör ve dosya uzantılarını seçin.")
    while True:
        selected_directory = select_directory()
        if selected_directory is None:
            continue
        
        extensions = get_extensions()
        if extensions is None:
            continue
        
        process_files(selected_directory, extensions)
        
        cont = input("\nİşlemler tamamlandı. Ana menüye dönmek için Enter tuşuna basın veya çıkmak için 'q' tuşlayın: ")
        if cont.lower() == 'q':
            print(f"{Fore.YELLOW}Çıkış yapılıyor...{Style.RESET_ALL}")
            break
        elif cont.strip() != '':
            print(f"{Fore.YELLOW}Geçersiz giriş.{Style.RESET_ALL} Ana menüye dönülüyor...")

if __name__ == "__main__":
    main()
