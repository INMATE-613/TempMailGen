import aiohttp
import asyncio
import pyfiglet
from colorama import Fore, Style

class TextStyler:
    @staticmethod
    def banner(text):
        banner_text = pyfiglet.figlet_format(text)
        styled_text = f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}{banner_text}{Fore.RESET}{Style.NORMAL}"
        return styled_text

    @staticmethod
    def warning(text):
        styled_text = f"{Fore.LIGHTYELLOW_EX}[!]{Fore.RESET}{Style.DIM} {text}{Fore.RESET}{Style.NORMAL}"
        return styled_text

    @staticmethod
    def success(text):
        styled_text = f"{Fore.LIGHTGREEN_EX}[+]{Fore.RESET}{Style.BRIGHT} {text}{Fore.RESET}{Style.NORMAL}"
        return styled_text

    @staticmethod
    def ask(text):
        styled_text = f"{Fore.LIGHTCYAN_EX}[?]{Fore.RESET}{Style.DIM} {text}{Fore.RESET}{Style.NORMAL}"
        return styled_text

class TempMailGenerator:
    def __init__(self):
        self.text_styler = TextStyler
        self.email_addresses = []

    async def generate_temp_email_addresses(self, count):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for _ in range(count):
                task = self.generate_single_temp_email(session)
                tasks.append(task)
            self.email_addresses = await asyncio.gather(*tasks)

    async def generate_single_temp_email(self, session):
        api_url = "https://www.1secmail.com/api/v1/?action=genRandomMailbox"
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                return data[0]
            else:
                print(self.text_styler.warning(f"Error: {response.status} - {await response.text()}"))
                return None

    async def check_mail(self, email):
        login, domain = email.split('@')
        api_url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    messages = await response.json()
                    return messages
                else:
                    print(self.text_styler.warning(f"Error: {response.status} - {await response.text()}"))
                    return None

    async def run(self, num_emails):
        await self.generate_temp_email_addresses(num_emails)
        if self.email_addresses:
            print(self.text_styler.success("Generated Emails") + "\n")
            for email in self.email_addresses:
                print(self.text_styler.success(email))
            while True:
                option = input(self.text_styler.ask("Enter the email address to check mail (or 'exit' to quit): "))
                if option.lower() == "exit":
                    break
                elif option in self.email_addresses:
                    messages = await self.check_mail(option)
                    if messages:
                        print(self.text_styler.success(f"Messages for {option}:"))
                        for message in messages:
                            print(message)
                    else:
                        print(self.text_styler.warning(f"No messages for {option}"))
                else:
                    print(self.text_styler.warning("Invalid email address. Please enter a valid one from the generated list."))

if __name__ == "__main__":
    styler = TextStyler()
    print(styler.banner("TempMail"))
    print(styler.warning("https://github.com/idkconsole\n"))
    num_emails = int(input(styler.ask("Enter the number of email addresses to generate: ")))
    email_manager = TempMailGenerator()
    asyncio.run(email_manager.run(num_emails))
