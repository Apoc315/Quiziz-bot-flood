#!/usr/bin/env python3
"""
🎮 Quizizz Ultimate Tool - Main Menu
"""

import sys
import os
import argparse
from termcolor import colored, cprint
from pyfiglet import Figlet
import colorama

# Initialize colorama
colorama.init()

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

def print_banner():
    """Print fancy banner"""
    f = Figlet(font='slant')
    print(colored(f.renderText('QUIZIZZ TOOL'), 'cyan'))
    print(colored('=' * 60, 'blue'))
    print(colored('🎯 Complete Quizizz Automation Suite', 'yellow'))
    print(colored('=' * 60, 'blue'))
    print()

def print_menu():
    """Print main menu"""
    print(colored("\n📋 MAIN MENU", 'yellow', attrs=['bold']))
    print(colored("-" * 40, 'blue'))
    print(colored("1. 🤖 Bot Flood Spammer", 'green'))
    print(colored("2. 🔍 Get Answers for Quiz", 'cyan'))
    print(colored("3. 🎮 Check Game Status", 'magenta'))
    print(colored("4. ⚙️ Settings & Configuration", 'yellow'))
    print(colored("5. 📊 View Statistics", 'white'))
    print(colored("6. ❌ Exit", 'red'))
    print(colored("-" * 40, 'blue'))

def bot_flood_menu():
    """Bot flood submenu"""
    print(colored("\n🤖 BOT FLOOD SETTINGS", 'yellow', attrs=['bold']))
    print(colored("-" * 40, 'blue'))
    
    game_code = input(colored("🎮 Enter Game Code (6 digits): ", 'cyan')).strip()
    if len(game_code) != 6 or not game_code.isdigit():
        print(colored("❌ Invalid game code!", 'red'))
        return
    
    bot_count = input(colored("👥 Number of bots (1-100): ", 'cyan')).strip()
    if not bot_count.isdigit() or not (1 <= int(bot_count) <= 100):
        print(colored("❌ Invalid bot count!", 'red'))
        return
    
    delay = input(colored("⏱️ Delay between bots (seconds): ", 'cyan')).strip()
    if not delay.replace('.', '').isdigit():
        print(colored("❌ Invalid delay!", 'red'))
        return
    
    headless = input(colored("🖥️ Headless mode? (y/N): ", 'cyan')).lower().strip() == 'y'
    
    print(colored(f"\n🚀 Ready to launch {bot_count} bots!", 'green'))
    confirm = input(colored("Start bot flood? (y/N): ", 'red')).lower().strip()
    
    if confirm == 'y':
        try:
            from bot_flood import QuizizzBotFlood
            flood = QuizizzBotFlood(
                game_code=game_code,
                bot_count=int(bot_count),
                delay=float(delay),
                headless=headless
            )
            flood.start_flood()
        except ImportError:
            print(colored("❌ Bot flood module not found!", 'red'))
        except Exception as e:
            print(colored(f"❌ Error: {e}", 'red'))

def answer_fetcher_menu():
    """Answer fetcher submenu"""
    print(colored("\n🔍 ANSWER FINDER", 'yellow', attrs=['bold']))
    print(colored("-" * 40, 'blue'))
    
    quiz_id = input(colored("📝 Enter Quiz ID: ", 'cyan')).strip()
    if not quiz_id:
        print(colored("❌ Quiz ID required!", 'red'))
        return
    
    try:
        from answer_fetcher import QuizizzAnswerFetcher
        fetcher = QuizizzAnswerFetcher(quiz_id)
        answers = fetcher.fetch_answers()
        fetcher.display_answers()
    except ImportError:
        print(colored("❌ Answer fetcher module not found!", 'red'))
    except Exception as e:
        print(colored(f"❌ Error: {e}", 'red'))

def game_checker_menu():
    """Game checker submenu"""
    print(colored("\n🎮 GAME CHECKER", 'yellow', attrs=['bold']))
    print(colored("-" * 40, 'blue'))
    
    game_code = input(colored("🎮 Enter Game Code: ", 'cyan')).strip()
    
    try:
        from game_checker import QuizizzGameChecker
        checker = QuizizzGameChecker(game_code)
        status = checker.check_game()
        checker.display_status()
    except ImportError:
        print(colored("❌ Game checker module not found!", 'red'))
    except Exception as e:
        print(colored(f"❌ Error: {e}", 'red'))

def settings_menu():
    """Settings menu"""
    print(colored("\n⚙️ SETTINGS", 'yellow', attrs=['bold']))
    print(colored("-" * 40, 'blue'))
    print(colored("1. View Current Settings", 'cyan'))
    print(colored("2. Edit Configuration", 'green'))
    print(colored("3. Test ChromeDriver", 'yellow'))
    print(colored("4. Back to Main Menu", 'white'))
    
    choice = input(colored("\nSelect option: ", 'cyan')).strip()
    
    if choice == '1':
        import json
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                print(colored(json.dumps(config, indent=2), 'green'))
        except:
            print(colored("❌ Could not load config!", 'red'))
    elif choice == '2':
        print(colored("\n⚠️ Edit config.json file manually", 'yellow'))
    elif choice == '3':
        test_chromedriver()

def test_chromedriver():
    """Test ChromeDriver installation"""
    print(colored("\n🔧 Testing ChromeDriver...", 'cyan'))
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        print(colored("📦 Installing ChromeDriver...", 'yellow'))
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        print(colored("✅ ChromeDriver installed successfully!", 'green'))
        
        driver.get("https://www.google.com")
        print(colored("🌐 Browser opened Google successfully!", 'green'))
        
        driver.quit()
        print(colored("✅ Test completed successfully!", 'green'))
    except Exception as e:
        print(colored(f"❌ ChromeDriver test failed: {e}", 'red'))

def main():
    """Main function"""
    print_banner()
    
    # Check dependencies
    try:
        import selenium
        import colorama
        import termcolor
    except ImportError:
        print(colored("❌ Missing dependencies!", 'red'))
        print(colored("Run: pip install -r requirements.txt", 'yellow'))
        return
    
    while True:
        print_menu()
        choice = input(colored("\n👉 Select option (1-6): ", 'cyan')).strip()
        
        if choice == '1':
            bot_flood_menu()
        elif choice == '2':
            answer_fetcher_menu()
        elif choice == '3':
            game_checker_menu()
        elif choice == '4':
            settings_menu()
        elif choice == '5':
            print(colored("\n📊 Statistics coming soon!", 'yellow'))
        elif choice == '6':
            print(colored("\n👋 Goodbye! Thanks for using Quizizz Tool!", 'green'))
            break
        else:
            print(colored("❌ Invalid choice! Please try again.", 'red'))
        
        input(colored("\nPress Enter to continue...", 'white'))

if __name__ == "__main__":
    main()
