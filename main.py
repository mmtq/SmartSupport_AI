import time
from extraction import EmailFetcher
from agent import AICustomerSupportAgent

if __name__ == "__main__":
    agent = AICustomerSupportAgent()
    fetcher = EmailFetcher()

    while True:
        new_emails = fetcher.fetch_new_emails()
        if new_emails:
            for email in new_emails:
                print(f"Sender: {email['sender_name']} <{email['sender_addr']}>")
                print(f"Subject: {email['subject']}")
                print(f"Body: {email['body']}")
                print("=" * 50)

                evaluation_result = agent.process_email(email)
                if evaluation_result:
                    print(f"Sending reply: {evaluation_result}")
                    fetcher.send_mail(recipient=email['sender_addr'], subject=f"Re: {email['subject']}", body=evaluation_result)

        time.sleep(10)
