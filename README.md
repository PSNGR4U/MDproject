# MDproject

## Opis projektu

MDproject to aplikacja internetowa dla restauracji, tworzona w ramach projektu PWGP SEM5. Jej celem jest usprawnienie prezentacji menu oraz obsługi klientów i zarządzania ofertą restauracji.

Projekt należy do branży **FoodTech / E-commerce**.

## Zespół

- **Maksym Boiko** (`maks819`) — Backend Developer / Git Master
- **Dmytro Shmakov** (`PSNGR4U`) — Frontend Developer / UI Designer

## Technologie

- Python 3.9
- Django 4.2.30
- SQLite
- HTML5
- CSS3
- Pillow
- Git i GitHub

## Zaimplementowane funkcjonalności

- Rejestracja i logowanie użytkowników.
- Obsługa ról użytkowników: klient i manager.
- Wyświetlanie menu restauracji.
- Przeglądanie dań i filtrowanie menu według kategorii.
- Wyszukiwanie dań.
- Wyświetlanie zdjęć, opisów i cen dań.
- Dodawanie, edytowanie i usuwanie dań przez managera.
- Dodawanie, edytowanie i usuwanie kategorii przez managera.
- Kontrola uprawnień dostępu do funkcji zarządzania menu.

## Główny scenariusz MVP

Manager loguje się do aplikacji, przechodzi do menu, dodaje nowe danie za pomocą formularza, a następnie zapisuje je w bazie danych SQLite. Po zapisaniu danie pojawia się na stronie menu i jest widoczne dla użytkowników.

## Struktura projektu

```text
MDproject/
│
├── accounts/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── menu/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── .gitignore
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

### Podział odpowiedzialności w projekcie

- **models.py** — definicje modeli i struktury danych.
- **forms.py** — formularze i walidacja danych.
- **views.py** — logika aplikacji i obsługa żądań użytkowników.
- **urls.py** — konfiguracja adresów URL.
- **templates/** — szablony stron HTML.
- **static/** — pliki CSS i obrazy.
- **migrations/** — zmiany struktury bazy danych.

## Instalacja i uruchomienie

### 1. Sklonowanie repozytorium

```bash
git clone https://github.com/PSNGR4U/MDproject.git
cd MDproject
```

### 2. Utworzenie środowiska wirtualnego

```bash
python -m venv .venv
```

### 3. Aktywacja środowiska

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalacja zależności

```bash
python -m pip install -r requirements.txt
```

### 5. Wykonanie migracji bazy danych

```bash
python manage.py migrate
```

### 6. Uruchomienie serwera

```bash
python manage.py runserver
```

Aplikacja będzie dostępna pod adresem:

http://127.0.0.1:8000/

## Podział obowiązków

### Maksym Boiko — Backend Developer / Git Master

- Konfiguracja projektu Django.
- Tworzenie modeli i obsługa bazy danych SQLite.
- Implementacja formularzy, widoków i logiki backendowej.
- System rejestracji, logowania i uprawnień użytkowników.
- Zarządzanie repozytorium GitHub, branchami i Pull Requestami.

### Dmytro Shmakov — Frontend Developer / UI Designer

- Projektowanie wyglądu aplikacji.
- Tworzenie struktury HTML5.
- Stylowanie stron za pomocą CSS3.
- Integracja szablonów HTML z widokami Django.
- Dostosowanie interfejsu do różnych rozmiarów ekranów.

## Poza zakresem aktualnego MVP

Poniższe funkcjonalności nie są częścią obecnie zrealizowanego MVP i mogą zostać rozwinięte w kolejnych etapach projektu:

- Koszyk zakupowy i składanie zamówień online.
- Zarządzanie statusami zamówień.
- Rezerwacja stolików.
- Integracja z prawdziwymi systemami płatności, np. BLIK i PayU.
- Weryfikacja numeru telefonu przez SMS.
- Dedykowana aplikacja mobilna.

## Informacje dodatkowe

Projekt jest rozwijany zespołowo z wykorzystaniem Git i GitHub. Prace są dzielone na osobne branche, a zmiany trafiają do głównej gałęzi `main` za pośrednictwem Pull Requestów.
