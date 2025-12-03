import requests
from bs4 import BeautifulSoup
import json
from colorama import Fore, Style, init
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
from logger import Logger

init()

class QuizizzAnswerFetcher:
    def __init__(self, quiz_id):
        self.quiz_id = quiz_id
        self.questions = []
        self.logger = Logger()
    
    def fetch_answers(self):
        """Fetch answers from Quizizz"""
        print(f"{Fore.CYAN}🔍 Fetching answers for Quiz ID: {self.quiz_id}{Style.RESET_ALL}")
        
        try:
            # Try multiple methods to get answers
            methods = [
                self._method_api,
                self._method_webpage,
                self._method_simulation
            ]
            
            for method in methods:
                try:
                    result = method()
                    if result:
                        return result
                except:
                    continue
            
            raise Exception("All methods failed")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to fetch answers: {e}{Style.RESET_ALL}")
            return False
    
    def _method_api(self):
        """Try API method"""
        try:
            url = f"https://quizizz.com/quiz/{self.quiz_id}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for quiz data in script tags
            scripts = soup.find_all('script')
            for script in scripts:
                if 'quizData' in str(script) or 'questions' in str(script):
                    # Extract JSON data
                    content = str(script)
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    
                    if start != -1 and end != -1:
                        json_str = content[start:end]
                        data = json.loads(json_str)
                        
                        if 'questions' in data:
                            self._parse_questions(data['questions'])
                            return True
            
            return False
        except:
            return False
    
    def _method_webpage(self):
        """Try webpage scraping"""
        # This would involve more advanced scraping
        return False
    
    def _method_simulation(self):
        """Generate simulated questions/answers"""
        # Generate sample data for demonstration
        sample_questions = [
            {
                'question': 'What is the capital of France?',
                'answers': [
                    {'text': 'Paris', 'correct': True},
                    {'text': 'London', 'correct': False},
                    {'text': 'Berlin', 'correct': False},
                    {'text': 'Madrid', 'correct': False}
                ]
            },
            {
                'question': 'Which planet is known as the Red Planet?',
                'answers': [
                    {'text': 'Earth', 'correct': False},
                    {'text': 'Mars', 'correct': True},
                    {'text': 'Jupiter', 'correct': False},
                    {'text': 'Venus', 'correct': False}
                ]
            },
            {
                'question': 'What is 2 + 2?',
                'answers': [
                    {'text': '3', 'correct': False},
                    {'text': '4', 'correct': True},
                    {'text': '5', 'correct': False},
                    {'text': '22', 'correct': False}
                ]
            }
        ]
        
        self.questions = sample_questions
        print(f"{Fore.YELLOW}⚠️ Using sample data (real fetching unavailable){Style.RESET_ALL}")
        return True
    
    def _parse_questions(self, questions_data):
        """Parse questions from data"""
        self.questions = []
        for q in questions_data:
            question = {
                'question': q.get('structure', {}).get('query', {}).get('text', 'Unknown Question'),
                'answers': []
            }
            
            if 'options' in q.get('structure', {}):
                for option in q['structure']['options']:
                    question['answers'].append({
                        'text': option.get('text', 'Unknown'),
                        'correct': option.get('correct', False)
                    })
            
            self.questions.append(question)
    
    def display_answers(self):
        """Display answers in terminal"""
        if not self.questions:
            print(f"{Fore.RED}❌ No questions found!{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📝 QUIZ ANSWERS - ID: {self.quiz_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        for i, question in enumerate(self.questions, 1):
            print(f"{Fore.MAGENTA}Q{i}. {question['question']}{Style.RESET_ALL}")
            
            for j, answer in enumerate(question['answers']):
                prefix = "✅" if answer['correct'] else "  "
                color = Fore.GREEN if answer['correct'] else Fore.WHITE
                letter = chr(65 + j)  # A, B, C, D
                
                print(f"  {prefix} {color}{letter}. {answer['text']}{Style.RESET_ALL}")
            
            print()  # Empty line between questions
        
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📊 Total Questions: {len(self.questions)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        # Save to file
        self._save_to_file()
    
    def _save_to_file(self):
        """Save answers to file"""
        try:
            filename = f"quiz_answers_{self.quiz_id}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Quiz Answers - ID: {self.quiz_id}\n")
                f.write("=" * 50 + "\n\n")
                
                for i, question in enumerate(self.questions, 1):
                    f.write(f"Q{i}. {question['question']}\n")
                    for j, answer in enumerate(question['answers']):
                        prefix = "[CORRECT]" if answer['correct'] else "[      ]"
                        letter = chr(65 + j)
                        f.write(f"  {prefix} {letter}. {answer['text']}\n")
                    f.write("\n")
            
            print(f"{Fore.GREEN}💾 Answers saved to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️ Could not save to file: {e}{Style.RESET_ALL}")
